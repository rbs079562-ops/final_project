import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import crypto_engine


class DecryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Recovery Tool")
        self.root.geometry("500x300")
        self.root.configure(bg="#2c3e50")

        # Header
        tk.Label(root, text="Decryption Utility", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50").pack(pady=15)

        # Instructions
        tk.Label(root, text="Enter the unique key provided by the administrator:", fg="#bdc3c7", bg="#2c3e50").pack()

        # Input Field
        self.key_entry = tk.Entry(root, width=50, font=("Consolas", 10))
        self.key_entry.pack(pady=10)

        # Progress
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=15)

        # Button
        self.decrypt_btn = tk.Button(root, text="RECOVER FILES", command=self.start_decryption,
                                     bg="#27ae60", fg="white", font=("Arial", 11, "bold"))
        self.decrypt_btn.pack(pady=10)

        self.status = tk.Label(root, text="Waiting for key...", fg="#7f8c8d", bg="#2c3e50")
        self.status.pack()

    def run_logic(self):
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please enter a key.")
            self.decrypt_btn.config(state="normal")
            return

        files = crypto_engine.get_target_files()
        if not files:
            messagebox.showinfo("Info", "No files found to decrypt.")
            self.decrypt_btn.config(state="normal")
            return

        self.decrypt_btn.config(state="disabled")
        self.progress["maximum"] = len(files)

        for i, file in enumerate(files):
            self.status.config(text=f"Decrypting {os.path.basename(file)}...")
            crypto_engine.process_file_in_memory(file, key)
            self.progress["value"] = i + 1

        self.status.config(text="Decryption Finished.")
        messagebox.showinfo("Success", "Process completed. Verify your files.")
        self.decrypt_btn.config(state="normal")

    def start_decryption(self):
        threading.Thread(target=self.run_logic, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = DecryptorApp(root)
    root.mainloop()