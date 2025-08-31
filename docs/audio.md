---
title: Audio
layout: default
nav_order: 3
parent: Library
permalink: audio
---

# Audio
The audio file contains functions designed to provide the voiceover for each GuideFrame step. It interacts with Piper (local neural TTS) and markdown in order to create these mp3 files. The following section will list each function contained within this file and provide some insight into its use and syntax.

## Voice Model Management

Piper requires voice models to function. The system automatically downloads the `en_GB-alan-medium` voice model on first use to `~/.guideframe/voices/`. This ensures:
- No voice models are committed to the repository
- Users get high-quality neural TTS without manual setup
- Offline operation after initial download

### export_piper_tts()
```python
def export_piper_tts(text, file_name):
```
This function creates high-quality MP3 audio files using Piper's neural TTS engine. It:
- Generates audio from text using the downloaded voice model
- Creates a temporary WAV file for processing
- Converts to MP3 using ffmpeg for universal compatibility
- Automatically cleans up temporary files
- Returns the path to the generated MP3 file

**Parameters:**
- `text` (str): The text to convert to speech
- `file_name` (str): The output MP3 filename

**Returns:** None (creates the MP3 file directly)

**Example:**
```python
export_piper_tts("Hello, this is a test.", "test_output.mp3")
```

### export_gtts()
```python
def export_gtts(text, file_name):
```
This function is maintained for backward compatibility but now uses Piper instead of gTTS.

### sleep_based_on_vo()
```python
 def sleep_based_on_vo(file_name):
    audio = MP3(file_name)
    print("Sleeping for", audio.info.length, "seconds")
    time.sleep(audio.info.length)
```
This function is designed to prevent the main script's interactions from accelerating beyond the recorded voiceover. It achieves this by taking the `file_name` of the .mp3 file created during the above function. It then parses the length of this audio file before using the `sleep` function from the `time` package to sleep based on the length found in seconds. This ensures that an interaction cannot occur until the requisite voiceover clip has completed.

### pull_vo_from_markdown()
```python
def pull_vo_from_markdown(md_file, step_number):
    # Open the markdown file and read its contents
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Find the heading for the specified step
    pattern = rf'^## Step {step_number}\s*$(.*?)(?=^## Step {step_number + 1}\s*$|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    else:
        return None
```
This function extracts voiceover text from markdown files. It searches for content under headings like "## Step 1", "## Step 2", etc., and returns the text content for the specified step number.

### pull_vo_from_python_file()
```python
def pull_vo_from_python_file(py_file, step_number):
    # Open the python file and read its contents
    with open(py_file, 'r') as f:
        content = f.read()
    
    # Find the markdown comment for the specified step
    pattern = rf'# Step {step_number}:(.*?)(?=# Step {step_number + 1}:|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    else:
        return None
```
This function extracts voiceover text from Python files that contain embedded markdown comments. It searches for comments like "# Step 1:", "# Step 2:", etc., and returns the text content for the specified step number.

### generate_voicover()
```python
def generate_voicover(source_file, step_number):
```
This function orchestrates the entire voiceover generation process for a single step. It:
- Extracts voiceover text from either Python or markdown files
- Generates MP3 audio using Piper TTS
- Automatically sleeps for the duration of the generated audio
- Handles both file types automatically

**Parameters:**
- `source_file` (str): Path to the source file (.py or .md)
- `step_number` (int): The step number to generate voiceover for

**Example:**
```python
generate_voicover("tutorial.md", 1)
```

## Technical Details

- **Audio Format**: MP3 (128kbps, 22050Hz, mono)
- **Voice Model**: en_GB-alan-medium (British English, male voice)
- **TTS Engine**: Piper (local neural TTS)
- **Conversion**: WAV → MP3 using ffmpeg
- **Compatibility**: Universal MP3 support across all platforms and media players