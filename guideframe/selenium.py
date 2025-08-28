from selenium import webdriver  # Importing the webdriver module from selenium and other modules
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

'''
For GUIDEFRAME-15 selenium functionality has been broken out into a separate script
This will aid legibility and also lend itself to the SDK-lite id where we provide a simple
library of functions that are clear to a user but deeper on this side in terms of error-handling etc
Additional functions will be added as they are required before a doc is prepared to outline them
'''

# Function to setup the driver and return it for initialization in main scripts
from shutil import which
import os

def driver_setup(driver_location=None):
    """
    Cross-distro WebDriver bootstrap.
    - Picks a Chromium/Chrome binary from $GUIDEFRAME_BROWSER, or PATH.
    - Picks a chromedriver from arg, $GUIDEFRAME_CHROMEDRIVER, or PATH.
    Raises RuntimeError with actionable guidance if either is missing.
    """
    options = Options()
    options.add_argument("--incognito")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Browser binary (prefer env override)
    binary = (
        os.environ.get("GUIDEFRAME_BROWSER")
        or which("chromium")
        or which("google-chrome-stable")
        or which("google-chrome")
    )
    if binary:
        options.binary_location = binary
    else:
        raise RuntimeError(
            "Chromium/Chrome not found on PATH. Install `chromium` (Fedora) or `google-chrome-stable`, "
            "or set GUIDEFRAME_BROWSER=/full/path/to/browser"
        )

    # Chromedriver location
    drv = (
        driver_location
        or os.environ.get("GUIDEFRAME_CHROMEDRIVER")
        or which("chromedriver")
    )
    if not drv:
        raise RuntimeError(
            "chromedriver not found. On Fedora: `sudo dnf install -y chromedriver`. "
            "Or set GUIDEFRAME_CHROMEDRIVER=/full/path/to/chromedriver"
        )

    service = Service(drv)
    return webdriver.Chrome(service=service, options=options)

# Function to open a URL
def open_url(driver, target):
    driver.get(target)
    # sleep(1)  # Give the page time to load


# Function to set window size
def set_window_size(driver):
    # Try block added for GUIDEFRAME-30
    try:
        driver.maximize_window()
    # If an exception is caught, manually set the window size
    except Exception as e:
        print("Error maximizing window:", e)
        print("Setting window size to 1920x1080")
        driver.set_window_size(1920, 1080)


# Function to find an element by its id
def find_element(driver, id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id))
        )
        return element
    except Exception as e:
        print(f"Error finding element with ID '{id}': {e}")
        raise


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
        raise


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
        raise


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
        print(f"Error in hover_over_element for href '{href}': {e}")
        raise


# Function to click an element using a CSS selector
def click_element(driver, css_selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with selector '{css_selector}': {e}")
        raise


# Function to type into an input field using an ID
def type_into_field(driver, element_id, text):
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        input_field.send_keys(text)
    except Exception as e:
        print(f"Error typing into field with ID '{element_id}': {e}")
        raise


# Function to open a link in a new tab
def open_link_in_new_tab(driver, href):
    try:
        # Open the link in a new tab
        driver.execute_script(f"window.open('{href}', '_blank');")
        
        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])
    except Exception as e:
        print(f"Error opening link '{href}' in a new tab: {e}")
        raise


# Function to switch between browser tabs using index as an arg
def switch_to_tab(driver, tab_index):
    try:
        if 0 <= tab_index < len(driver.window_handles):
            driver.switch_to.window(driver.window_handles[tab_index])
        else:
            print(f"Invalid tab index: {tab_index}")
    except Exception as e:
        print(f"Error switching to tab {tab_index}: {e}")
        raise


# Function to take a screenshot (mainly for testing but could be useful)
def take_screenshot(driver, file_name="screenshot.png"):
    try:
        driver.save_screenshot(file_name)
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        raise


# Function to select a dropdown option by visible text
def select_dropdown_option(driver, dropdown_id, visible_text):
    try:
        dropdown = Select(WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, dropdown_id))
        ))
        dropdown.select_by_visible_text(visible_text)
        print(f"Selected dropdown option: {visible_text}")
    except Exception as e:
        print(f"Error selecting dropdown option '{visible_text}': {e}")
        raise


# Function to click a button by the text of a span element (useful for cookie popups etc)
def click_button_by_span_text(driver, span_text):
    try:
        # XPath to find a button containing a span with the given text
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[span[text()='{span_text}']]"))
        )
        button.click()
        print(f"Clicked button with span text: '{span_text}'")
    except Exception as e:
        print(f"Error clicking button with span text '{span_text}': {e}")
        raise
    
    
# Function to click an element by its XPath
def click_element_by_xpath(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with xpath '{xpath}': {e}")
        raise


# Function to hover over an element by its XPath
def hover_over_element_by_xpath(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
    except Exception as e:
        print(f"Error hovering over element with xpath '{xpath}': {e}")
        raise
    
    
# Function to highlight code on GitHub.com (useful for code walkthroughs)
def highlight_github_code(driver, target):
    driver.get(target)
    driver.refresh() # Refresh the page to ensure the code is highlighted


# Function to sleep for a specified number of seconds (added to negate the need to import time)    
def sleep_for(seconds):
    sleep(seconds)