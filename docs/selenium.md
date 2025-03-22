---
title: Selenium
layout: default
nav_order: 4
parent: Library
permalink: /selenium/
---

# Selenium
The selenium file contains functions designed to perform the various UI-based interactions specified in a GuideFrame step. The functions act as an SDK-lite, providing an abstraction layer to users who wish to avoid more escoteric `selenium` commands. The following section will list each function contained within this file and provide some insight into its use and syntax.


`driver_setup()`
```python
def driver_setup(driver_location):
    # Setting up with Chrome options and the ChromeDriver service
    options = Options()
    options.add_argument("usr/bin/google-chrome")
    options.add_argument("--incognito")

    # Disable the "Chrome is being controlled by automated test software" banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Specify the path to ChromeDriver
    service = Service(driver_location) 

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    return driver
```
This function takes the `driver_location` variable extracted by `get_env_settings()` in utils. The function then adds numerous `selenium` options in to provide the optimum setup for GuideFrame. This includes using incognito mode to avoid password saving prompts and disabling the chrome banner stating the use of automation in the session. Once the various options have been set, the function returns the `driver` which will be used as an argument in all of the below functions.


### `open_url()`
```python
def open_url(driver, target):
    driver.get(target)
```
This function simply takes the `driver` and a url as arguments. It then opens the passed url in the browser.


### `set_window_size()`
```python
def set_window_size(driver):
    # Try block to account for potential driver issues
    try:
        driver.maximize_window()
    # If an exception is caught, manually set the window size
    except Exception as e:
        print("Error maximizing window:", e)
        print("Setting window size to 1920x1080")
        driver.set_window_size(1920, 1080)
```
This function uses the `driver` as an argument and then uses the requisite `selenium` command to maximise the browser window, ensuring a full screen representation of the session. It includes a try block to account for potential errors due to `chromedriver` updates. Should the initial command fail, it will fall back to using a 1920x1080 pixel count.


### `find_element()`
```python
def find_element(driver, id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id))
        )
        return element
    except Exception as e:
        print(f"Error finding element with ID '{id}': {e}")
        raise
```
This function takes the `driver` and an elements `id` as arguments. It then uses `selenium` functions to wait for the element to appear. This is wrapped in a try block ensuring that if an element is not found with a matching `id`, then an exception is raised.


### `scroll_to_element()`
```python
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
```
This function takes the `driver` and a `href` as arguments. It once again uses `selenium` functions to wait for the presence of an element. In this case however, an xpath filter is used to find the element by its `href`. Once this has occured, the `selenium` functions to scroll to an element are invoked with the result of the xpath check passed.


### `hover_and_click()`
```python
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
```
This function once again takes a `driver` and `href` as arguments. It uses the same logic as the previous function to find the element by the `href` but in this case, `selenium` is invoked to perform the `move_to_element` interaction. Once this has occured, the element is clicked.


### `hover_over_element()`
```python
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
```
This function is identical to the previous one with the exception that it doesn't click the element. Useful for highlight a linked button etc without following through on the click.

### `click_element()`
```python
def click_element(driver, css_selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with selector '{css_selector}': {e}")
        raise
```
This function uses similar logic to the `find_element()` function with the exception of adding a click to the sequence and using a `css_selector` rather than an `id` to locate the element. This is useful for situations where an `id` may not be static.


### `type_into_field()`
```python
def type_into_field(driver, element_id, text):
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        input_field.send_keys(text)
    except Exception as e:
        print(f"Error typing into field with ID '{element_id}': {e}")
        raise
```
This function uses the same element-locating logic seen throughout this file with the addition of a call to the `selenium` function, `send_keys` where the `text` argument from this function is passed.


### `open_link_in_new_tab()`
```python
def open_link_in_new_tab(driver, href):
    try:
        # Open the link in a new tab
        driver.execute_script(f"window.open('{href}', '_blank');")
        
        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])
    except Exception as e:
        print(f"Error opening link '{href}' in a new tab: {e}")
        raise
```
This function takes the `driver` and a `href` as an argument. It uses the `execute_script()` function within selenium to pass script arguments. In this case a window is opened using the passed `href`. The `switch_to.window()` function from `selenium` is then called where it takes the most recently opened tab as an argument. This is found using the size of the `window_handles` array and subtracting 1 to find the most recently opened window.


### `switch_to_tab()`
```python
def switch_to_tab(driver, tab_index):
    try:
        if 0 <= tab_index < len(driver.window_handles):
            driver.switch_to.window(driver.window_handles[tab_index])
        else:
            print(f"Invalid tab index: {tab_index}")
    except Exception as e:
        print(f"Error switching to tab {tab_index}: {e}")
        raise
```
This function takes the `driver` and `tab_index` as arguments. The user simply needs to specify which index of the array of open tabs they wish to switch to. This is wrapped in conditional logic to ensure an invalid index isn't provided. The `window_handles()` function is then called with `tab_index` passed in order to open the correct tab.


### `take_screenshot()`
```python
def take_screenshot(driver, file_name="screenshot.png"):
    try:
        driver.save_screenshot(file_name)
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        raise
```
This function takes the `driver` and a `file_name` as arguments. It has a default of "screenshot.png". It uses `selenium` to take a screenshot and use the argument to name the file.


### `select_dropdown_option()`
``` python
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
```
This function takes the `driver`, `dropdown_id` and `visible_text` as arguments. It uses `selenium` logic to ensure that the element is clickable before using the `select_by_visible_text()` function to click on a dropdown option with text matching the functions argument.


### `click_button_by_span_text()`
```python
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
```
This function uses similar logic to other clicking functions but in this case uses an xpath filter to locate an element by the `span_text` argument passed to the function. This is useful for buttons in particular or other elements with static span text.


### `click_element_by_xpath()`
```python
def click_element_by_xpath(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with xpath '{xpath}': {e}")
        raise
```
This function is similar to other outlined throughout this document except that it takes an `xpath` as an argument. This allows a user to simply use a browser's `inspect` feature to select an element, right click and then select `copy xpath`. This can then be passed to this function.


### `hover_over_element_by_xpath()`
```python
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
```
This function, similar to the above example, is similar to the other hovering functions with the exception of using `xpath` to locate elements. As above, this streamlines the user experience in terms of locating elements in the browser prior to GuideFrame script creation.


### `highlight_github_code()`
```python
def highlight_github_code(driver, target):
    driver.get(target)
    driver.refresh()
```
This function matchess the `open_url()` function but refreshes the page once it's opened. This occurs to allow the user to pass GitHub urls with line numbers for code walkthroughs. By default, when on a GitHub page, adding the line numbers to the url will not move to the requisite line. A refresh is required, hence this implementation.


### `sleep_for()`
```python
def sleep_for(seconds):
    sleep(seconds)
```
This function exists to keep all GuideFrame interaction functionality contained within one file. It uses `time.sleep()` to take the `seconds` argument and sleep for the duration. This function can be called using `lambda` in a `guide_step()` call. This allows a user to inject customized waits between GuideFrame actions.
