from guideframe.selenium import *
from guideframe.utils import get_env_settings  # Importing the guide_step and get_env_settings functions from guideframe_utils.py
import time

# Setup the driver and perform automation tests
def selenium_automation_tests():
    try:
        # Getting the environment settings
        env_settings = get_env_settings()  
        driver_location = env_settings["driver_location"]  # Getting the driver location from the settings
        driver = driver_setup(driver_location)  # Initializing driver
        
        # Set window size and navigate to URL
        set_window_size(driver)
        open_url(driver, "https://magento.softwaretestingboard.com/")
        time.sleep(2)
        
        '''
        # Removing this as cookie is not present in github runner environment
        click_button_by_span_text(driver, "AGREE")
        time.sleep(2)
        '''

        # Click on the 'Sign In' link
        click_element(driver, ".authorization-link > a")
        time.sleep(2)
        
        # Enter email and password
        type_into_field(driver, "email", "test-user@email.com")
        type_into_field(driver, "pass", "testuser-1")
        
        # Click the sign-in button
        click_element(driver, "button[name='send']")
        time.sleep(3)

        # First, hover over the "Gear" menu
        hover_over_element(driver, "https://magento.softwaretestingboard.com/gear.html")
        time.sleep(2)

        # Then, click on "Fitness Equipment"
        click_element(driver, "a[href='https://magento.softwaretestingboard.com/gear/fitness-equipment.html']")
        time.sleep(2)

        # Hover over the yoga straps product
        hover_over_element(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html")
        time.sleep(2)

        # Return to the straps product and click on it
        hover_and_click(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html")
        time.sleep(2)

        # Hover over the reviews link
        hover_over_element(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html#reviews")
        time.sleep(2)

        # Open the reviews link in a new tab
        open_link_in_new_tab(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html#reviews")
        time.sleep(2)
        
        # Fill review fields
        type_into_field(driver, "nickname_field", "Test User")
        type_into_field(driver, "summary_field", "Great product!")
        type_into_field(driver, "review_field", "I love this product!")
        time.sleep(2)

        # Submit the review
        click_button_by_span_text(driver, "Submit Review")
        time.sleep(2)

        # Return to the first tab
        switch_to_tab(driver, 0)
        time.sleep(2)

        # Click the user dropdown
        click_button_by_span_text(driver, "Change")
        time.sleep(2)

        # Click the "Sign Out" button
        click_element(driver, "a[href='https://magento.softwaretestingboard.com/customer/account/logout/']")
        time.sleep(2)
        
        print("Test Passed ✅")  # Print the success message
        exit_code = 0  # Set the exit code to 0

    except Exception as e:
        # print the failure message
        print(f"Test Failed ❌: {str(e)}")
        exit_code = 1  # Set the exit code to 1
        raise
    
    finally:
        driver.quit()
        exit(exit_code)

# Run the automation test
if __name__ == "__main__":
    selenium_automation_tests()
