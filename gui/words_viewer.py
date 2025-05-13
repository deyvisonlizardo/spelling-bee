import customtkinter
import json
import tkinter.filedialog as fd
import pandas as pd
from tkinter import messagebox
import threading
from gtts import gTTS
import os
import threading



class WordsViewer(customtkinter.CTkToplevel):
    def __init__(self, master, file_path, title="Words Viewer"):
        super().__init__(master)
        self.title(title)
        self.geometry("900x700")

        self.transient(master)  # Keep it tied to master
        self.grab_set()         # Block interaction with main window
        self.focus()            # Bring this window into focus

        self.file_path = file_path
        self.page = 0
        self.page_size = 20

        self.words = []

        self.counter_label = customtkinter.CTkLabel(self, text="")
        self.counter_label.pack(pady=(5, 5))

        self.scroll_frame = customtkinter.CTkScrollableFrame(self)
        self.scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.page_frame = customtkinter.CTkFrame(self)
        self.page_frame.pack(pady=(0, 10))

        # Top control bar
        self.control_frame = customtkinter.CTkFrame(self)
        self.control_frame.pack(pady=(5, 0), fill="x", padx=10)

        self.import_btn = customtkinter.CTkButton(self.control_frame, text="📥 Import from Excel", command=self.import_from_excel)
        self.import_btn.pack(side="left", padx=5)

        self.template_btn = customtkinter.CTkButton(self.control_frame, text="📄 Download Template", command=self.download_template)
        self.template_btn.pack(side="left", padx=5)

        self.generate_audio_btn = customtkinter.CTkButton(self.control_frame, text="🔊 Generate Missing Audios", command=self.start_audio_generation_thread)  # Note: this triggers a thread
        self.generate_audio_btn.pack(side="left", padx=5)

        # Progress bar (initially hidden)
        self.progress = customtkinter.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(pady=(0, 10), padx=10, fill="x")
        self.progress.pack_forget()  # Hide initially

        self.load_words()

    def load_words(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.words = json.load(f)

            if not isinstance(self.words, list) or not all(isinstance(i, dict) and "word" in i for i in self.words):
                raise Exception("Invalid format for words.json")

            self.show_page(0)

        except Exception as e:
            self.scroll_frame.pack_forget()
            error_label = customtkinter.CTkLabel(self, text=f"❌ Failed to load:\n{e}")
            error_label.pack(pady=20)

    def show_page(self, index):
        for row in self.scroll_frame.winfo_children():
            row.destroy()

        start = index * self.page_size
        end = start + self.page_size
        page_items = self.words[start:end]

        for i, item in enumerate(page_items):
            row = customtkinter.CTkFrame(self.scroll_frame)
            row.pack(fill="x", pady=2, padx=5)

            row_number = start + i + 1  # Global row number

            # Row number
            customtkinter.CTkLabel(row, text=f"{row_number:3}", width=40).pack(side="left", padx=5)

            w = item.get("word", "")
            p = item.get("part_of_speech", "")
            e = item.get("example", "")

            customtkinter.CTkLabel(row, text=w, width=200).pack(side="left", padx=5)
            customtkinter.CTkLabel(row, text=p, width=120).pack(side="left", padx=5)
            customtkinter.CTkLabel(row, text=e, anchor="w").pack(side="left", fill="x", expand=True, padx=5)

        self.page = index
        self.build_pagination()

        # ✅ Improved counter message
        start_index = start + 1
        end_index = min(end, len(self.words))
        self.counter_label.configure(text=f"Showing words {start_index}–{end_index} of {len(self.words)}")

    def build_pagination(self):
        for w in self.page_frame.winfo_children():
            w.destroy()

        total_pages = (len(self.words) + self.page_size - 1) // self.page_size
        for i in range(total_pages):
            btn = customtkinter.CTkButton(self.page_frame, text=str(i + 1), width=40, command=lambda i=i: self.show_page(i))
            if i == self.page:
                btn.configure(fg_color="blue", text_color="white")
            btn.pack(side="left", padx=2)

    def import_from_excel(self):
        file_path = fd.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            if not all(col in df.columns for col in ["word", "part_of_speech", "example"]):
                raise Exception("Excel must contain 'word', 'part_of_speech', and 'example' columns.")

            new_words = df[["word", "part_of_speech", "example"]].dropna().to_dict(orient="records")

            self.preview_import_dialog(new_words)

        except Exception as e:
            messagebox.showerror("Import Failed", f"❌ Failed to read Excel:\n{e}")
    
    def preview_import_dialog(self, new_words):
        preview_window = customtkinter.CTkToplevel(self)
        preview_window.title("Preview Words to Import")
        preview_window.geometry("700x500")

        preview_window.transient(self)  # Keep it tied to master
        preview_window.grab_set()         # Block interaction with main window
        preview_window.focus()            # Bring this window into focus

        label = customtkinter.CTkLabel(preview_window, text=f"Previewing {len(new_words)} words:")
        label.pack(pady=5)

        scroll = customtkinter.CTkScrollableFrame(preview_window)
        scroll.pack(expand=True, fill="both", padx=10, pady=10)

        for i, item in enumerate(new_words):
            row = customtkinter.CTkFrame(scroll)
            row.pack(fill="x", pady=1, padx=5)

            customtkinter.CTkLabel(row, text=f"{i+1}", width=30).pack(side="left", padx=2)
            customtkinter.CTkLabel(row, text=item.get("word", ""), width=200).pack(side="left", padx=5)
            customtkinter.CTkLabel(row, text=item.get("part_of_speech", ""), width=120).pack(side="left", padx=5)
            customtkinter.CTkLabel(row, text=item.get("example", ""), anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons
        button_frame = customtkinter.CTkFrame(preview_window)
        button_frame.pack(pady=10)

        confirm_btn = customtkinter.CTkButton(button_frame, text="✅ Confirm Import", command=lambda: self.start_import_thread(new_words, preview_window))
        confirm_btn.pack(side="left", padx=10)

        cancel_btn = customtkinter.CTkButton(button_frame, text="❌ Cancel", command=preview_window.destroy)
        cancel_btn.pack(side="left", padx=10)

    def start_import_thread(self, new_words, preview_window):
        preview_window.destroy()
        threading.Thread(target=self.import_words, args=(new_words,), daemon=True).start()

    def import_words(self, new_words):
        try:
            self.progress.set(0)
            self.progress.pack()
            self.update_idletasks()

            # Simulate progress updates
            self.progress.set(0.3)
            self.update_idletasks()

            # Just store in memory
            self.words = new_words

            self.progress.set(0.7)
            self.update_idletasks()

            # Save to file
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.words, f, indent=4, ensure_ascii=False)

            self.progress.set(1)
            self.update_idletasks()

            # Use main thread to update GUI safely
            self.after(0, lambda: self.finalize_import(success=True, count=len(new_words)))

        except Exception as e:
            self.after(0, lambda: self.finalize_import(success=False, error=e))

    def finalize_import(self, success=True, count=0, error=None):
        self.progress.pack_forget()

        if success:
            self.show_page(0)
            messagebox.showinfo("Import Successful", f"✅ Successfully imported {count} words.")
        else:
            messagebox.showerror("Import Error", f"❌ Failed during import:\n{error}")

    def download_template(self):
        save_path = fd.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not save_path:
            return

        template_data = {
            "word": ["example_word"],
            "part_of_speech": ["noun"],
            "example": ["This is an example sentence."]
        }

        try:
            df = pd.DataFrame(template_data)
            df.to_excel(save_path, index=False, engine="openpyxl")
            messagebox.showinfo("Template Saved", "✅ Excel template saved successfully!")

        except Exception as e:
            messagebox.showerror("Template Failed", f"❌ Failed to save template:\n{e}")

    
    def start_audio_generation_thread(self):
        # Disable the button while processing
        self.generate_audio_btn.configure(state="disabled")

        # Start background thread
        threading.Thread(target=self.generate_missing_audios, daemon=True).start()


    def generate_missing_audios(self):

        audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audios"))
        os.makedirs(audio_dir, exist_ok=True)

        def sanitize_audio_filename(word):
            return "".join(c if c.isalnum() else "_" for c in word.lower())

        def audio_exists(word):
            file_path = os.path.join(audio_dir, sanitize_audio_filename(word) + ".mp3")
            return os.path.exists(file_path)

        def save_audio(word):
            file_path = os.path.join(audio_dir, sanitize_audio_filename(word) + ".mp3")
            tts = gTTS(text=word, lang='en')
            tts.save(file_path)

        # Create progress bar safely in the main thread
        self.after(0, lambda: self._show_progress_bar())

        created_count = 0
        total = len(self.words)

        for idx, entry in enumerate(self.words):
            word = entry.get("word", "")
            if not audio_exists(word):
                try:
                    save_audio(word)
                    created_count += 1
                except Exception as e:
                    print(f"Error creating audio for {word}: {e}")

            # Update progress bar safely in the UI thread
            self.after(0, lambda i=idx: self.progress.set((i + 1) / total))

        # Hide progress bar and re-enable button
        self.after(0, lambda: self.progress.pack_forget())
        self.after(0, lambda: self.generate_audio_btn.configure(state="normal"))
        self.after(0, lambda: messagebox.showinfo("Audio Generation", f"✅ {created_count} missing audio(s) created."))

    def _show_progress_bar(self):
        self.progress = customtkinter.CTkProgressBar(self)
        self.progress.pack(pady=10, padx=10, fill="x")
        self.progress.set(0)
