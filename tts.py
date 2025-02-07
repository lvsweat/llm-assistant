import os
import edge_tts
from playsound import playsound


TEXT = "Hello World!"
VOICE = "en-US-EmmaMultilingualNeural"
OUTPUT_FILE = "response.mp3"


def say(text: str):
    """
    Downloads tts audio file of provided text and plays it

    Args:
        text (string): The text to be read through tts
    """

    comms = edge_tts.Communicate(text, VOICE) # Get edge tts data
    comms.save_sync(OUTPUT_FILE) # Save tts data to audio file
    playsound(OUTPUT_FILE) # Play the audio from the saved tts data file
    os.remove(OUTPUT_FILE) # Delete the now unneeded tts audio file to avoid file access permissions clash