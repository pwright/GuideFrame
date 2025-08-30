---
title: Assembly
layout: default
nav_order: 5
parent: Library
permalink: assembly
---

# Assembly
The assembly file contains the functions which act to combine the various files created during the GuideFrame pipeline. The following section will list each function contained within this file and provide some insight into its use and syntax.

## Key Improvements
The assembly functions now include:
- **Better error handling** with detailed error messages and return values
- **File validation** to ensure input files are valid video/audio files
- **Fallback methods** for video concatenation if the primary method fails
- **Working directory validation** to ensure files are found in expected locations
- **Debug logging** to help troubleshoot issues during the assembly process

### assemble_audio_video()
```python
def assemble_audio_video(video_file, audio_file, output_file):
    # Check that both files exist and are not empty
    if os.path.exists(video_file) and os.path.exists(audio_file):
        # Validate file sizes to ensure they're not empty
        if os.path.getsize(video_file) == 0:
            print(f"Error: {video_file} is empty (0 bytes)")
            return False
        if os.path.getsize(audio_file) == 0:
            print(f"Error: {audio_file} is empty (0 bytes)")
            return False
            
        print(f"Combining {video_file} and {audio_file} into {output_file}")
        
        # Create video and audio in variables for use in combined output
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
```
This function takes a `video_file`, `audio_file` and `output_file` as arguments. It now includes:
- **File existence validation** for both input files
- **File size validation** to ensure files are not empty
- **Better error reporting** with specific missing file information
- **Return values** (`True`/`False`) to indicate success or failure
- **Detailed logging** of the combination process

The function uses the `ffmpeg` python package to combine the files into a single output file, named by the passed argument. This file then contains the combined audio and video for a single `guide_step`.

### combine_all_videos()
```python
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
```
This function takes `output_files` and `final_output` as arguments. It now includes:
- **File validation** to ensure only valid video files are processed
- **Absolute path conversion** to avoid path resolution issues
- **Better error handling** with detailed error messages
- **Fallback concatenation method** using filter_complex if the concat demuxer fails
- **Debug logging** to show file list contents
- **Return values** to indicate success or failure

The function creates a text file listing all valid video files and uses FFmpeg's concat demuxer to combine them. If that fails, it falls back to using the filter_complex concat filter method.

### assemble()
```python
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
```
This function uses the two others from this file to perform the overall assembly and cleanup of GuideFrame step files. It now includes:
- **Working directory validation** to ensure files are found in expected locations
- **Success tracking** to monitor how many combinations were successful
- **Better error handling** with early returns on failures
- **File existence validation** before attempting video combination
- **Return values** to indicate overall success or failure

The function takes the `clip_number` argument and uses it to iterate through a loop of all audio and video files, creating appropriately named `output_file` during the loop. Within each loop, these files are passed to the `assemble_audio_video()` function for combination.

An array of the files outputted by this process is then created using another loop and the `clip_number` variable. A `script_name` variable is initialized using `extract_script_name()` from `utils`. An output file is then created using the `script_name` and a randomly generated `uuid`. The array and filename are then passed to `combine_all_videos()` for final assembly.

Once this process is complete, a check that a matching file exists is performed. Provided this is successful, a cleanup loop occurs using the `clip_number` variable again to iterate through all created audio and video files with the exception of the final output.

*Note: 1 is added to account for steps starting at 1. This means an iteration from 1 -> `clip_number` will have the intended range.*

## Helper Functions

### _validate_video_file()
Validates that a file is a valid video file using FFmpeg's probe functionality.

### _ensure_working_directory()
Checks the current working directory and warns if expected step files are not found.

### _debug_file_list()
Prints the contents of the file list for debugging purposes.

## Troubleshooting

If you encounter the "Invalid data found when processing input" error:

1. **Run the debug test script**: Use `python test_assembly.py` to diagnose issues
2. **Check file paths**: Ensure all video files exist and are accessible
3. **Verify FFmpeg installation**: Make sure FFmpeg is properly installed and in your PATH
4. **Check file formats**: Ensure all input files are valid MP4 files
5. **Review error logs**: The improved error handling will provide more detailed information

The assembly process now includes multiple fallback methods and comprehensive error handling to help identify and resolve issues during video processing.