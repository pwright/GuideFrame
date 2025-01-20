import subprocess
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyttsx3  # Import the TTS library
import time
import os

# Initial test script to verify threading the video concept.
# This will be expanded with some form of TTS next.
# Testing branch configuration with Jira.

engine = pyttsx3.init()  # Initialize the TTS engine
audio_dir = "tts_audio"  # Directory to store TTS audio files

def export_tts(text, filename):
    audio_path = os.path.join(audio_dir, filename)
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    return audio_path

# Function to open a URL
def open_url(driver, target):
    driver.get("https://www.wikipedia.org" + target)

# Function to set window size
def set_window_size(driver):
    driver.maximize_window()
    
# Function to click an element using a CSS selector with error handling
def click_element(driver, css_selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with selector '{css_selector}': {e}")

# Function to type into an input field using an ID with error handling
def type_into_field(driver, element_id, text):
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        input_field.send_keys(text)
    except Exception as e:
        print(f"Error typing into field with ID '{element_id}': {e}")

# Function to start FFmpeg to record the screen
def start_ffmpeg_recording(output_file):
    # Command to start recording using FFmpeg
    command = [
        'ffmpeg',
        '-f', 'avfoundation',           # Capture avfoundation
        '-video_size', '1920x1080',     # Set resolution; consider using '$(xdpyinfo | grep dimensions)' for dynamic resolution
        '-i', '1',                      # Input display (change this if necessary)
        '-c:v', 'libxvid',              # Video codec
        '-preset', 'fast',              # Preset for encoding speed
        '-framerate', '30',             # Frame rate; increase for smoother video
        '-b:v', '3000k',                # Set bitrate for better quality
        '-pix_fmt', 'yuv420p',          # Pixel format
        output_file                     # Output file
    ]
    
    # Start the FFmpeg process
    return subprocess.Popen(command)

# Function to run the entire test sequence
def run_selenium_test():
    # Set up Chrome options with the user profile
    options = Options()
    options.add_argument("usr/bin/google-chrome") 

    # Disable the "Chrome is being controlled by automated test software" banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Specify the path to ChromeDriver
    service = Service('/opt/homebrew/bin/chromedriver')

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Step 1: Set window size
        set_window_size(driver)

        # Step 2: Open URL
        open_url(driver, "/")
        engine.say("First, open wikipedia.org")
        engine.runAndWait()

        time.sleep(5)

        # Step 3: Type "Red Hat" into the search input
        engine.say("Next, type Red Hat into the search bar")
        type_into_field(driver, "searchInput", "Red Hat")

        # Step 4: Wait for the suggestion list to appear, then click the first suggestion
        try:
            suggestion = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".suggestion-text"))
            )
            engine.say("Click the suggested text")
            engine.runAndWait()
            suggestion.click()

            time.sleep(5)

        except Exception as e:
            print(f"Error clicking suggestion: {e}")

        # Step 5: Click the link for "Fedora Project"
        engine.say("Now click on the Fedora Project link")
        engine.runAndWait()
        click_element(driver, ".hatnote:nth-child(39) > a")
        time.sleep(10)

    finally:
        engine.say("Guide complete")
        engine.runAndWait()
        print("Test complete")

if __name__ == "__main__":
    output_file = "screen_recording.mp4"
    
    # Start FFmpeg recording in a separate thread
    ffmpeg_process = threading.Thread(target=start_ffmpeg_recording, args=(output_file,))
    ffmpeg_process.start()

    try:
        run_selenium_test()
    finally:
        # Stop FFmpeg process
        subprocess.call(['pkill', 'ffmpeg'])
        ffmpeg_process.join()
