---
title: Video
layout: default
nav_order: 2
parent: Library
permalink: /video/
---

# Video
The video file contains functions designed to provide start and stop the `ffmpeg` recordings used to capture each GuideFrame step. The following section will list each function contained within this file and provide some insight into its use and syntax.


### `start_ffmpeg_recording()`
```python
def start_ffmpeg_recording(output_file, input_format, input_display):
    print("Beginning recording of clip")
    command = [
        'ffmpeg',
        '-f', input_format,           # Input format
        '-video_size', '1920x1080',   # Resolution
        '-framerate', '30',           # Frame rate
        '-i', input_display,          # Input display (1 or :99.0 for GitHub actions)
        '-vcodec', 'libxvid',         # Video codec
        '-preset', 'fast',            # Preset for encoding speed
        '-b:v', '3000k',              # Bitrate
        '-pix_fmt', 'yuv420p',        # Pixel format                 
        output_file                   # Output file path
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    return process
```
This function is responsible for starting the `ffmpeg` recording which will be used to capture the virtual screen on which the GuideFrame interactions are occuring. 

It takes the `output_file`, `input_format` and `input_display` variables in order to account for the environment differences in command flags and the desired final file name.

It then uses `subprocess` to run the `ffmpeg` command, passing the array of flags outlined above.


### `stop_ffmpeg_recording()`
```python
def stop_ffmpeg_recording(process):
    process.stdin.write(b"q\n")  # Send 'q' to gracefully stop the recording
    process.communicate()         # Wait for the process to finish
    print("Ending recording of clip")
```
This function takes the return value of the previous function and passes `q` to standard in. This prompts the running process to quit, completing the recording cycle.