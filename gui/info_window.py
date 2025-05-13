import os
from PIL import Image
import customtkinter

from gui.info_student_frame import InfoStudentFrame
from gui.info_word_frame import InfoWordFrame
from gui.info_timer_frame import InfoTimerFrame

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
assets_path = os.path.join(base_path, "assets")

class InfoWindow(customtkinter.CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.title("Spelling Bee")

        # Center the window
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Delayed focus and icon
        self.after(100, lambda: (self.lift(), self.focus_force()))
        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.after(200, lambda: self.iconbitmap(os.path.join(assets_path, "sp_icon.ico")))

        # Load logo images using absolute paths
        logo_img = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(assets_path, "your-logo-black.png")),
            dark_image=Image.open(os.path.join(assets_path, "your-logo-white.png")),
            size=(120, 50.04)
        )

        # Modular Frames
        self.student_frame = InfoStudentFrame(self, app)
        self.student_frame.grid(row=0, column=0, sticky="news", padx=(30, 10), pady=(30, 10))

        self.timer_frame = InfoTimerFrame(self, app)
        self.timer_frame.grid(row=0, column=1, padx=(10, 30), pady=(30, 10))

        self.word_frame = InfoWordFrame(self, app)
        self.word_frame.grid(row=1, column=0, columnspan=2, sticky="news", padx=(30, 30), pady=(10, 30))

        self.logo = customtkinter.CTkLabel(self, image=logo_img, text="")
        self.logo.grid(row=2, column=1, padx=(0, 40), pady=(0, 40), sticky="se")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(1, weight=1)

        self.update_all()

    def update_all(self):
        self.student_frame.update()
        self.word_frame.update()
        self.timer_frame.update()
