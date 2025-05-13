import customtkinter

class InfoWordFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        self.word_label = customtkinter.CTkLabel(self, text="Word:", font=("Poppins", 18))
        self.word_label.grid(row=0, column=0, sticky="new", padx=10, pady=(10, 0))

        self.label = customtkinter.CTkLabel(self, text="", font=("Poppins", 50, "bold"))
        self.label.grid(row=1, column=0, sticky="news", pady=10)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def update(self):
        word = self.app.word.get_current_word()
        self.label.configure(text=f"{word}" if word else "")

    def clear(self):
        self.label.configure(text="")