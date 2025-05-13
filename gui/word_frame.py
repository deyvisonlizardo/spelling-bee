import customtkinter
from core import word_manager, audio_manager


class WordFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.current_word = None

        self.word_label = customtkinter.CTkLabel(self, text="", font=("Poppins", 30, "bold"))
        self.word_label.grid(row=0, rowspan=2, column=0, sticky="news", pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.pick_button = customtkinter.CTkButton(self, text="🎲 Pick a Word", command=self.update_word)
        self.pick_button.grid(row=0, column=1, sticky="ews", padx=10, pady=10)

        self.re_pronounce = customtkinter.CTkButton(self, text="Pronunciation", command=self.repeat_pronunciation)
        self.re_pronounce.grid(row=1, column=1, sticky="new", padx=10, pady=(0, 10))

    def update_word(self):
        word_data = word_manager.choose_word(logger=self.app.logs)
        if word_data:
            self.current_word = word_data
            self.word_label.configure(text=f"{word_data['word']}")
            self.app.speech.update_speech(word_data['part_of_speech'])
            self.app.speech.update_example(word_data['example'])
            self.app.logs.log(f"📚 Picked word: {word_data['word']}")

            # Update info window if it exists
            if hasattr(self.app.leftframe, "info_window") and self.app.leftframe.info_window.winfo_exists():
                self.app.leftframe.info_window.word_frame.update()

            # Play pronunciation
            audio_manager.pronounce_word(word_data['word'], logger=self.app.logs, disable_buttons=[self.pick_button, self.re_pronounce])

            # Restart timer
            self.app.timer.stop_timer()
            self.after(200, self.app.timer.start_timer)

    def repeat_pronunciation(self):
        if self.current_word:
            self.app.logs.log("🔁 Repeating pronunciation.")
            audio_manager.pronounce_word(self.current_word['word'], logger=self.app.logs, disable_buttons=[self.pick_button, self.re_pronounce])

    def clear_word(self):
        self.current_word = None
        self.word_label.configure(text="")

    def get_current_word(self):
        return self.current_word["word"] if self.current_word else ""
