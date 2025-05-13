import customtkinter

class InfoStudentFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.student_label = customtkinter.CTkLabel(self, text="Student:", font=("Poppins", 18))
        self.student_label.grid(row=0, column=0, sticky="new", padx=10, pady=(10, 0))

        self.label = customtkinter.CTkLabel(self, text="", font=("Poppins", 22, "bold"))
        self.label.grid(row=1, column=0, sticky="news", padx=10, pady=(0, 10))

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def update(self):
        student = self.app.student.get_current_student()
        self.label.configure(text=f"{student}" if student else "")
