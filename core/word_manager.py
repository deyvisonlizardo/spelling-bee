"""
word_manager.py

Handles word management for the spelling bee game including:
- Loading words
- Marking words as used
- Sanitizing filenames
- Shuffling and resetting word pools

Functions:
- sanitize_filename(): Converts a string into a filesystem-safe format.
- load_words(): Load all available words from file.
- save_used_words(): Save the list of already-used words.
- get_unused_words(): Filter and return unused words.
- mark_word_as_used(): Add a word to the used list.
- reset_used_words(): Clear the list of used words.
"""

import json
import os
import random
import unicodedata
import re
import tkinter.messagebox as messagebox 

# Paths
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "database")
WORDS_FILE = os.path.join(db_path, "words.json")
USED_WORDS_FILE = os.path.join(db_path, "used_words.json")

def sanitize_filename(text):
    """Sanitize text for use as a safe filename (multilingual support)."""
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "_", text)

def load_words():
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_used_words():
    try:
        with open(USED_WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_used_words(used_words):
    with open(USED_WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(used_words, f, indent=4)

def reset_used_words(logger=None):
    """Fully resets the used words list."""
    if logger:
        logger.log("🔄 All words used. Resetting history...")

    if os.path.exists(USED_WORDS_FILE):
        os.remove(USED_WORDS_FILE)

    with open(USED_WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

def choose_word(logger=None):
    """Pick a random word that hasn't been used yet."""
    words = load_words()
    used_words = load_used_words()

    available_words = [word for word in words if word["word"] not in used_words]

    if not available_words:
        # Ask for confirmation to reset
        confirm = messagebox.askyesno(
            "Reset Used Words",
            "All words have been used.\nDo you want to reset the word list?"
        )
        if not confirm:
            if logger:
                logger.log("❌ Word reset canceled by user.")
            return None

        reset_used_words(logger)

        # Notify user that reset occurred
        messagebox.showinfo(
            "Reset Completed",
            "✅ Word list has been reset.\nYou can now select a new word."
        )

        if logger:
            logger.log("✅ Word list reset completed.")

        return None  # STOP here, don't auto-select a new word

    # Select and return a word
    chosen_word = random.choice(available_words)
    used_words.append(chosen_word["word"])
    save_used_words(used_words)

    if logger:
        logger.log(f"📚 New word selected: {chosen_word['word']}")

    return chosen_word