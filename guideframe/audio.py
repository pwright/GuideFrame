import piper # Importing Piper for audio generation (local neural TTS engine)
from mutagen.mp3 import MP3 # Importing the MP3 module from mutagen for audio length checking
import time # Importing the time module for sleep functions
import re # Importing regex library as this proved a simple method for extracting text under headings
import os
import requests
from pathlib import Path

'''
Pivoting to Piper
This provides local neural text-to-speech with better quality than gTTS
Voice models are downloaded automatically on first use
'''

def get_voice_model_path():
    """Get the path to the voice model, downloading if necessary"""
    voice_dir = Path.home() / ".guideframe" / "voices"
    voice_dir.mkdir(parents=True, exist_ok=True)
    
    voice_file = voice_dir / "en_GB-alan-medium.onnx"
    
    if not voice_file.exists():
        print("Voice model not found. Downloading...")
        if download_voice_model(voice_file) is None:
            raise FileNotFoundError(f"Could not download voice model to {voice_file}")
    
    return voice_file

def download_voice_model(voice_file):
    """Download the voice model from Hugging Face"""
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium"
    
    # Download the .onnx file
    url = f"{base_url}/en_GB-alan-medium.onnx"
    
    try:
        print(f"Downloading voice model from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(voice_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rDownload progress: {percent:.1f}%", end='', flush=True)
        
        print(f"\nVoice model downloaded successfully to {voice_file}")
        return voice_file
        
    except Exception as e:
        print(f"Error downloading voice model: {e}")
        return None

# Function to create the Piper speech clips. Takes the text arg passed by the user and a file name to write it to
def export_piper_tts(text, file_name):
    voice_model_path = get_voice_model_path()
    
    # Initialize Piper with the voice model
    tts = piper.PiperVoice.load(voice_model_path)
    
    # Generate audio as WAV first, then convert to MP3 for better compatibility
    temp_wav = file_name.replace('.mp3', '_temp.wav')
    
    # Generate the audio content - synthesize returns AudioChunk objects, so we need to extract the audio data
    audio_data = b''.join(chunk.audio_int16_bytes for chunk in tts.synthesize(text))
    
    # Write the audio data to the temporary WAV file with proper WAV headers
    write_wav_file(temp_wav, audio_data, 22050, 1, 16)
    
    # Convert WAV to MP3 using ffmpeg
    import subprocess
    subprocess.run([
        'ffmpeg', '-y', '-i', temp_wav, '-acodec', 'libmp3lame', 
        '-ab', '128k', '-ar', '22050', file_name
    ], check=True, capture_output=True)
    
    # Clean up temporary WAV file
    os.remove(temp_wav)
    
    print(f"Exported {file_name}")

def write_wav_file(filename, audio_data, sample_rate, channels, bits_per_sample):
    """Write audio data to a WAV file with proper headers"""
    # WAV file header
    header = bytearray()
    
    # RIFF header
    header.extend(b'RIFF')
    file_size = len(audio_data) + 36  # 36 bytes for header
    header.extend((file_size & 0xFF, (file_size >> 8) & 0xFF, (file_size >> 16) & 0xFF, (file_size >> 24) & 0xFF))
    header.extend(b'WAVE')
    
    # fmt chunk
    header.extend(b'fmt ')
    header.extend((16, 0, 0, 0))  # fmt chunk size
    header.extend((1, 0))  # audio format (PCM)
    header.extend((channels, 0))  # number of channels
    header.extend((sample_rate & 0xFF, (sample_rate >> 8) & 0xFF, (sample_rate >> 16) & 0xFF, (sample_rate >> 24) & 0xFF))
    byte_rate = sample_rate * channels * bits_per_sample // 8
    header.extend((byte_rate & 0xFF, (byte_rate >> 8) & 0xFF, (byte_rate >> 16) & 0xFF, (byte_rate >> 24) & 0xFF))
    block_align = channels * bits_per_sample // 8
    header.extend((block_align, 0))
    header.extend((bits_per_sample, 0))
    
    # data chunk
    header.extend(b'data')
    data_size = len(audio_data)
    header.extend((data_size & 0xFF, (data_size >> 8) & 0xFF, (data_size >> 16) & 0xFF, (data_size >> 24) & 0xFF))
    
    # Write header and audio data
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(audio_data)

# Keep the old function name for backward compatibility
def export_gtts(text, file_name):
    """Legacy function name - now uses Piper instead of gTTS"""
    export_piper_tts(text, file_name)


# Function to check the length of an audio clip and then sleep based on it
def sleep_based_on_vo(file_name):
    try:
        # Try to read as MP3 first
        audio = MP3(file_name)
        duration = audio.info.length
    except:
        # If MP3 fails, try to read as WAV using wave module
        try:
            import wave
            with wave.open(file_name, 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
        except:
            # If both fail, try using ffprobe to get duration
            try:
                import subprocess
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                    '-of', 'csv=p=0', file_name
                ], capture_output=True, text=True, check=True)
                duration = float(result.stdout.strip())
            except:
                print(f"Warning: Could not determine duration of {file_name}, sleeping for 3 seconds")
                duration = 3.0
    
    print("Sleeping for", duration, "seconds")
    time.sleep(duration)


# Function to extract the markdown content under a specified heading
def pull_vo_from_markdown(md_file, step_number):
    # Open the markdown file and read
    with open(md_file, "r", encoding="utf-8") as file:
        md_content = file.read()
    
    '''
    Regex pattern breakdown:

    ## Step {step_number} -> The step heading to match
    \\s* -> Any whitespace characters before the content
    (.*?) -> The content under the step heading
    (?=\\n##|\\Z) -> A lookahead to match the next step heading (##) or the end of the file
    '''

    # Define the regex pattern for the step heading (explained above)
    step_heading = rf"## Step {step_number}\s*(.*?)\s*(?=\n##|\Z)"

    # Search the markdown content for the step heading
    match = re.search(step_heading, md_content, re.DOTALL)

    # Return the content under the step heading if found
    return match.group(1).strip() if match else None


# Function to extract markdown content from Python files containing embedded markdown
def pull_vo_from_python_file(py_file, step_number):
    # Open the Python file and read
    with open(py_file, "r", encoding="utf-8") as file:
        py_content = file.read()
    
    '''
    Look for markdown content embedded in the Python file.
    This could be in:
    1. Triple-quoted strings containing markdown
    2. Multi-line comments with markdown
    3. A specific markdown section
    '''
    
    # First, try to find markdown content in triple-quoted strings or comments
    # Look for pattern like '''markdown or """markdown followed by step content
    markdown_pattern = r'(?:\'\'\'|""")[\s]*markdown[\s]*\n(.*?)(?:\'\'\'|""")'
    markdown_match = re.search(markdown_pattern, py_content, re.DOTALL | re.IGNORECASE)
    
    if markdown_match:
        markdown_content = markdown_match.group(1)
    else:
        # If no explicit markdown block, look for step comments in the entire file
        markdown_content = py_content
    
    # Define the regex pattern for the step heading
    step_heading = rf"## Step {step_number}\s*(.*?)\s*(?=\n##|\Z)"
    
    # Search for the step heading
    match = re.search(step_heading, markdown_content, re.DOTALL)
    
    # Return the content under the step heading if found
    return match.group(1).strip() if match else None


# Function to generate the voiceover (in order to avoid repetition in main script)
def generate_voicover(source_file, step_number):
    # Check if source file is .py or .md
    if source_file.endswith('.py'):
        # Extract voiceover text from the .py file containing embedded markdown
        voiceover = pull_vo_from_python_file(source_file, step_number)
    else:
        # Extract voiceover text from the .md file (original behavior)
        voiceover = pull_vo_from_markdown(source_file, step_number)

    # Check if content was found
    if not voiceover:
        print(f"Warning: No content found for Step {step_number}")
        return

    # Export the voiceover to an MP3 file
    export_piper_tts(voiceover, f"step{step_number}.mp3")
    
    # Sleep based on the voiceover duration
    sleep_based_on_vo(f"step{step_number}.mp3")