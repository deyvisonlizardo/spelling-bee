import customtkinter
from core import round_manager
import os
import tkinter.messagebox as messagebox

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "database")


class StudentFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.current_student = None

        self.label = customtkinter.CTkLabel(self, text="", font=("Poppins", 20, "bold"))
        self.label.grid(row=0, rowspan=4, column=0, sticky="news", padx=10, pady=10)

        self.pick_button = customtkinter.CTkButton(self, text="🎯 Pick Student", command=self.pick_student)
        self.pick_button.grid(row=0, column=1, sticky="s", padx=10, pady=(20, 10))

        self.approve_button = customtkinter.CTkButton(self, text="✅ Approve", command=self.approve_student)
        self.approve_button.grid(row=1, column=1, padx=10, pady=(0, 10))

        self.reject_button = customtkinter.CTkButton(self, text="❌ Reject", command=self.reject_student)
        self.reject_button.grid(row=2, column=1, padx=10, pady=(0, 20))

        self.next_round_button = customtkinter.CTkButton(self, text="➡️ Next Round", command=self.advance_round)
        self.next_round_button.grid(row=3, column=1, padx=10, pady=(0, 10))

        self.reset_competition_button = customtkinter.CTkButton(self, text="🔁 Reset Competition", command=self.reset_competition)
        self.reset_competition_button.grid(row=4, column=1, padx=10, pady=(0, 20))

        self.columnconfigure(0, weight=1)

    def pick_student(self):
        if self.current_student and not self.is_current_student_marked():
            self.label.configure(text="⚠️ Approve/Reject current student first.")
            self.app.logs.log("⚠️ Approve/Reject current student before picking next.")
            return

        student = round_manager.get_next_student()
        if not student:
            if round_manager.can_advance_round():
                self.label.configure(text="⚠️ Round over! Press 'Advance Round'")
            else:
                self.label.configure(text="✅ All students done")
            return

        self.current_student = student
        self.label.configure(text=f"🙋 {student}")
        self.app.logs.log(f"🎯 Picked student: {student}")

        # ✅ Re-enable buttons now that a student is selected
        self.approve_button.configure(state="normal")
        self.reject_button.configure(state="normal")

        # Update student info if it exists and clears the word info
        if hasattr(self.app.leftframe, "info_window") and self.app.leftframe.info_window.winfo_exists():
            self.app.leftframe.info_window.student_frame.update()
            self.app.leftframe.info_window.word_frame.clear()

        # Clear word info & stop timer
        self.app.word.clear_word()
        self.app.speech.clear_info()
        self.app.timer.stop_timer()

    def approve_student(self):
        if not self.current_student:
            messagebox.showwarning("No Student", "No student selected.")
            return
        round_manager.approve_student(self.current_student)
        
        self.app.logs.log(f"✅ Student approved: {self.current_student}")

    def reject_student(self):
        if not self.current_student:
            messagebox.showwarning("No Student", "No student selected.")
            return
        round_manager.reject_student(self.current_student)

        self.app.logs.log(f"❌ Student rejected: {self.current_student}")

    def advance_round(self):
        result = round_manager.advance_round()

        if result is None:
            messagebox.showerror("Error", "Round state not available.")
            return

        if "error" in result:
            messagebox.showwarning("⚠️ Cannot Advance", result["error"])
            return

        self.current_student = None
        self.approve_button.configure(state="disabled")
        self.reject_button.configure(state="disabled")

        if "winner" in result:
            self.label.configure(text=f"🏆 Winner: {result['winner']}")

            if hasattr(self.app.leftframe, "info_window") and self.app.leftframe.info_window.winfo_exists():
                try:
                    self.app.leftframe.info_window.word_frame.label.configure(text=f"** 🏆 Winner **\n{result['winner']}")
                    self.app.leftframe.info_window.student_frame.grid_forget()
                    self.app.leftframe.info_window.timer_frame.grid_forget()
                    self.app.leftframe.info_window.word_frame.word_label.grid_forget()

                except AttributeError:
                    pass # Handle case where info_window is not initialized

            messagebox.showinfo("🏆 Spelling Bee Winner", f"🎉 Congratulations to {result['winner']}!")

        elif "next_round" in result:
            self.label.configure(text=f"🔄 Round {result['next_round']} ready")

            if hasattr(self.app.leftframe, "info_window") and self.app.leftframe.info_window.winfo_exists():
                try:
                    self.app.leftframe.info_window.word_frame.label.configure(text=f"Starting round {result['next_round']}")
                    self.app.leftframe.info_window.student_frame.label.configure(text="")
                except AttributeError:
                    pass # Handle case where info_window is not initialized

        self.current_student = None

        self.app.word.clear_word()
        self.app.speech.clear_info()
        self.app.timer.stop_timer()

    def reset_competition(self):

        confirm = messagebox.askyesno(
            "Confirm Reset",
            "Are you sure you want to reset the entire competition?\nThis action cannot be undone."
        )
        if not confirm:
            return

        round_manager.reset_round()
        state = round_manager.initialize_round()
        self.current_student = None
        self.label.configure(text=f"🔄 Competition Reset - Round {state['current_round']} ready")
        self.app.logs.log("🔄 Competition has been reset")

        self.app.word.clear_word()
        self.app.speech.clear_info()
        self.app.timer.stop_timer()

    def is_current_student_marked(self):
        data = round_manager.load_round_state()
        if not data or not self.current_student:
            return False

        return (
            self.current_student in data["approved_students"]
            or self.current_student in data["rejected_students"]
        )
    
    def get_current_student(self):
        return self.current_student if hasattr(self, "current_student") else ""
