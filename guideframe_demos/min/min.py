from guideframe.selenium import * # Moved all selenium functions to external file
from guideframe.assembly import assemble  # Importing the assemble_clips function from assembly.py
from guideframe.utils import guide_step, get_env_settings  # Importing the guide_step and get_env_settings functions from guideframe_utils.py

"""markdown
## Step 1 
This GuideFrame demo begins by opening tutors.dev. This is achieved by using the open u r l function prior to step 1.

## Step 2
We can demonstrate the ability to pass multiple actions to GuideFrame by activating dark mode. This involves 3 calls to the click element function. We'll also call the sleep function for 0.5 seconds between each action.

## Step 3
Now let's use the hover and click function to move to the tutors reference manual.

"""

# Function to run the main walkthrough section
def guideframe_script():
    try:
        '''
        Setup - Setup driver and Open Tutors.dev and set window size etc
        '''
        env_settings = get_env_settings()  # Getting the environment settings
        driver_location = env_settings["driver_location"]  # Getting the driver location from the settings
        driver = driver_setup(driver_location) # Initializing driver as the return value from the setup function in selenium script
        set_window_size(driver)
        open_url(driver, "https://tutors.dev")

        '''
        Step 1 - Open Tutors
        '''
        guide_step(
            1, 
            lambda: None,
            )
        
        '''
        Step 2 - setting dark mode
        '''
        guide_step(
            2,
            lambda: click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block"),
            lambda: sleep_for(0.5),
            lambda: click_element(driver, "label[data-testid='segment-item']"),
            lambda: sleep_for(0.5),
            lambda: click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block"),
            )

        '''
        Step 3 - navigating to the docs page
        '''
        guide_step(
            3,
            lambda: hover_and_click(driver, "/course/tutors-reference-manual"),
            )



    finally:
        print("Script complete -> moving to assembly")
        driver.quit()


# Main function to run the test and assemble the clips
if __name__ == "__main__":
    guideframe_script()
    assemble(12)
