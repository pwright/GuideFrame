import subprocess # Importing the subprocess module for running FFmpeg
import threading # Importing the threading module (not currently using it but likely will)
from selenium import webdriver # Importing the webdriver module from selenium and other modules
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gtts import gTTS # Importing gTTS for audio generation (opensource based on Google translate API)
from mutagen.mp3 import MP3 # Importing the MP3 module from mutagen for audio length checking
import time # Importing the time module for sleep functions
import os # Importing the os module for file operations (was using, likely will again but not in this commit)

# Initial test script to verify threading the video concept.

'''
Pivoting to gTTS
This has a significantly simpler design in terms of saving clips so it better serves this need that pytts
It also sounds generally better and easily fulfills the intended logic in terms of clip generation for later splicing
Leaving pytts in for now until clip assembly logic is in place.
'''
def export_gtts(text, file_name):
    tts = gTTS(text)
    tts.save(file_name)
    print("Exported", file_name)

# Function to check the length of an audio clip and then sleep based on it
def sleep_based_on_vo(file_name):
    audio = MP3(file_name)
    print("Sleeping for", audio.info.length, "seconds")
    time.sleep(audio.info.length)

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
        '-framerate', '30.000000',      # Frame rate; increase for smoother video
        '-b:v', '3000k',                # Set bitrate for better quality
        '-pix_fmt', 'yuv420p',          # Pixel format
        output_file                     # Output file
    ]
    
    # Start the FFmpeg process (Popen allows communication via stdin)
    return subprocess.Popen(command, stdin=subprocess.PIPE)

# Function to stop FFmpeg recording
def stop_ffmpeg_recording(process):
    process.stdin.write(b"q\n")  # Gracefully stop FFmpeg by sending 'q' to stdin as a byte string
    process.communicate()       # Wait for process to finish (again, this is to prevent carry over or timing errors)

# Function to run the test with segmented video recording (refactored for this ticket as explained below)
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

    '''
    Extensive refactor below in order to render invidual steps as video clips
    FFMPEG is started and stopped in each step in order to render a single video in parallel
    with the audio generation. This is obviously inelegant but will serve to build towards a simple
    demo for interim report.

    Each of the below steps will render a video and audio clip respectively, then sleep based on the
    length of the audio clip. This will allow for the video clips to be spliced together in a later step.
    This will obviously require some finessing but will serve for now.
    '''
    try:
        # Step 1 - Start recording
        recording1 = start_ffmpeg_recording("step1.mp4")
        set_window_size(driver)
        stop_ffmpeg_recording(recording1)

        # Step 2 - Open Wikipedia
        recording2 = start_ffmpeg_recording("step2.mp4")
        export_gtts("First, open wikipedia.org", "step2.mp3")
        sleep_based_on_vo("step2.mp3")
        open_url(driver, "/")
        stop_ffmpeg_recording(recording2)

        # Step 3 - Type "Red Hat" into the search bar
        recording3 = start_ffmpeg_recording("step3.mp4")
        export_gtts("Next, type Red Hat into the search bar", "step3.mp3")
        sleep_based_on_vo("step3.mp3")
        type_into_field(driver, "searchInput", "Red Hat")
        stop_ffmpeg_recording(recording3)

        # Step 4 - Click the suggested text
        recording4 = start_ffmpeg_recording("step4.mp4")
        try:
            export_gtts("Click the suggested text", "step4.mp3")
            sleep_based_on_vo("step4.mp3")
            suggestion = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".suggestion-text"))
            )
            suggestion.click()
        except Exception as e:
            print(f"Error clicking suggestion: {e}")
        stop_ffmpeg_recording(recording4)

        # Step 5 - Click the Fedora Project link
        recording5 = start_ffmpeg_recording("step5.mp4")
        export_gtts("Now click on the Fedora Project link", "step5.mp3")
        sleep_based_on_vo("step5.mp3")
        click_element(driver, ".hatnote:nth-child(39) > a")
        stop_ffmpeg_recording(recording5)

    # End
    finally:
        print("Test complete")
        driver.quit()

if __name__ == "__main__":
    # Run the function
    run_selenium_test()