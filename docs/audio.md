---
title: Audio
layout: default
nav_order: 3
parent: Library
permalink: audio
---

# Audio
The audio file contains functions designed to provide the voiceover for each GuideFrame step. It interacts with both `gTTS` and markdown in order to create these mp3 files. The following section will list each function contained within this file and provide some insight into its use and syntax.

### `export_gtts()`
```python
def export_gtts(text, file_name):
    tts = gTTS(text)
    tts.save(file_name)
    print("Exported", file_name)
```
This function uses the `gTTS` python package in order to generate audio based on the user-prescribed text. It takes the `text` argument and passes it, along with a `file_name` to the native `gTTS` functions. This then writes an audio file, with the passed name and featuring the prescribed text, to the local directory.

### `sleep_based_on_vo()`
```python
 def sleep_based_on_vo(file_name):
    audio = MP3(file_name)
    print("Sleeping for", audio.info.length, "seconds")
    time.sleep(audio.info.length)
```
This function is designed to prevent the main script's interactions from accelerating beyond the recorded voiceover. It achieves this by taking the `file_name` of the .mp3 file created during the above function. It then parses the length of this audio file before using the `sleep` function from the `time` package to sleep based on the length found in seconds. This ensures that an interaction cannot occur until the requisite voiceover clip has completed.

### `pull_vo_from_markdown()`
```python
def pull_vo_from_markdown(md_file, step_number):
    # Open the markdown file and read
    with open(md_file, "r", encoding="utf-8") as file:
        md_content = file.read()
    
    '''
    Regex pattern breakdown:

    ## Step {step_number} -> The step heading to match
    \s* -> Any whitespace characters before the content
    (.*?) -> The content under the step heading
    (?=\n##|\Z) -> A lookahead to match the next step heading (##) or the end of the file
    '''

    # Define the regex pattern for the step heading (explained above)
    step_heading = rf"## Step {step_number}\s*(.*?)\s*(?=\n##|\Z)"

    # Search the markdown content for the step heading
    match = re.search(step_heading, md_content, re.DOTALL)

    # Return the content under the step heading if found
    return match.group(1).strip() if match else None
```
This function takes the `md_file` and `step_number` as arguments. It uses these to extract the text content of the markdown file by opening it and then using the `re` package to perform a regex parse (outlined in above code comments). This pattern ensures that the text must follow a `##` heading with text matching "Step n*". Provided a match is found, it is then returned.

### `generate_voiceover()`
```python
def generate_voicover(md_file, step_number):
    # Extract voiceover text from the .md file
    voiceover = pull_vo_from_markdown(md_file, step_number) # parsing the markdown

    # Check if content was found
    if not voiceover:
        print(f"Warning: No content found for Step {step_number}")
        return

    # Export the voiceover to an MP3 file
    export_gtts(voiceover, f"step{step_number}.mp3")
    # Sleeping based on the length of the voiceover
    sleep_based_on_vo(f"step{step_number}.mp3")
```
This function brings the above functions together. It takes `md_file` and `step_number` as arguments before passing these into a call to `pull_vo_from_markdown()`. It then checks for the presence of resulting voiceover.

It then uses the `export_gtts()` function where it passes the voiceover created above along with a file name created using the `step_number` variable. Finally, it calls the `sleep_based_on_vo()` function to complete the generation cycle.