import os
import customtkinter

from gui.word_frame import WordFrame
from gui.student_frame import StudentFrame
from gui.timer_frame import TimerFrame
from gui.speech_example_frame import SpeechExampleFrame
from gui.log_frame import LogFrame
from gui.left_frame import LeftFrame

# Always resolve relative to this file's location
base_path = os.path.abspath(os.path.dirname(__file__))
assets_path = os.path.join(base_path, "assets")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spelling Bee")
        self.iconbitmap(os.path.join(assets_path, "sp_icon.ico"))

        # Center the window
        window_width = 1280
        window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)

        # Left Frame (Logo & Settings)
        self.leftframe = LeftFrame(self)
        self.leftframe.grid(row=0, column=0, rowspan=4, sticky="news", padx=10, pady=10)

        # Word Frame
        self.word = WordFrame(self, app=self)
        self.word.grid(row=0, column=1, sticky="news", padx=(10, 10), pady=(30, 10))

        # Timer Frame
        self.timer = TimerFrame(self, app=self)
        self.timer.grid(row=0, column=2, sticky="news", padx=(10, 30), pady=(30, 10))

        # Speech & Example Frame
        self.speech = SpeechExampleFrame(self)
        self.speech.grid(row=1, column=1, columnspan=2, sticky="news", padx=(10, 30), pady=(10, 10))

        # Student Frame
        self.student = StudentFrame(self, app=self)
        self.student.grid(row=2, column=1, columnspan=2, sticky="news", padx=(10, 30), pady=(10, 10))

        # Log Frame
        self.logs = LogFrame(self)
        self.logs.grid(row=3, column=1, columnspan=2, sticky="news", padx=(10, 30), pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
