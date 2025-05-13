import customtkinter

class SpeechExampleFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.speech_label = customtkinter.CTkLabel(self, text="", font=("Poppins", 20, "italic"))
        self.speech_label.grid(row=0, column=0, sticky="ews", padx=10, pady=(20, 10))

        self.example_label = customtkinter.CTkLabel(self, text="", font=("Poppins", 20), wraplength=800)
        self.example_label.grid(row=1, column=0, sticky="new", padx=10, pady=(0, 20))

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=1)

    def update_speech(self, text):
        self.speech_label.configure(text=f"🔠 {text}")

    def update_example(self, text):
        self.example_label.configure(text=f"💬 {text}")

    def clear_info(self):
        self.speech_label.configure(text="")
        self.example_label.configure(text="")
