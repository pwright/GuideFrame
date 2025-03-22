---
title: Utils
layout: default
nav_order: 1
parent: Library
permalink: /utils/
---

# Utils
The utils file contains functions designed to provide vital variables to other aspects of the GuideFrame logic in addition to outlining the logic of the key `guide_step`. The following section will list each function contained within this file and provide some insight into its use and syntax.


### `get_env_settings()`
```python
def get_env_settings():
    if len(sys.argv) > 1:
        env = sys.argv[1]  # Getting the environment argument
    else:
        print("No environment argument provided. Use 'macos' or 'github'.")
        sys.exit(1)

    # Define settings based on environment
    if env == "macos":
        return {
            "input_format": "avfoundation",
            "input_display": "1",
            "driver_location": "/opt/homebrew/bin/chromedriver"
        }
    elif env == "github":
        return {
            "input_format": "x11grab",
            "input_display": ":99.0",
            "driver_location": "/usr/bin/chromedriver"
        }
    else:
        print("Invalid environment specified. Use 'macos' or 'github'.")
        sys.exit(1)
```
This function takes the system argument provided to the GuideFrame script and sets vital environmental variables based on this. This function is key in accounting for the variance in file paths, display type etc.


### `extract_md_filename()`
```python
def extract_md_filename():
    script_name = sys.argv[0]
    return script_name.replace(".py", ".md")
```
This function extracts the GuideFrame scripts name from the system argument before replacing the `.py` extension with `.md`. This is performed in order to ascertain the title of the GuideFrame scripts matching markdown file. The markdown file MUST match the GuideFrame scripts title or the core logic will fail.


### `extract_script_name()`
```python
def extract_script_name():
    script_name = sys.argv[0]
    return script_name.replace(".py", "")
```
This function serves a similar purpose and shares logic with `extract_md_filename()`. It is used to drop the `.py` extension in order to grab the scripts name for final output file naming.


### ```guide_step()```
```python
def guide_step(step_number, *actions, order="action-after-vo"):
    # Get the environment settings
    env_settings = get_env_settings()
    input_format = env_settings["input_format"]
    input_display = env_settings["input_display"]
    md_file = extract_md_filename()

    # Start the recording for the step
    step = start_ffmpeg_recording(f"step{step_number}.mp4", input_format, input_display)

    # Conditional logic to account for vo relative to action
    if order == "action-before-vo":
        for action in actions:
            action()
        generate_voicover(md_file, step_number)
    else:  # Default order is action-after-vo
        generate_voicover(md_file, step_number)
        for action in actions:
            action()

    stop_ffmpeg_recording(step)
```
This is the function which carries out each individual step of a GuideFrame script. It takes multiple arguments in the form of:
* `step_number` in order to match to the correct markdown step number.
* `*actions` to allows the user to pass any number of functions via `lambda`.
* `order` which defaults to `"actions-after-vo"`. This allows the user some level of control over how actions and voiceover are recorded relative to each other.

Its logic follows the below order:
1. It calls `get_env_settings()` in order to extract the variables it will need to pass to `ffmpeg`.
2. It then calls `extract_md_filename()` in order to later pass this filename to `generate_voiceover()`. 
3. It then calls `start_ffmpeg_recording()`, passing the step number, in order to name the output file accordingly, alongside the aforementioned input variables.
4. It checks the status of the `order` variable before iterating through the actions before or after calling `generate_voiceover`.
5. Once the above has been completed, it calls `stope_ffmpeg_recording` and the step's video and matching audio are now complete as separate files.







