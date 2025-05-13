"""
round_manager.py

Handles logic for loading and saving round state and student data.
Useful for persisting competition sessions between runs.

Functions:
- load_students(): Load the student list from a JSON file.
- save_round_state(data): Save the round state to disk.
- load_round_state(): Load the round state from disk.
"""

import os
import json
import random

# Paths
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "database")
STUDENT_LIST_FILE = os.path.join(db_path, "students.json")
ROUND_STATE_FILE = os.path.join(db_path, "round_state.json")

def load_students():

    """
    Loads student data from a JSON file.

    Returns:
        list: List of student dictionaries, or empty list if file not found.
    """

    try:
        with open(STUDENT_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_round_state(data):

    """
    Saves the current round state to a JSON file.

    Args:
        data (dict): The round state data to save.
    """

    try:
        with open(ROUND_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"❌ Error saving round state: {e}")

def load_round_state():

    """
    Loads the saved round state from a JSON file.

    Returns:
        dict: The round state, or an empty dictionary if not found.
    """

    if not os.path.exists(ROUND_STATE_FILE):
        return None
    try:
        with open(ROUND_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading round state: {e}")
        return None

def initialize_round():
    students = load_students()
    state = {
        "current_round": 1,
        "current_students": students,
        "picked_students": [],
        "approved_students": [],
        "rejected_students": []
    }
    save_round_state(state)
    return state

def reset_round():
    if os.path.exists(ROUND_STATE_FILE):
        os.remove(ROUND_STATE_FILE)

def get_next_student():
    state = load_round_state()
    if not state:
        state = initialize_round()

    available = [s for s in state["current_students"] if s not in state["picked_students"]]
    if not available:
        return None

    student = random.choice(available)
    state["picked_students"].append(student)
    save_round_state(state)
    return student

def approve_student(name):
    state = load_round_state()
    if not state:
        return

    if name not in state["picked_students"]:
        state["picked_students"].append(name)

    if name not in state["approved_students"]:
        state["approved_students"].append(name)

    if name in state["rejected_students"]:
        state["rejected_students"].remove(name)

    save_round_state(state)

def reject_student(name):
    state = load_round_state()
    if not state:
        return

    if name not in state["picked_students"]:
        state["picked_students"].append(name)

    if name in state["approved_students"]:
        state["approved_students"].remove(name)

    if name not in state["rejected_students"]:
        state["rejected_students"].append(name)

    save_round_state(state)

def can_advance_round():
    state = load_round_state()
    if not state:
        return False

    all_picked = len(state["picked_students"]) == len(state["current_students"])
    return all_picked

def advance_round():
    state = load_round_state()
    if not state:
        return None

    # Block advancing if any student is unjudged
    unprocessed = [
        student for student in state["current_students"]
        if student not in state["approved_students"] and student not in state["rejected_students"]
    ]

    if unprocessed:
        return {
            "error": f"⚠️ Cannot advance: {len(unprocessed)} student(s) haven't been judged yet."
        }

    # Handle winner case
    if len(state["approved_students"]) == 1:
        winner = state["approved_students"][0]
        reset_round()
        return {"winner": winner}

    # Advance with approved students, or all if none approved
    next_students = state["approved_students"] if state["approved_students"] else state["current_students"]

    state = {
        "current_round": state["current_round"] + 1,
        "current_students": next_students,
        "picked_students": [],
        "approved_students": [],
        "rejected_students": []
    }

    save_round_state(state)
    return {"next_round": state["current_round"], "students": next_students}
