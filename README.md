# Spelling Bee Application

The **Spelling Bee Application** is a Python-based tool designed to assist users in learning and practicing spelling. It provides features such as word pronunciation using text-to-speech (TTS), notification sounds, and a user-friendly interface.

---

## Features

- 🎓 Manage student participants.
- 📖 Word database management (used/unused words).
- ⏱️ Timer and round control.
- 🔊 Audio playback for spelling prompts.
- 🖥️ Full GUI interface with real-time updates.

---

## Project Structure

```text
.
│
├── main.py # Application entry point
├── core/ # Core logic for rounds, students, and words
│ ├── audio_manager.py
│ ├── round_manager.py
│ ├── student_manager.py
│ └── word_manager.py
│
├── gui/ # Graphical user interface components
│ ├── info_window.py
│ ├── student_frame.py
│ └── ... (various UI frames)
│
├── database/ # JSON files storing app data
│ ├── students.json
│ ├── words.json
│ └── used_words.json
│
├── assets/ # Icons and logos
│ └── *.png, *.ico
│
└── improvements.txt # Suggestions or planned enhancements
└── requirements.txt # Libraries to be install via pip
```

## How to Install and Run the Project

If you're setting up this Spelling Bee application on a local machine (such as a POS or any standalone system), follow these steps to install the necessary dependencies and run the project:

### Step-by-Step Installation

#### 1. Install Python

- Download and install Python 3.11 or later from the official [Python website](https://www.python.org/downloads/).

- Make sure to check the option “Add Python to PATH” during installation.

#### 2. Clone or Download the Project

```bash
git clone https://github.com/deyvisonlizardo/spelling-bee.git
```
```bash
cd spelling-bee
```

#### 3. Install required dependencies

Use the requirements.txt file to install all needed packages:

```bash
pip install -r requirements.txt
```

#### 4. Run the Application

From the project root directory, run:

```bash
python main.py
```

## Notes
- Internet access is required the first time `gTTS` is used to generate speech files.

## How to use the project

The main GUI window consists of several key panels:

- **Student Panel**: Displays the current student, their progress, and allows switching between students.

- **Word Panel**: Displays the current word, plays pronunciation audio using gTTS, and marks it as used once spelled.

- **Timer Panel**: Shows a countdown timer for each student.

- **Log Panel**: Keeps a record of words attempted and student results.

- **Control Buttons**: Start/Stop round, Reset, Skip word, etc.

This is the screen that is used by the controller of the competition.



---

The secondary GUI/Infos window consists of:

- **Student Panel**: Displays the current student.
- **Timer Panel**: Shows a countdown timer for each student.
- **Word Panel**: Displays the current word.

This is the screen that should be showed for the public but not for the student.