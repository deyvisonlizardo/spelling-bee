import customtkinter

class InfoTimerFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.label = customtkinter.CTkLabel(self, text="00:00", font=("Poppins SemiBold", 18), width=140, height=100)
        self.label.grid(row=0, column=0, sticky="news")

    def update(self):
        time_left = self.app.timer.get_remaining_time()

        if isinstance(time_left, int):
            mins, secs = divmod(time_left, 60)
            formatted_time = f"{mins:02}:{secs:02}"
        elif isinstance(time_left, str):  # e.g., "Time's up!"
            formatted_time = time_left
        else:
            formatted_time = "00:00"

        self.label.configure(text=formatted_time)
