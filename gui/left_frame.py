import customtkinter
from PIL import Image
import os
from gui.student_editor import StudentEditor
from gui.words_viewer import WordsViewer
from gui.info_window import InfoWindow


# Get project root (parent of current file's directory)
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
assets_path = os.path.join(base_path, "assets")
db_path = os.path.join(base_path, "database")

class LeftFrame(customtkinter.CTkFrame):
    def __init__(self, master, logger=None):
        super().__init__(master)
        self.logger = logger
        self.configure(fg_color="transparent")

        # Load logo images using absolute paths
        logo_img = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(assets_path, "sb-logo-black.png")),
            dark_image=Image.open(os.path.join(assets_path, "sb-logo-white.png")),
            size=(106, 59)
        )

        self.logo = customtkinter.CTkLabel(self, image=logo_img, text="")
        self.logo.grid(row=0, column=0, padx=10, pady=20)

        self.rowconfigure(1, weight=1)

        # Infos button
        self.button = customtkinter.CTkButton(self, text="Infos", command=self.open_info_window)
        self.button.grid(row=2, column=0, padx=10)

        # Buttons that now call methods on this instance
        self.manage_students_btn = customtkinter.CTkButton(self, text="👥 Manage students", command=self.open_students_editor)
        self.manage_students_btn.grid(row=3, column=0, padx=10, pady=(20, 10))

        self.manage_words_btn = customtkinter.CTkButton(self, text="📚 View words", command=self.open_words_viewer)
        self.manage_words_btn.grid(row=4, column=0, padx=10, pady=(0, 10))

        # Theme toggle button
        self.theme_mode = "System"  # default
        self.toggle_theme_btn = customtkinter.CTkButton(self, text="🌓 Toggle Theme", command=self.toggle_theme)
        self.toggle_theme_btn.grid(row=99, column=0, padx=10, pady=(30, 10), sticky="s")


    def open_students_editor(self):
        STUDENT_LIST_FILE = os.path.join(db_path, "students.json")
        StudentEditor(self, STUDENT_LIST_FILE, title="Manage Students", logger=self.logger)

    def open_words_viewer(self):
        WORDS_FILE = os.path.join(db_path, "words.json")
        WordsViewer(self, WORDS_FILE, title="Manage Words")

    def open_info_window(self):
        if hasattr(self, "info_window") and self.info_window.winfo_exists():
            self.info_window.lift()
            return

        self.info_window = InfoWindow(self.master)  # Pass main app reference

    def toggle_theme(self):
        if self.theme_mode == "Light":
            customtkinter.set_appearance_mode("Dark")
            self.theme_mode = "Dark"
        else:
            customtkinter.set_appearance_mode("Light")
            self.theme_mode = "Light"
