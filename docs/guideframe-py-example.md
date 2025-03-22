---
title: GuideFrame Script Example
layout: default
nav_order: 1
parent: Samples
permalink: /guideframe-py-example/
---

# GuideFrame Script Example

```python
from guideframe.selenium import * # Importing all functions from selenium_functions.py
from guideframe.assembly import assemble  # Importing the assemble_clips function from assembly.py
from guideframe.utils import get_env_settings, guide_step  # Importing the guide_step and get_env_settings functions from guideframe_utils.py


# This function will run the full script
def guideframe_demo_script():
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
       Step 2 - Click the "Sign In" link
       '''
       guide_step(
           2,
           lambda: click_element(driver, ".authorization-link > a")
       )


       '''
       Step 3 - Enter email and password
       '''
       guide_step(
           3,
           lambda: type_into_field(driver, "email", "test-user@email.com"),
           lambda: type_into_field(driver, "pass", "testuser-1")
       )


       '''
       Step 4 - Click the "Sign In" button
       '''
       guide_step(
           4,
           lambda: click_element(driver, "button[name='send']")
       )   


       '''
       Step 5 - Hover over the "Gear" menu
       '''
       guide_step(
           5,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/gear.html")
       )


       '''
       Step 6 - Then, click on "Fitness Equipment"
       '''
       guide_step(
           6,
           lambda: click_element(driver, "a[href='https://magento.softwaretestingboard.com/gear/fitness-equipment.html']")
       )


       '''
       Step 7 - Hover over the yoga companion kit
       '''
       guide_step(
           7,
           lambda: hover_over_element_by_xpath(driver, '//*[@id="maincontent"]/div[3]/div[1]/div[3]/ol/li[1]/div/a/span/span/img')
       )


       '''
       Step 8 - Hover over the "Yoga Straps" product
       '''
       guide_step(
           8,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html")
       )


       '''
       Step 9 - Hover over the strength band kit
       '''
       guide_step(
           9,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html")
       )


       '''
       Step 10 - Return to the straps and click on them
       '''
       guide_step(
           10,
           lambda: hover_and_click(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html")
       )


       '''
       Step 11 - Hover over the reviews link
       '''
       guide_step(
           11,
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html#review-form")
       )


       '''
       Step 12 - Open the reviews link in a new tab
       '''
       guide_step(
           12,
           lambda: open_link_in_new_tab(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html#review-form")
       )


       '''
       Step 13 - Enter the nickname, summary, and review
       '''
       guide_step(
           13,
           lambda: type_into_field(driver, "nickname_field", "Test User"),
           lambda: type_into_field(driver, "summary_field", "Great product!"),
           lambda: type_into_field(driver, "review_field", "I love this product!")
       )


       '''
       Step 14 - Submit the review
       '''
       guide_step(
           14,
           lambda: click_button_by_span_text(driver, "Submit Review")
       )


       '''
       Step 15 - Return to the first tab
       '''
       guide_step(
           15,
           lambda: switch_to_tab(driver, 0)
       )


       '''
       Step 16 - Click the dropdown next to user name
       '''
       guide_step(
           16,
           lambda: click_button_by_span_text(driver, "Change")
       )


       '''
       Step 17 - Click the "Log Out" button
       '''
       guide_step(
           17,
           lambda: click_element(driver, "a[href='https://magento.softwaretestingboard.com/customer/account/logout/']")
       )


   finally:   
       print("Script complete -> moving to assembly")
       driver.quit()


# Run the demo script and then use the assemble function
if __name__ == "__main__":
   guideframe_demo_script()
   assemble(17)
```