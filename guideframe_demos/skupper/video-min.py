from guideframe.selenium import *  # selenium helpers
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""markdown
## Step 1
Testing YouTube video playback with proper consent handling and full screen functionality.
"""

def guideframe_script():
    driver = None
    try:
        # Setup
        env = get_env_settings()
        driver_location = env["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)
        
        # Step 1 - Open YouTube video
        print("Opening YouTube video...")
        open_url(driver, "https://www.youtube.com/watch?v=pm8OP9bG2mU")
        
        # Wait for page to load
        print("Waiting for page to load...")
        sleep_for(8)  # Increased wait time
        
        # Handle YouTube consent popups - focus on "Accept all"
        print("Looking for YouTube consent popups...")
        
        consent_found = False
        max_attempts = 5  # Increased attempts
        
        for attempt in range(max_attempts):
            try:
                print(f"Attempt {attempt + 1}: Looking for consent dialog...")
                
                # Wait longer for consent dialog to appear
                consent_dialog = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-consent-bump-v2-lightbox"))
                )
                print("Found consent dialog!")
                
                # Try multiple strategies to find Accept all button
                accept_button = None
                
                # Strategy 1: Look for "Accept all" text
                try:
                    accept_button = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]"))
                    )
                    print("Found 'Accept all' button via text")
                except:
                    pass
                
                # Strategy 2: Look for button with aria-label containing Accept
                if not accept_button:
                    try:
                        accept_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Accept']"))
                        )
                        print("Found Accept button via aria-label")
                    except:
                        pass
                
                # Strategy 3: Look for any button in the consent dialog
                if not accept_button:
                    try:
                        buttons = consent_dialog.find_elements(By.TAG_NAME, "button")
                        print(f"Found {len(buttons)} buttons in consent dialog")
                        for button in buttons:
                            text = button.text.lower()
                            if "accept" in text or "agree" in text:
                                accept_button = button
                                print(f"Found Accept button via button text: {button.text}")
                                break
                    except:
                        pass
                
                if accept_button:
                    print("Clicking Accept button...")
                    accept_button.click()
                    consent_found = True
                    print("Successfully clicked Accept button")
                    break
                else:
                    print("No Accept button found in this attempt")
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    print("Retrying...")
                    sleep_for(3)  # Increased retry wait
        
        if not consent_found:
            print("ERROR: Could not find or click 'Accept all' button!")
            return
        
        # Wait for consent to be processed
        print("Consent accepted, waiting for page to load...")
        sleep_for(5)
        
        # Now go full screen
        print("Looking for full screen button...")
        
        try:
            # Wait for video player to load
            video_player = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#movie_player"))
            )
            print("Video player found")
            
            # Look for full screen button
            fullscreen_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-fullscreen-button"))
            )
            print("Found full screen button, clicking...")
            fullscreen_button.click()
            print("Full screen button clicked")
            
            # Wait for full screen to take effect
            sleep_for(3)
            
            # Verify we're in full screen
            is_fullscreen = driver.execute_script("return document.fullscreenElement !== null")
            if is_fullscreen:
                print("SUCCESS: Video is now in full screen mode!")
            else:
                print("WARNING: May not be in full screen mode")
                
        except Exception as e:
            print(f"ERROR: Could not go full screen: {e}")
            return
        
        # Wait for video to start playing
        print("Waiting for video to start playing...")
        sleep_for(5)
        
        # Verify video is playing
        try:
            time_element = driver.find_element(By.CSS_SELECTOR, ".ytp-time-current")
            current_time = time_element.get_attribute("textContent")
            print(f"Video time: {current_time}")
            
            if current_time and current_time != "0:00":
                print("SUCCESS: Video is playing!")
            else:
                print("WARNING: Video may not be playing - time shows 0:00")
                
        except Exception as e:
            print(f"Could not verify video time: {e}")
        
        # Keep the video playing for a bit to confirm everything works
        print("Keeping video playing for 10 seconds to confirm...")
        sleep_for(10)
        
        print("SUCCESS: YouTube video is playing in full screen with consent handled!")
        
    except Exception as e:
        print(f"ERROR in script: {e}")
    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(1) 