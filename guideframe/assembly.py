import ffmpeg
import os
import uuid 
from guideframe.utils import extract_script_name

'''
The assembly.py file contains the functions to combine the audio and video files into a single video file
and perform any necessary cleanup. It interacts exensively with the audio functions and the utils to achieve this.
'''

def _debug_file_list(file_list_path):
    """Debug function to verify the file list format"""
    if os.path.exists(file_list_path):
        print(f"Debug: Contents of {file_list_path}:")
        with open(file_list_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        print(f"Debug: File size: {os.path.getsize(file_list_path)} bytes")
    else:
        print(f"Debug: {file_list_path} does not exist")

def _validate_video_file(file_path):
    """Validate that a file is a valid video file using FFmpeg"""
    try:
        # Use FFmpeg to probe the file and check if it's a valid video
        probe = ffmpeg.probe(file_path)
        if probe and 'streams' in probe:
            video_streams = [s for s in probe['streams'] if s['codec_type'] == 'video']
            if video_streams:
                print(f"Validated {file_path}: {video_streams[0]['codec_name']} video, {probe['format']['duration']}s")
                return True
            else:
                print(f"Warning: {file_path} has no video streams")
                return False
        else:
            print(f"Warning: {file_path} could not be probed by FFmpeg")
            return False
    except ffmpeg.Error as e:
        print(f"Warning: {file_path} is not a valid video file: {e}")
        return False
    except Exception as e:
        print(f"Warning: Error validating {file_path}: {e}")
        return False

def _ensure_working_directory():
    """Ensure we're in the correct working directory for file operations"""
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # Check if we're in a directory that contains the expected files
    if not any(os.path.exists(f"step{i}.mp4") for i in range(1, 10)):
        print("Warning: Expected step files not found in current directory")
        # List current directory contents for debugging
        print("Current directory contents:")
        for item in os.listdir('.'):
            if item.endswith(('.mp4', '.mp3')):
                print(f"  {item}")
    return current_dir

# Combinging audio and video via wrapper (wrapper aids legibility and removes need for subprocess)
def assemble_audio_video(video_file, audio_file, output_file):
    # Check that both files exist
    if os.path.exists(video_file) and os.path.exists(audio_file):
        # Validate file sizes to ensure they're not empty
        if os.path.getsize(video_file) == 0:
            print(f"Error: {video_file} is empty (0 bytes)")
            return False
        if os.path.getsize(audio_file) == 0:
            print(f"Error: {audio_file} is empty (0 bytes)")
            return False
            
        print(f"Combining {video_file} and {audio_file} into {output_file}")
        
        # The wrapper doesn't allow multiple .input tags like the '-i' in cli. This solution is from stack overflow
        video_in = ffmpeg.input(video_file)
        audio_in = ffmpeg.input(audio_file)
        combined_output = ffmpeg.output(video_in, audio_in, output_file, vcodec='copy', acodec='copy')
        try:
            (
                combined_output.run()
            )
            print(f"Successfully created: {output_file}")
            return True
        # Attempting to extract an error via the wrapper if one occurs
        except ffmpeg.Error as e:
            # Outputting the error
            error_output = e.stderr.decode('utf-8') if e.stderr else "No error details available."
            print(f"Error combining {video_file} and {audio_file}: {error_output}")
            return False
    else:
        missing_files = []
        if not os.path.exists(video_file):
            missing_files.append(video_file)
        if not os.path.exists(audio_file):
            missing_files.append(audio_file)
        print(f"Missing files: {missing_files}")
        return False


# Combining all of the audio + video combinations (result of the above)
def combine_all_videos(output_files, final_output):
    # Temp text file to iterate through
    file_list = "file_list.txt"
    
    # Filter out non-existent files and get absolute paths
    valid_files = []
    for video in output_files:
        if os.path.exists(video):
            # Convert to absolute path to ensure FFmpeg can find the files
            abs_path = os.path.abspath(video)
            # Validate that it's actually a valid video file
            if _validate_video_file(abs_path):
                valid_files.append(abs_path)
            else:
                print(f"Warning: {video} is not a valid video file, skipping...")
        else:
            print(f"Warning: {video} not found, skipping...")
    
    if not valid_files:
        print("Error: No valid video files found to combine")
        return False

    # Write the list of video files to the text file
    with open(file_list, "w", encoding='utf-8') as f:
        for video_path in valid_files:
            # Use proper escaping for file paths in concat file
            # Ensure the path is properly quoted and escaped
            safe_path = video_path.replace("'", "'\"'\"'")  # Escape single quotes
            f.write(f"file '{safe_path}'\n")

    # Debug: Verify the file list contents
    _debug_file_list(file_list)
    
    # Additional validation: check if the file list was written correctly
    if os.path.getsize(file_list) == 0:
        print("Error: File list is empty")
        return False

    try:
        # Run FFmpeg using the concat method and check for errors etc
        # Using more compatible codec settings
        input_stream = ffmpeg.input(file_list, format="concat", safe=0)
        output_stream = ffmpeg.output(
            input_stream, 
            final_output, 
            vcodec='copy',  # Copy video codec instead of re-encoding
            acodec='copy'   # Copy audio codec instead of re-encoding
        )
        
        print(f"Running FFmpeg command to combine {len(valid_files)} videos...")
        output_stream.run(overwrite_output=True)
        print(f"Successfully combined all videos into {final_output}")
        return True
    except ffmpeg.Error as e:
        error_output = e.stderr.decode('utf-8') if e.stderr else "No error details available."
        print(f"Error combining videos with concat demuxer: {error_output}")
        print("Attempting fallback method with filter_complex...")
        
        # Fallback: Use filter_complex concat filter
        try:
            # Create input streams for each video file
            inputs = []
            for video_path in valid_files:
                inputs.append(ffmpeg.input(video_path))
            
            # Use filter_complex to concatenate
            if len(inputs) == 1:
                # Single file, just copy it
                output_stream = ffmpeg.output(inputs[0], final_output, vcodec='copy', acodec='copy')
            else:
                # Multiple files, concatenate them
                concat_filter = ffmpeg.concat(*inputs, v=1, a=1)
                output_stream = ffmpeg.output(concat_filter, final_output, vcodec='copy', acodec='copy')
            
            output_stream.run(overwrite_output=True)
            print(f"Successfully combined all videos into {final_output} using fallback method")
            return True
            
        except ffmpeg.Error as fallback_error:
            fallback_error_output = fallback_error.stderr.decode('utf-8') if fallback_error.stderr else "No error details available."
            print(f"Fallback method also failed: {fallback_error_output}")
            print(f"FFmpeg command failed. Check that all input files are valid video files.")
            return False
    finally:
        # Removing the txt file
        if os.path.exists(file_list):
            os.remove(file_list)


# Combine individual video and audio for each step (obviously needs error handling etc but will do for now) (now taking in a number of clips rather than hardcoding in aid of tutors test)
def assemble(number_of_steps):
    # Ensure we're in the correct working directory
    _ensure_working_directory()
    
    # Combine individual video and audio for each step by iterating through files and passing to above functions
    clip_number = number_of_steps + 1
    successful_combinations = 0
    
    for i in range(1, clip_number):
        video_file = f"step{i}.mp4"
        audio_file = f"step{i}.mp3"
        output_file = f"output_step{i}.mp4"
        # Call the function to combine video and audio
        if assemble_audio_video(video_file, audio_file, output_file):
            successful_combinations += 1
        else:
            print(f"Failed to combine step {i}")
    
    print(f"Successfully combined {successful_combinations} out of {number_of_steps} steps")
    
    if successful_combinations == 0:
        print("Error: No video/audio combinations were successful. Cannot proceed with assembly.")
        return False
    
    # Now that all video/audio combinations are complete, combine the output videos into the final one
    output_files = [f"output_step{i}.mp4" for i in range(1, clip_number)]
    
    # Check if any output files exist before attempting to combine
    existing_files = [f for f in output_files if os.path.exists(f)]
    if not existing_files:
        print("Error: No output video files found to combine. Check that assemble_audio_video completed successfully.")
        return False
    
    print(f"Found {len(existing_files)} output files to combine: {existing_files}")
    
    # Now using the extract_script_name function from guideframe_utils.py to get the script name
    script_name = extract_script_name()
    # Creating a unique filename for the final output file via uuid and the extracted script name
    output_filename = f"{script_name}_{uuid.uuid4().hex[:6]}.mp4"
    # Combining all the videos into the final output as a single video
    if combine_all_videos(existing_files, output_filename):
        # Check if final_output exists and if so, clean up temporary files (the various mp3 and mp4 files we created)
        if os.path.exists(output_filename):
            print("Final output created. Cleaning up temporary files...")
            # Cleanup loop
            for i in range(1, clip_number):
                step_video = f"step{i}.mp4"
                step_audio = f"step{i}.mp3"
                output_step = f"output_step{i}.mp4"
                if os.path.exists(step_video):
                    os.remove(step_video)
                    print(f"Removed {step_video}")
                if os.path.exists(step_audio):
                    os.remove(step_audio)
                if os.path.exists(output_step):
                    os.remove(output_step)
                    print(f"Removed {output_step}")
            print("Cleanup complete.")
            return True
        else:
            print("Final output not found. No cleanup performed.")
            return False
    else:
        print("Failed to combine videos. No cleanup performed.")
        return False
