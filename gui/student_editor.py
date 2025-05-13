import customtkinter
import json
import os


class StudentEditor(customtkinter.CTkToplevel):
    def __init__(self, master, file_path, title="Manage Students", logger=None):
        super().__init__(master)
        self.title(title)
        self.geometry("600x600")

        self.transient(master)  # Keep it tied to master
        self.grab_set()         # Block interaction with main window
        self.focus()            # Bring this window into focus

        self.file_path = file_path
        self.logger = logger
        self.entries = {}

        # Top Controls
        top_frame = customtkinter.CTkFrame(self)
        top_frame.pack(pady=5, fill="x", padx=10)

        self.add_btn = customtkinter.CTkButton(top_frame, text="➕ Add", command=self.add_entry)
        self.add_btn.pack(side="left", padx=5)

        self.save_btn = customtkinter.CTkButton(top_frame, text="💾 Save", command=self.save_changes)
        self.save_btn.pack(side="left", padx=5)

        self.counter_label = customtkinter.CTkLabel(self, text="")
        self.counter_label.pack(pady=(0, 5))

        # Scrollable Content
        self.scroll_frame = customtkinter.CTkScrollableFrame(self)
        self.scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.load_content()

    def load_content(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

            if not isinstance(self.data, list) or not all(isinstance(i, str) for i in self.data):
                raise Exception("Invalid format for students.json")

            for name in self.data:
                self.add_entry(name)

        except Exception as e:
            error_label = customtkinter.CTkLabel(self, text=f"❌ Error:\n{e}")
            error_label.pack()

    def add_entry(self, value=""):
        row = customtkinter.CTkFrame(self.scroll_frame)
        row.pack(fill="x", pady=2, padx=5)

        entry = customtkinter.CTkEntry(row)
        entry.insert(0, value)
        entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        remove_btn = customtkinter.CTkButton(row, text="❌", width=30, command=lambda: self.remove_entry(row))
        remove_btn.pack(side="left")

        self.entries[row] = entry
        self.update_counter()

    def remove_entry(self, row):
        row.destroy()
        if row in self.entries:
            del self.entries[row]
        self.update_counter()

    def update_counter(self):
        self.counter_label.configure(text=f"{len(self.entries)} students")

    def save_changes(self):
        try:
            new_data = []
            for _, entry in self.entries.items():
                value = entry.get().strip()
                if value:
                    new_data.append(value)

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)

            if self.logger:
                self.logger.log("✅ Student list saved.")

            self.destroy()

        except Exception as e:
            error_label = customtkinter.CTkLabel(self, text=f"❌ Error saving JSON:\n{e}")
            error_label.pack(pady=5)
