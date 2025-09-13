from __future__ import annotations

import sys
import inspect
import subprocess
import wave
import piper  # Local neural TTS
from mutagen.mp3 import MP3  # Audio length checking
import time
import re
import os
import requests
from pathlib import Path
from typing import Optional, List

"""
GuideFrame TTS (Piper) — version-agnostic

- Works with both *older* Piper (rhasspy) API: PiperVoice.synthesize(text, wav_file, ...)
  and *newer* OHF API: PiperVoice.synthesize(text, config=SynthesisConfig(...)).

- Speed control (without pitch change):
  * Prefer Piper length_scale at synthesis time (faster = smaller length_scale).
  * If the installed Piper doesn't accept timing params, fall back to ffmpeg 'atempo'.

- Sends diagnostics to stderr (keeps stdout clean).
- Outputs MP3 via ffmpeg. A temporary WAV is written and then removed.

Usage:
    export_piper_tts(text, "out.mp3", speed=1.25, sentence_silence=0.05)
"""

# ------------------------------------------------------------------------------
# Voice model management
# ------------------------------------------------------------------------------

def get_voice_model_path() -> Path:
    """Get the path to the voice model, downloading if necessary."""
    voice_dir = Path.home() / ".guideframe" / "voices"
    voice_dir.mkdir(parents=True, exist_ok=True)

    voice_file = voice_dir / "en_GB-alan-medium.onnx"

    if not voice_file.exists():
        print("Voice model not found. Downloading...", file=sys.stderr)
        if download_voice_model(voice_file) is None:
            raise FileNotFoundError(f"Could not download voice model to {voice_file}")

    return voice_file


def download_voice_model(voice_file: Path) -> Optional[Path]:
    """Download the voice model from Hugging Face (.onnx only)."""
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium"
    url = f"{base_url}/en_GB-alan-medium.onnx"

    try:
        print(f"Downloading voice model from {url}", file=sys.stderr)
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(voice_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rDownload progress: {percent:.1f}%", end="", flush=True, file=sys.stderr)

        print(f"\nVoice model downloaded successfully to {voice_file}", file=sys.stderr)
        return voice_file

    except Exception as e:
        print(f"Error downloading voice model: {e}", file=sys.stderr)
        return None

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def _speed_to_length_scale(speed: float) -> float:
    """
    Map a human-friendly speed multiplier to Piper's length_scale.
    speed > 1.0 => faster; speed < 1.0 => slower.
    Rule-of-thumb: length_scale = 1 / speed.
    Clamped to a sane range.
    """
    try:
        speed = float(speed)
    except Exception:
        speed = 1.0
    if speed <= 0:
        speed = 1.0
    ls = 1.0 / speed
    return max(0.4, min(ls, 2.5))


def _atempo_chain(speed: float) -> List[str]:
    """
    Build a safe atempo chain for ffmpeg. Each 'atempo' filter supports 0.5..2.0.
    Returns a list like: ['-filter:a', 'atempo=2.0,atempo=1.25'] or [] if speed≈1.0.
    """
    try:
        speed = float(speed)
    except Exception:
        speed = 1.0

    if abs(speed - 1.0) < 1e-6:
        return []

    factors = []
    remaining = speed

    # Break >2.0 into repeated 2.0
    while remaining > 2.0:
        factors.append(2.0)
        remaining /= 2.0

    # Build <0.5 into repeated 0.5
    while remaining < 0.5:
        factors.append(0.5)
        remaining /= 0.5

    factors.append(remaining)
    chain = ",".join(f"atempo={f:.6g}" for f in factors)
    return ["-filter:a", chain]


def write_wav_file(filename: str, audio_data: bytes, sample_rate: int, channels: int, bits_per_sample: int) -> None:
    """Write PCM audio data to a WAV file with proper headers."""
    header = bytearray()

    # RIFF header
    header.extend(b"RIFF")
    file_size = len(audio_data) + 36  # 36 bytes for header
    header.extend((
        file_size & 0xFF,
        (file_size >> 8) & 0xFF,
        (file_size >> 16) & 0xFF,
        (file_size >> 24) & 0xFF,
    ))
    header.extend(b"WAVE")

    # fmt chunk
    header.extend(b"fmt ")
    header.extend((16, 0, 0, 0))  # fmt chunk size
    header.extend((1, 0))         # audio format (PCM)
    header.extend((channels, 0))  # num channels
    header.extend((
        sample_rate & 0xFF,
        (sample_rate >> 8) & 0xFF,
        (sample_rate >> 16) & 0xFF,
        (sample_rate >> 24) & 0xFF,
    ))
    byte_rate = sample_rate * channels * bits_per_sample // 8
    header.extend((
        byte_rate & 0xFF,
        (byte_rate >> 8) & 0xFF,
        (byte_rate >> 16) & 0xFF,
        (byte_rate >> 24) & 0xFF,
    ))
    block_align = channels * bits_per_sample // 8
    header.extend((block_align, 0))
    header.extend((bits_per_sample, 0))

    # data chunk
    header.extend(b"data")
    data_size = len(audio_data)
    header.extend((
        data_size & 0xFF,
        (data_size >> 8) & 0xFF,
        (data_size >> 16) & 0xFF,
        (data_size >> 24) & 0xFF,
    ))

    with open(filename, "wb") as f:
        f.write(header)
        f.write(audio_data)

# ------------------------------------------------------------------------------
# TTS core
# ------------------------------------------------------------------------------

def export_piper_tts(
    text: str,
    file_name: str,
    *,
    speed: float = 1.0,                  # 1.0 = default; 1.25 ≈ 25% faster, etc.
    length_scale: Optional[float] = None,# override for raw control
    sentence_silence: float = 0.15,      # seconds of silence between sentences (if supported)
    noise_w: Optional[float] = None,     # optional: affects cadence/variability (if supported)
    noise_scale: Optional[float] = None
) -> None:
    """
    Synthesize speech to MP3 using Piper.
    - Tries to set timing at synthesis (length_scale) if API supports it.
    - Otherwise applies ffmpeg 'atempo' to preserve pitch while changing speed.
    """
    voice_model_path = get_voice_model_path()
    tts = piper.PiperVoice.load(voice_model_path)

    eff_ls = float(length_scale) if length_scale is not None else _speed_to_length_scale(float(speed))
    used_length_scale = False
    sample_rate = None

    # Always render a temp WAV, then convert to MP3
    temp_wav = file_name.replace(".mp3", "_temp.wav")

    # Inspect Piper API to pick the right path
    sig = inspect.signature(tts.synthesize)
    params = sig.parameters
    print(f"[debug] Piper synth signature: {sig}", file=sys.stderr)

    if "config" in params:
        # Newer OHF-style API: synthesize(text, config=SynthesisConfig(...)) -> chunks
        try:
            from piper import SynthesisConfig
        except Exception as e:
            raise RuntimeError("Piper exposes 'config' but SynthesisConfig import failed") from e

        print("[debug] Using OHF API with SynthesisConfig", file=sys.stderr)
        chunks = list(tts.synthesize(
            text,
            config=SynthesisConfig(
                length_scale=eff_ls,
                sentence_silence=sentence_silence,
                noise_w=noise_w,
                noise_scale=noise_scale,
            )
        ))
        if not chunks:
            raise RuntimeError("Piper returned no audio")
        sample_rate = getattr(chunks[0], "sample_rate", 22050)
        audio_data = b"".join(getattr(c, "audio_int16_bytes", b"") for c in chunks)
        write_wav_file(temp_wav, audio_data, sample_rate, 1, 16)
        used_length_scale = True

    elif "wav_file" in params:
        # Older rhasspy-style API: synthesize(text, wav_file, ...)
        # Many older builds reject timing kwargs entirely, so be conservative.
        print("[debug] Using legacy API with wav_file handle", file=sys.stderr)
        with wave.open(temp_wav, "wb") as wav_file:
            # Older Piper writes WAV params & frames internally.
            # Passing timing kwargs can cause TypeError on some builds, so avoid them.
            tts.synthesize(text, wav_file)
        # sample_rate will be read by ffmpeg from the temp WAV header.

    else:
        # Unknown API shape
        raise RuntimeError(f"Unsupported PiperVoice.synthesize signature: {sig}")

    # Build ffmpeg command (apply atempo only if we couldn't use length_scale)
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_wav,
        "-acodec", "libmp3lame",
        "-ab", "128k",
    ]
    if used_length_scale:
        # Keep native rate if we learned it; otherwise let ffmpeg decide.
        if sample_rate:
            cmd += ["-ar", str(sample_rate)]
    else:
        # Apply pitch-preserving speed change at encode time
        cmd += _atempo_chain(speed)

    cmd += [file_name]

    try:
        print(f"[debug] Running: {' '.join(cmd)}", file=sys.stderr)
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8", errors="ignore") if e.stderr else str(e)
        print(err, file=sys.stderr)
        raise
    finally:
        try:
            os.remove(temp_wav)
        except Exception:
            pass

    print(f"Exported {file_name} (speed={speed:.2f}, used_length_scale={used_length_scale})")


# Keep the old function name for backward compatibility
def export_gtts(text: str, file_name: str) -> None:
    """Legacy name - now uses Piper instead of gTTS."""
    # Default to a slightly faster cadence and tighter pauses.
    export_piper_tts(text, file_name, speed=1.25, sentence_silence=0.05)

# ------------------------------------------------------------------------------
# Duration/sleep utilities
# ------------------------------------------------------------------------------

def sleep_based_on_vo(file_name: str) -> None:
    """Sleep for the duration of an audio file (MP3/WAV), with ffprobe fallback."""
    try:
        audio = MP3(file_name)  # MP3 path
        duration = audio.info.length
    except Exception:
        try:
            import wave as _wave  # WAV path
            with _wave.open(file_name, "rb") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
        except Exception:
            try:
                # ffprobe fallback
                result = subprocess.run(
                    ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", file_name],
                    capture_output=True, text=True, check=True
                )
                duration = float(result.stdout.strip())
            except Exception:
                print(f"Warning: Could not determine duration of {file_name}, sleeping for 3 seconds", file=sys.stderr)
                duration = 3.0

    print(f"Sleeping for {duration:.3f} seconds", file=sys.stderr)
    time.sleep(duration)

# ------------------------------------------------------------------------------
# Markdown/Python extraction utilities
# ------------------------------------------------------------------------------

def pull_vo_from_markdown(md_file: str, step_number: int) -> Optional[str]:
    """Extract the markdown content under '## Step {step_number}'."""
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Regex: match the step heading and capture until next '##' or EOF
    step_heading = rf"## Step {step_number}\s*(.*?)\s*(?=\n##|\Z)"
    match = re.search(step_heading, md_content, re.DOTALL)
    return match.group(1).strip() if match else None


def pull_vo_from_python_file(py_file: str, step_number: int) -> Optional[str]:
    """Extract markdown-like content embedded in a Python file."""
    with open(py_file, "r", encoding="utf-8") as f:
        py_content = f.read()

    # Prefer explicit triple-quoted block starting with the word 'markdown'
    markdown_pattern = r'(?:\'\'\'|""")[\s]*markdown[\s]*\n(.*?)(?:\'\'\'|""")'
    markdown_match = re.search(markdown_pattern, py_content, re.DOTALL | re.IGNORECASE)
    markdown_content = markdown_match.group(1) if markdown_match else py_content

    step_heading = rf"## Step {step_number}\s*(.*?)\s*(?=\n##|\Z)"
    match = re.search(step_heading, markdown_content, re.DOTALL)
    return match.group(1).strip() if match else None

# ------------------------------------------------------------------------------
# High-level voiceover function
# ------------------------------------------------------------------------------

def generate_voicover(source_file: str, step_number: int) -> None:
    """Create an MP3 voiceover for the given step by extracting text from .md/.py."""
    # Extract text
    if source_file.endswith(".py"):
        voiceover = pull_vo_from_python_file(source_file, step_number)
