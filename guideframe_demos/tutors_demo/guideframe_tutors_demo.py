from guideframe.selenium import * # Moved all selenium functions to external file
from guideframe.assembly import assemble  # Importing the assemble_clips function from assembly.py
from guideframe.utils import guide_step, get_env_settings  # Importing the guide_step and get_env_settings functions from guideframe_utils.py


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

        '''
        Step 4 - Docs page intro
        '''
        guide_step(
            4,
            lambda: None
            )

        '''
        Step 5 - Hovering over the first card
        '''
        guide_step(
            5,
            lambda: hover_over_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started"),
            order="action-before-vo"
            )

        '''
        Step 6 - Hovering over the second card
        '''
        guide_step(
            6,
            lambda: hover_over_element(driver, "/course/tutors-starter-course"),
            order="action-before-vo"
            )

        '''
        Step 7 - Hovering over the third card
        '''
        guide_step(
            7,
            lambda: hover_over_element(driver, "/course/layout-reference-course"),
            order="action-before-vo"
            )

        '''
        Step 8 - Hovering over the fourth card
        '''
        guide_step(
            8,
            lambda: scroll_to_element(driver, "/course/reference-course"),
            lambda: hover_over_element(driver, "/course/reference-course"),
            order="action-before-vo"
            )

        '''
        Step 9 - Click the search button
        '''
        guide_step(
            9,
            lambda: click_element_by_xpath(driver, '/html/body/div[1]/div[1]/header/header/section/div[3]/div[1]/div[3]/button/div/span[2]'),
            )
        
        '''
        Step 10 - Search for a term
        '''
        guide_step(
            10,
            lambda: type_into_field(driver, "search", "card"),
            )
        
        '''
        Step 11 - Open the search result in a new tab
        '''
        guide_step(
            11,
            lambda: open_link_in_new_tab(driver, "https://tutors.dev/note/tutors-reference-manual/unit-1-fundamentals/note-02-cards")
        )
        
        '''
        Step 12 - End demo
        '''
        guide_step(
            12,
            lambda: None
        )
        

    finally:
        print("Script complete -> moving to assembly")
        driver.quit()


# Main function to run the test and assemble the clips
if __name__ == "__main__":
    guideframe_script()
    assemble(12)
