from selenium_functions import * # Importing all functions from selenium_functions.py
from assembly import assemble  # Importing the assemble_clips function from assembly.py
from guideframe_utils import get_env_settings, guide_step  # Importing the guide_step and get_env_settings functions from guideframe_utils.py


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
           lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/sprite-yoga-companion-kit.html")
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