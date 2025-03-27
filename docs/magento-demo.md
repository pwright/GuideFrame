---
title: Magento Demo
layout: default
nav_order: 2
parent: Demos
permalink: /magento-demo/
---

# Code Walkthrough

The below video serves as a demonstration of GuideFrame's Selenium SDK via the Magento test site. The script used to create this can be seen below in addition to its companion markdown.

<div style="padding-bottom:56.25%; position:relative; display:block; width: 100%">
  <iframe width="100%" height="100%"
    src="https://www.youtube.com/embed/O9Mt2SXts-0?si=2XaDCqrkSyge9WHL"
    frameborder="0" allowfullscreen="" style="position:absolute; top:0; left: 0">
  </iframe>
</div>

## GuideFrame Code Walkthrough Script
```python

from guideframe.selenium import * # Importing all functions from selenium_functions.py
from guideframe.assembly import assemble  # Importing the assemble_clips function from assembly.py
from guideframe.utils import get_env_settings, guide_step  # Importing the guide_step and get_env_settings functions from guideframe_utils.py


# This function will run the full script
def selenium_automation_tests():
   try:
       env_settings = get_env_settings()  # Getting the environment settings
       driver_location = env_settings["driver_location"]  # Getting the driver location from the settings
       driver = driver_setup(driver_location)  # Initializing driver
       set_window_size(driver)
       open_url(driver, "https://magento.softwaretestingboard.com/")


       '''
       Step 1 - Open the Magento website
       '''
       guide_step(
           1,
           lambda: None
       )


       '''
       Step 2 - Click the "AGREE" button on the cookies policy
       '''
       guide_step(
           2,
           lambda: click_button_by_span_text(driver, "AGREE")
       )


       '''
       Step 3 - Click the "Sign In" link
       '''
       guide_step(
           3,
           lambda: click_element(driver, ".authorization-link > a")
       )


       '''
       Step 4 - Enter email and password
       '''
       guide_step(
           4,
           lambda: type_into_field(driver, "email", "test-user@email.com"),
           lambda: type_into_field(driver, "pass", "testuser-1")
       )


       '''
       Step 5 - Click the "Sign In" button
       '''
       guide_step(
           5,
           lambda: click_element(driver, "button[name='send']")
       )   


       '''
       Step 6 - Hover over the "Gear" menu
       '''
       guide_step(
           6,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/gear.html")
       )


       '''
       Step 7 - Then, click on "Fitness Equipment"
       '''
       guide_step(
           7,
           lambda: click_element(driver, "a[href='https://magento.softwaretestingboard.com/gear/fitness-equipment.html']")
       )


       '''
       Step 8 - Hover over the yoga companion kit
       '''
       guide_step(
           8,
           lambda: hover_over_element_by_xpath(driver, '//*[@id="maincontent"]/div[3]/div[1]/div[3]/ol/li[1]/div/a/span/span/img')
       )


       '''
       Step 9 - Hover over the "Yoga Straps" product
       '''
       guide_step(
           9,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html")
       )


       '''
       Step 10 - Hover over the strength band kit
       '''
       guide_step(
           10,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html")
       )


       '''
       Step 11 - Return to the straps and click on them
       '''
       guide_step(
           11,
           lambda: hover_and_click(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html")
       )


       '''
       Step 12 - Hover over the reviews link
       '''
       guide_step(
           12,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html#review-form")
       )


       '''
       Step 13 - Open the reviews link in a new tab
       '''
       guide_step(
           13,
           lambda: open_link_in_new_tab(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html#review-form")
       )


       '''
       Step 14 - Enter the nickname, summary, and review
       '''
       guide_step(
           14,
           lambda: type_into_field(driver, "nickname_field", "Test User"),
           lambda: type_into_field(driver, "summary_field", "Great product!"),
           lambda: type_into_field(driver, "review_field", "I love this product!")
       )


       '''
       Step 15 - Submit the review
       '''
       guide_step(
           15,
           lambda: click_button_by_span_text(driver, "Submit Review")
       )


       '''
       Step 16 - Return to the first tab
       '''
       guide_step(
           16,
           lambda: switch_to_tab(driver, 0)
       )


       '''
       Step 17 - Click the dropdown next to user name
       '''
       guide_step(
           17,
           lambda: click_button_by_span_text(driver, "Change")
       )


       '''
       Step 18 - Click the "Log Out" button
       '''
       guide_step(
           18,
           lambda: click_element(driver, "a[href='https://magento.softwaretestingboard.com/customer/account/logout/']")
       )


   finally:   
       print("Script complete -> moving to assembly")
       driver.quit()


# Run the automation test
if __name__ == "__main__":
   selenium_automation_tests()
   assemble(18)
```

## GuideFrame Code Walkthrough Markdown

```markdown
## Step 1
This video serves as a demonstration of guideframe's use of selenium functions. We'll achieve this via the Magneto testing site.


## Step 2
Here, we can demonstrate the function which takes a buttons span text as an argument. In this case, we can click on the agree button within the cookie policy popup.


## Step 3
We can use the click element function by passing in the elements I D. Let's use that to sign in.


## Step 4
We can use the form fields here to demonstrate the type into fields function, which takes the element I D and the text you wish to pass as arguments.


## Step 5
Now that we've filled the form, we can use the click element function again to sign in with these credentials.


## Step 6
Next, we'll demonstrate the hover over element function by hovering over the gear dropdown in the navbar. This function takes an h ref as an argument. It is then used in an X path filter to locate the appropriate element.


## Step 7
We'll once again use the click element function to select the fitness equipment link.


## Step 8
Now we'll hover over the yoga companion kit using the same hovering function.


## Step 9
Then we can move on to hover over the yoga straps.


## Step 10
Then the strength band kit.


## Step 11
Before returning to the yoga straps, this time using the hover and click function in order to first hover, then click on the link.


## Step 12
Next, let's hover over the reviews section on the product page.


## Step 13
We can use the open link in new tab function here to open the reviews section in a new tab and switch to it.


## Step 14
Let's enter some text here using the same function for fields that we did earlier.


## Step 15
Now we can click on the submit review button using the same functionality we've been using throughout.


## Step 16
We can use the switch to tab function to return to the original tab by passing the tab index as an argument.


## Step 17
Now that we're on the original tab, let's click the dropdown in the top right of the screen. We do this by using the click on button via span text function once again.


## Step 18
Finally, let's click the sign out button to end this demonstration.
```
