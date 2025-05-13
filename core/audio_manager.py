"""
audio_manager.py

This module handles word pronunciation using gTTS and playback using pygame.
It can generate audio files for words and play them, ensuring thread safety
and caching generated audio to disk.

Functions:
- pronounce_word: Generate/play pronunciation for a word
- play_notification_sound: Play a notification sound
"""

import os
import threading
import time
import pygame
from gtts import gTTS
from .word_manager import sanitize_filename

# Paths
base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
audios_path = os.path.join(base_path, "audios")

audio_lock = threading.Lock()


def pronounce_word(word, logger=None, disable_buttons=None):

    """
    Plays or generates audio for the given word using gTTS and pygame.

    Args:
        word (str): The word to pronounce.
        logger (object, optional): Logger object with a `.log()` method.
        disable_buttons (callable, optional): Function to toggle UI buttons.
    """

    if not word:
        if logger:
            logger.log("⚠️ No word to pronounce.")
        return

    def play_audio():
        safe_word = sanitize_filename(word)
        audio_file = os.path.join(audios_path, f"{safe_word}.mp3")

        if logger:
            logger.log(f"🔊 Pronouncing: '{word}' → {safe_word}.mp3")

        try:
            with audio_lock:
                if disable_buttons:
                    for btn in disable_buttons:
                        btn.configure(state="disabled")

                if not os.path.exists(audio_file):
                    if logger:
                        logger.log("📥 Audio not found. Generating...")
                    tts = gTTS(text=safe_word, lang="en")
                    tts.save(audio_file)
                    if logger:
                        logger.log("✅ Audio file created.")

                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                if logger:
                    logger.log("▶️ Audio playback started.")

            while pygame.mixer.music.get_busy():
                time.sleep(0.05)

            if logger:
                logger.log("⏹️ Audio playback finished.")

        except Exception as e:
            if logger:
                logger.log(f"❌ Error during audio playback: {e}")

        finally:
            if disable_buttons:
                for btn in disable_buttons:
                    btn.configure(state="normal")

    threading.Thread(target=play_audio, daemon=True).start()


def play_notification_sound(logger=None):
    """Plays a simple notification sound using pygame."""
    
    audio_file = os.path.join(audios_path, "!notification.wav")

    if not os.path.exists(audio_file):
        if logger:
            logger.log("⚠️ Notification sound file not found.")
        return

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        if logger:
            logger.log("🔔 Notification sound played.")
    except Exception as e:
        if logger:
            logger.log(f"❌ Error playing notification sound: {e}")
