from gtts import gTTS # Importing gTTS for audio generation (opensource based on Google translate API)
from mutagen.mp3 import MP3 # Importing the MP3 module from mutagen for audio length checking
import time 

'''
Pivoting to gTTS
This has a significantly simpler design in terms of saving clips so it better serves this need that pytts
It also sounds generally better and easily fulfills the intended logic in terms of clip generation for later splicing
Leaving pytts in for now until clip assembly logic is in place.
'''

# Function to create the gTTS speech clips. Takes the text arg passed by the user and a file name to write it to
def export_gtts(text, file_name):
    tts = gTTS(text)
    tts.save(file_name)
    print("Exported", file_name)


# Function to check the length of an audio clip and then sleep based on it
def sleep_based_on_vo(file_name):
    audio = MP3(file_name)
    print("Sleeping for", audio.info.length, "seconds")
    time.sleep(audio.info.length)