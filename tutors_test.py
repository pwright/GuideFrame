from selenium import webdriver  # Importing the webdriver module from selenium and other modules
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time  # Importing the time module for sleep functions
from assembly import assemble  # Importing the assemble_clips function from assembly.py
from audio import export_gtts, sleep_based_on_vo  # Importing the export_gtts and sleep_based_on_vo functions from audio.py
from video import start_ffmpeg_recording, stop_ffmpeg_recording  # Importing the start_ffmpeg_recording and stop_ffmpeg_recording functions from video.py

'''
This file represents a more elaborate test script that uses the tutors website as a dynamic example. 
This test will be expanded but for now should demonstrate the concept in a less static setting than the wiki test.
Additionally, at the time of writing, this represents further refactoring where video and audio generation have been moved to separate files.
This should further aid separation of concerns and hopefully render this more legible.
Similarly, a potential improvement could be made in placing all selenium functions in a separate file but again, future work.
'''

# Function to open a URL
def open_url(driver, target):
    driver.get(target)


# Function to set window size
def set_window_size(driver):
    driver.maximize_window()


# Function to find an element by its id
def find_element(driver, id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id))
        )
        return element
    except Exception as e:
        print(f"Error finding element with ID '{id}': {e}")
        return None

# Function to scroll to an element using a href
def scroll_to_element(driver, href):
    try:
        # Use WebDriverWait to ensure the element is present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{href}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView()", element)


    except Exception as e:
        print(f"Error in scroll_to_element for href '{href}': {e}")


# Function to hover over a href element and click it (ideal for link buttons)
def hover_and_click(driver, href):
    try:
        # Use WebDriverWait to ensure the element is present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{href}']"))
        )
        # Use ActionChains to hover over the element
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

        # Click the element
        element.click()
    except Exception as e:
        print(f"Error in hover_and_click for href '{href}': {e}")


# Function to hover over an href element (ideal for link buttons)
def hover_over_element(driver, href):
    try:
        # Use WebDriverWait to ensure the element is present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{href}']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

    except Exception as e:
        print(f"Error in hover_and_click for href '{href}': {e}")


# Function to click an element using a CSS selector with error handling
def click_element(driver, css_selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with selector '{css_selector}': {e}")


# Function to run the modified Selenium test
def run_selenium_test():
    # Setting up with Chrome options and the ChromeDriver service
    options = Options()
    options.add_argument("usr/bin/google-chrome")

    # Disable the "Chrome is being controlled by automated test software" banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Specify the path to ChromeDriver
    service = Service('/opt/homebrew/bin/chromedriver')

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Main walkthrough logic here divided into steps etc (will hopefully be more legible after future refactors)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    try:
        '''
        Setup Open Tutors.dev and set window size etc
        '''
        set_window_size(driver)
        open_url(driver, "https://tutors.dev")
        time.sleep(2)  # Give the page time to load

        '''
        Step 1 - Open Tutors
        '''
        recording1 = start_ffmpeg_recording("step1.mp4")
        export_gtts("First, let's open tutors.dev. On this page we see the web toolkit, in addition to any courses we may recently have accessed.", "step1.mp3")
        # sleep_based_on_vo("step1.mp3") # removed to test pacing
        stop_ffmpeg_recording(recording1)

        '''
        Step 2 - setting dark mode
        '''
        recording2 = start_ffmpeg_recording("step2.mp4")
        export_gtts("Before we go any further, let's change to dark mode using the layout button in the top right of the screen", "step2.mp3")
        # sleep_based_on_vo("step2.mp3") # removed to test pacing
        # clicking layout button
        click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block")
        time.sleep(2)  # Wait for the navigation to complete
        # clicking the dark mode button
        click_element(driver, "label[data-testid='segment-item']")
        time.sleep(2)  # Wait for the navigation to complete
        # clicking layout button again to close
        click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block")
        stop_ffmpeg_recording(recording2)

        '''
        Step 3 - navigating to the docs page
        '''
        recording3 = start_ffmpeg_recording("step3.mp4")
        export_gtts("Now that we're in dark mode, let's navigate to the docs page by clicking the docs button under the web toolkit", "step3.mp3")
        # sleep_based_on_vo("step3.mp3") # removed to test pacing
        # hovering over and clicking the docs link
        hover_and_click(driver, "/course/tutors-reference-manual")
        # time.sleep(2)
        stop_ffmpeg_recording(recording3)

        '''
        Step 4 - Docs page intro
        '''
        recording4 = start_ffmpeg_recording("step4.mp4")
        export_gtts("On the docs page, we can see a number of cards. Each of these cards leads to a specific portion of the getting started guide.", "step4.mp3")
        # sleep_based_on_vo("step4.mp3") # removed to test pacing
        stop_ffmpeg_recording(recording4)

        '''
        Step 5 - Hovering over the first card
        '''
        recording5 = start_ffmpeg_recording("step5.mp4")
        hover_over_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started")
        export_gtts("The getting started card introduces the basic design model of tutors.", "step5.mp3")
        sleep_based_on_vo("step5.mp3")
        stop_ffmpeg_recording(recording5)

        '''
        Step 6 - Hovering over the second card
        '''
        recording6 = start_ffmpeg_recording("step6.mp4")
        hover_over_element(driver, "/course/tutors-starter-course")
        export_gtts("The simple starter card provides a helpful template course.", "step6.mp3")
        sleep_based_on_vo("step6.mp3")
        stop_ffmpeg_recording(recording6)

        '''
        Step 7 - Hovering over the third card
        '''
        recording7 = start_ffmpeg_recording("step7.mp4")
        hover_over_element(driver, "/course/layout-reference-course")
        export_gtts("The alternative starter card provides an example course to demonstrate layouts and nesting.", "step7.mp3")
        sleep_based_on_vo("step7.mp3")
        stop_ffmpeg_recording(recording7)

        '''
        Step 8 - Hovering over the fourth card
        '''
        recording8 = start_ffmpeg_recording("step8.mp4")
        scroll_to_element(driver, "/course/reference-course")
        hover_over_element(driver, "/course/reference-course")
        export_gtts("The reference course contains another example course. This one contains all Tutors learning objects for demonstration.", "step8.mp3")
        sleep_based_on_vo("step8.mp3")
        stop_ffmpeg_recording(recording8)

        '''
        Step 9 - Retuning to the original card
        '''
        recording9 = start_ffmpeg_recording("step9.mp4")
        scroll_to_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started")
        hover_and_click(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started")
        export_gtts("Finally, let's return to the getting started card and click it to demonstrate the getting started page.", "step9.mp3")
        sleep_based_on_vo("step9.mp3")
        print("End of test")
        stop_ffmpeg_recording(recording9)

    finally:
        print("Test complete -> moving to assembly")
        driver.quit()

# End of walkthrough section
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Main function to run the test and assemble the clips (now passing the number of steps to the assembly function)
if __name__ == "__main__":
    run_selenium_test()
    assemble(9)
