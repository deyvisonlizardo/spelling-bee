import customtkinter
from core.audio_manager import play_notification_sound


class TimerFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, width=160, height=140)
        self.app = app
        self.remaining_time = 0
        self.timer_running = False
        self.has_run = False

        font = customtkinter.CTkFont(family="Poppins SemiBold", size=16)

        self.timer_label = customtkinter.CTkLabel(self, text="00:00", font=font)
        self.timer_label.grid(row=0, columnspan=2, sticky="news", padx=10, pady=(10, 0))

        self.min_input = customtkinter.CTkEntry(self, width=50)
        self.min_input.insert(0, "0")
        self.min_input.grid(row=1, column=0, sticky="news", padx=10, pady=10)

        self.sec_input = customtkinter.CTkEntry(self, width=50)
        self.sec_input.insert(0, "60")
        self.sec_input.grid(row=1, column=1, sticky="news", padx=(0, 10), pady=10)

        self.start_btn = customtkinter.CTkButton(self, text="▶", command=self.start_timer, width=40)
        self.pause_btn = customtkinter.CTkButton(self, text="⏸", command=self.pause_timer, width=40)
        self.stop_btn = customtkinter.CTkButton(self, text="⏹", command=self.stop_timer, width=40)

        self.start_btn.grid(row=2, column=0, sticky="news", padx=10, pady=(0, 10))
        self.pause_btn.grid_forget()
        self.stop_btn.grid(row=2, column=1, sticky="news", padx=(0, 10), pady=(0, 10))

        self.timer_id = None
        self.update_timer()

    def start_timer(self):
        if not self.timer_running:
            if self.remaining_time == 0:
                try:
                    mins = int(self.min_input.get())
                    secs = int(self.sec_input.get())
                    self.remaining_time = (mins * 60) + secs
                except ValueError:
                    self.timer_label.configure(text="Invalid Input!")
                    return

            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None

            self.has_run = True
            self.timer_running = True
            self.toggle_start_pause(show_start=False)
            self.update_timer()

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.toggle_start_pause(show_start=True)
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None

    def stop_timer(self):
        self.timer_running = False
        self.has_run = False
        self.remaining_time = 0
        self.timer_label.configure(text="00:00")

        if hasattr(self.app.leftframe, "info_window") and self.app.leftframe.info_window.winfo_exists():
            self.app.leftframe.info_window.timer_frame.update()

        self.toggle_start_pause(show_start=True)
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer(self):
        if self.timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.configure(text=f"{mins:02}:{secs:02}")
            self.timer_id = self.after(1000, self.update_timer)

            # Update info window if it exists
            if hasattr(self.app.leftframe, "info_window") and self.app.leftframe.info_window.winfo_exists():
                self.app.leftframe.info_window.timer_frame.update()

        elif self.remaining_time == 0 and self.timer_running:
            self.timer_running = False
            self.timer_label.configure(text="Time's up!")
            self.toggle_start_pause(show_start=True)

            # Update info window if it exists
            if hasattr(self.app.leftframe, "info_window") and self.app.leftframe.info_window.winfo_exists():
                self.app.leftframe.info_window.timer_frame.update()

            play_notification_sound(logger=self.app.logs)
            self.app.logs.log("🔔 Time's up!")

    def toggle_start_pause(self, show_start=True):
        if show_start:
            self.pause_btn.grid_forget()
            self.start_btn.grid(row=2, column=0, sticky="news", padx=10, pady=(0, 10))
        else:
            self.start_btn.grid_forget()
            self.pause_btn.grid(row=2, column=0, sticky="news", padx=10, pady=(0, 10))

    def get_remaining_time(self):
        if hasattr(self, "timer_running"):
            if not self.timer_running and self.remaining_time == 0 and getattr(self, "has_run", False):
                return "Time's up!"
            return self.remaining_time
        return 0
