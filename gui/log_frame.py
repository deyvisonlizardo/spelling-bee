import customtkinter

class LogFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.textbox = customtkinter.CTkTextbox(self, height=100)
        self.textbox.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def log(self, message):
        self.textbox.insert("end", f"{message}\n")
        self.textbox.see("end")
