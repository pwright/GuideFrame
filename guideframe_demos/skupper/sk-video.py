from guideframe.selenium import *  # selenium helpers
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""markdown
## Step 1
Skupper is a powerful layer 7 service interconnect. With Skupper, you can easily connect your applications across platforms and regions, ensuring secure communication no matter where you have them running. To get a better grasp of how it works, we'll set up a distributed system with components that aren't accessible from the outside.

Let's dive in. A company located in North America uses a public cloud provider to run their applications in a Kubernetes cluster. They need to run a front-end application on a particular namespace in this cluster. But for this application to work, it needs access to a payment processor microservice and to a database. But those are currently running on private networks.

The payment processor microservice runs on a private cloud provider in Europe and it's not public. The database is running on a bare metal Linux machine in South America. What's great about Skupper is that it doesn't require network changes, making it incredibly simple and easy to test out and integrate with your applications.

To install it in your Kubernetes cluster, all you need to do is just apply the install YAML which is available on the Skupper website. The Skupper controller watches all namespaces in your cluster for a set of custom resources and the most relevant ones are the site resource - it's the main and mandatory one.

When a site is created, the Skupper controller creates a Skupper router instance in the same namespace. The Skupper router is the core component that links your sites and routes all the traffic between the apps in your virtual application network or VAN.

Listeners are used to provide access to workloads exposed through the VAN. In a Kubernetes cluster, a service will be created to allow apps to communicate with exposed workloads. Connectors are used to expose workloads into the VAN so that they are accessible to other sites that have a corresponding listener. Listeners and connectors will match based upon the provided routing key which is just an arbitrary string.

Let's explore which resources are needed in each region. Starting with North America, the first resource needed is the site. Once a site is created, an instance of Skupper router will be created by the controller into the namespace. Then we need two listeners, one to the payment processor microservice and one to the database. Once the listeners are processed by the controller, Kubernetes services will be created into the namespace for each one.

Moving on to Europe, we need to have a site resource and we also need a connector that points to the payment processor pods. Once the connector is processed by the controller, the payment processor microservice is exposed into the VAN. Whether you are using Kubernetes or working outside of Kubernetes with Podman, Docker or even a bare metal Linux machine, Skupper has you covered.

That is the case for the database we have running in South America. It's running on a bare metal Linux machine. Similarly, we can create our resources on the file system and use the available Skupper tooling to run your Skupper site outside of Kubernetes. To expose the database into the VAN, we need a site and a connector that points to the IP and port of the database server.

At this point, the sites are individually configured, but they're not linked yet. Let's connect the Skupper network. First, we need to create a token to the public cloud cluster in North America. To do that, we create a resource named access grant. The controller processes the access grant definition and generates an access token.

Then we need to apply these access tokens into the other two sites. Skupper processes the access tokens on those sites creating a mutual TLS connection with the North America site ensuring a secure communication between the sites. Once the links are established, the VAN is working and the exposed workloads are available to the front end.

And this is how easy Skupper works. I hope you found this useful and that you're ready to start your Skupper journey.
"""

def handle_youtube_consent(driver):
    """Handle YouTube consent popups with robust timing and multiple strategies"""
    print("Looking for YouTube consent popups...")
    
    consent_found = False
    max_attempts = 5
    
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
            
            # Strategy 1: Look for the exact button with the specific class and aria-label
            try:
                accept_button = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Accept the use of cookies and other data for the purposes described']"))
                )
                print("Found 'Accept all' button via exact aria-label")
            except:
                pass
            
            # Strategy 2: Look for button with the specific class structure
            if not accept_button:
                try:
                    accept_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.yt-spec-button-shape-next--filled[aria-label*='Accept']"))
                    )
                    print("Found Accept button via class and aria-label")
                except:
                    pass
            
            # Strategy 3: Look for "Accept all" text in the button span
            if not accept_button:
                try:
                    accept_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button//span[contains(text(), 'Accept all')]/ancestor::button"))
                    )
                    print("Found 'Accept all' button via span text")
                except:
                    pass
            
            # Strategy 4: Look for any button in the consent dialog with Accept text
            if not accept_button:
                try:
                    buttons = consent_dialog.find_elements(By.TAG_NAME, "button")
                    print(f"Found {len(buttons)} buttons in consent dialog")
                    for button in buttons:
                        try:
                            # Check button text content
                            text_content = button.find_element(By.CSS_SELECTOR, ".yt-spec-button-shape-next__button-text-content")
                            if text_content and "Accept all" in text_content.text:
                                accept_button = button
                                print(f"Found Accept button via button text content: {text_content.text}")
                                break
                        except:
                            # Check direct button text
                            if "Accept all" in button.text:
                                accept_button = button
                                print(f"Found Accept button via direct text: {button.text}")
                                break
                except Exception as e:
                    print(f"Strategy 4 failed: {e}")
            
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
                time.sleep(3)
    
    if consent_found:
        print("Consent handled successfully, waiting for page to load...")
        time.sleep(5)
        return True
    else:
        print("ERROR: Could not find or click Accept button!")
        return False

def go_fullscreen(driver):
    """Go full screen on video player"""
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
        time.sleep(3)
        
        # Verify we're in full screen
        is_fullscreen = driver.execute_script("return document.fullscreenElement !== null")
        if is_fullscreen:
            print("SUCCESS: Video is now in full screen mode!")
            return True
        else:
            print("WARNING: May not be in full screen mode")
            return False
            
    except Exception as e:
        print(f"ERROR: Could not go full screen: {e}")
        return False

def guideframe_script():
    driver = None
    try:
        # Setup
        env = get_env_settings()
        driver_location = env["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)
        
        # Step 1 - Play maximized YouTube video
        guide_step(
            1,
            lambda: open_url(driver, "https://www.youtube.com/watch?v=pm8OP9bG2mU"),
            order="action-before-vo",
        )
        
        # Wait for page to load and handle consent popups
        print("Waiting for page to load...")
        sleep_for(8)  # Increased wait time for page load
        
        # Handle YouTube consent popups with robust timing and multiple strategies
        if handle_youtube_consent(driver):
            print("YouTube consent handled successfully")
            
            # Now go full screen
            if go_fullscreen(driver):
                print("Full screen mode activated")
            else:
                print("Could not activate full screen mode")
        else:
            print("Failed to handle YouTube consent, proceeding anyway...")
        
        # Wait for voiceover to complete (approximately 6 minutes)
        print("Waiting for voiceover to complete (6 minutes)...")
        time.sleep(360)  # 6 minutes = 360 seconds
        
    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(1)
