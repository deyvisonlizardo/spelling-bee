"""
student_manager.py

Handles loading and saving student data and their competition states.

Functions:
- load_students(): Load the list of students from JSON.
- save_student_state(data): Save current student states to disk.
- load_student_state(): Load persisted student states from disk.
"""

import json
import os
import random

# Paths
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "database")
STUDENT_LIST_FILE = os.path.join(db_path, "students.json")
STUDENT_STATE_FILE = os.path.join(db_path, "students_state.json")


def load_students():

    """
    Loads the list of students from a JSON file.

    Returns:
        list: List of student dictionaries or empty list if not found.
    """

    try:
        with open(STUDENT_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_student_state(data):

    """
    Saves the current state of students (e.g., scores, progress) to a file.

    Args:
        data (dict): A dictionary containing student state data.
    """

    with open(STUDENT_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def initialize_student_state():
    student_names = load_students()
    student_state = [{"name": name, "status": "neutral"} for name in student_names]
    save_student_state(student_state)


def load_student_state():

    """
    Loads the saved student state from a JSON file.

    Returns:
        dict: The student state data, or an empty dictionary if not found.
    """

    student_names = set(load_students())

    try:
        with open(STUDENT_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        initialize_student_state()
        return load_student_state()

    existing_names = {s["name"] for s in data}

    # If mismatch, reinitialize
    if student_names != existing_names:
        initialize_student_state()
        return load_student_state()

    return data

def choose_next_student():
    """Choose a student with 'neutral' status, or declare winner."""
    data = load_student_state()

    neutral = [s for s in data if s["status"] == "neutral"]
    if neutral:
        return random.choice(neutral)

    approved = [s for s in data if s["status"] == "approved"]
    if len(approved) == 1:
        return {"name": approved[0]["name"], "status": "winner"}

    return None


def update_student_status(name, status):
    data = load_student_state()
    for s in data:
        if s["name"] == name:
            s["status"] = status
            break
    save_student_state(data)


def reset_approved_students():
    data = load_student_state()
    for s in data:
        if s["status"] == "approved":
            s["status"] = "neutral"
    save_student_state(data)


def reset_all_students():
    initialize_student_state()
