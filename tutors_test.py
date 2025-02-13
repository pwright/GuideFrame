import sys # Importing the sys module to access system arguments
from selenium_functions import * # Moved all selenium functions to external file
import time  # Importing the time module for sleep functions
from assembly import assemble  # Importing the assemble_clips function from assembly.py
from audio import export_gtts, sleep_based_on_vo  # Importing the export_gtts and sleep_based_on_vo functions from audio.py
from video import start_ffmpeg_recording, stop_ffmpeg_recording  # Importing the start_ffmpeg_recording and stop_ffmpeg_recording functions from video.py

# Setting the environment based on the system argument (default arg must be 1 hence > 1)
if len(sys.argv) > 1:
    env = sys.argv[1]  # Getting the environment argument

    # Setting the input format and display based on the environment argument
    if env == "macos": # My local environment
        input_format = 'avfoundation'
        input_display = '1'
        driver_location = '/opt/homebrew/bin/chromedriver'
    elif env == "github": # GitHub Actions environment
        input_format = 'x11grab'
        input_display = ':99.0'
        driver_location = '/usr/bin/chromedriver'
    else:
        print("Invalid environment specified. Use 'macos' or 'github'.")
        sys.exit(1)
else:
    print("No environment argument provided. Use 'macos' or 'github'.")
    sys.exit(1)

# Function to run a step in the guide, passing all previously hard coded actions as params
def guide_step(step_number, voiceover, *actions, order="action-after-vo"):
    # Start the recording for the step
    step = start_ffmpeg_recording(f"step{step_number}.mp4", input_format, input_display)
    # Conditional logic to account for vo relative to action
    if order == "action-before-vo":
        for action in actions:
            action()
            time.sleep(1)
        export_gtts(voiceover, f"step{step_number}.mp3")
        sleep_based_on_vo(f"step{step_number}.mp3")
    # Default value for order is after-vo
    if order == "action-after-vo":
        export_gtts(voiceover, f"step{step_number}.mp3")
        sleep_based_on_vo(f"step{step_number}.mp3")
        for action in actions:
            action()
            time.sleep(1)
    stop_ffmpeg_recording(step)

'''
As of GUIDEFRAME-13, implemented during sprint 2, the script has been refactored via new function
guide_steps() which passes the step number, string for VO, action(s) and order of action relative to VO.
This greatly reduces the amount of code required to run the walkthrough and makes it more legible.
If GUIDEFRAME-25 is successfully implemented, the string will be replaced by another function call, 
further enhancing the legibility of the script. Of note, this doesn't prevent a user from hard-coding 
the steps if they wish to further customise the interactions.
'''

# Function to run the main walkthrough section
def guideframe_script():
    # Main walkthrough logic here divided into steps etc (will hopefully be more legible after future refactors)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    try:
        '''
        Setup - Setup driver and Open Tutors.dev and set window size etc
        '''
        driver = driver_setup(driver_location) # Initializing driver as the return value from the setup function in selenium script
        set_window_size(driver)
        open_url(driver, "https://tutors.dev")
        time.sleep(2)  # Give the page time to load

        '''
        Step 1 - Open Tutors
        '''
        guide_step(
            1, 
            "First, let's open tutors.dev. On this page we see the web toolkit, in addition to any courses we may recently have accessed.", 
            lambda: None
            )
        
        '''
        Step 2 - setting dark mode
        '''
        guide_step(
            2,
            "Before we go any further, let's change to dark mode using the layout button in the top right of the screen",
            lambda: click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block"),
            lambda: click_element(driver, "label[data-testid='segment-item']"),
            lambda: click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block")
            )

        '''
        Step 3 - navigating to the docs page
        '''
        guide_step(
            3,
            "Now that we're in dark mode, let's navigate to the docs page by clicking the docs button under the web toolkit",
            lambda: hover_and_click(driver, "/course/tutors-reference-manual")
            )

        '''
        Step 4 - Docs page intro
        '''
        guide_step(
            4,
            "On the docs page, we can see a number of cards. Each of these cards leads to a specific portion of the getting started guide.",
            lambda: None
            )

        '''
        Step 5 - Hovering over the first card
        '''
        guide_step(
            5,
            "The getting started card introduces the basic design model of tutors.",
            lambda: hover_over_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started"),
            order="action-before-vo"
            )

        '''
        Step 6 - Hovering over the second card
        '''
        guide_step(
            6,
            "The simple starter card provides a helpful template course.",
            lambda: hover_over_element(driver, "/course/tutors-starter-course"),
            order="action-before-vo"
            )

        '''
        Step 7 - Hovering over the third card
        '''
        guide_step(
            7,
            "The alternative starter card provides an example course to demonstrate layouts and nesting.",
            lambda: hover_over_element(driver, "/course/layout-reference-course"),
            order="action-before-vo"
            )

        '''
        Step 8 - Hovering over the fourth card
        '''
        guide_step(
            8,
            "The reference course contains another example course. This one contains all Tutors learning objects for demonstration.",
            lambda: scroll_to_element(driver, "/course/reference-course"),
            lambda: hover_over_element(driver, "/course/reference-course"),
            order="action-before-vo"
            )

        '''
        Step 9 - Retuning to the original card
        '''
        guide_step(
            9,
            "Finally, let's return to the getting started card and click it to demonstrate the getting started page.",
            lambda: scroll_to_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started"),
            lambda: hover_and_click(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started")
            )

    finally:
        print("Test complete -> moving to assembly")
        driver.quit()

# End of walkthrough section
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Main function to run the test and assemble the clips (now passing the number of steps to the assembly function)
if __name__ == "__main__":
    guideframe_script()
    assemble(9)
