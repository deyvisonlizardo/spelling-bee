from gtts import gTTS
from playsound import playsound
import os

def say_word(word):
    # Create a gTTS object
    tts = gTTS(text=word, lang='en')
    
    # Use os.path.join to ensure the correct path format across different OS
    file_path = os.path.join("Tests", f"{word}.mp3")

    # Save the speech as a temporary file
    tts.save(file_path)

    # Play the speech
    playsound(file_path)

if __name__ == "__main__":

    for x in range(5):
        word_to_say = input("Enter a word to say: ")
        say_word(word_to_say)