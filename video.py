import ffmpeg # Importing the python-ffmpeg wrapper to match functionality but improve legibility

'''
Starts recording the screen with FFmpeg using ffmpeg-python wrapper
We still need the process object in order to pass 'q' in order to end the recording
The wrapper doesn't have a stop() command or an equivalent hence this combo of both versions
'''
def start_ffmpeg_recording(output_file):
    print("Beginning recording of clip")
    process = (
        ffmpeg
        .input(
            '1',                      # Input display (can be changed obvs but this is my main display)
            format='avfoundation',    # Capture avfoundation (because I'm on mac)
            video_size='1920x1080',   # Resolution
            framerate=60              # Frame rate
        )
        .output(
            output_file,
            vcodec='libxvid',         # Video codec
            preset='fast',            # Preset for encoding speed
            bitrate='3000k',          # Bitrate
            pix_fmt='yuv420p'         # Pixel format
        )
        .overwrite_output()
        .run_async(pipe_stdin=True)   # Runing asynchronously to allow interaction via stdin (the 'q' from below)
    )
    return process


# Function to stop FFmpeg recording
def stop_ffmpeg_recording(process):
    process.stdin.write(b"q\n")  # Gracefully stop FFmpeg by sending 'q' to stdin as a byte string
    process.communicate()        # Wait for process to finish
    print("Ending recording of clip")