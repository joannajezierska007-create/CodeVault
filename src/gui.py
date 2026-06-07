import tkinter as tk
from tkinter import filedialog, messagebox

import crypto_engine as crypto
import file_manager as fs
import utils as utils
import vault as vault


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeVault NO-LIB")
        self.root.geometry("600x350")

        self.file = ""

        tk.Label(root, text="CodeVault", font=("Arial", 18)).pack()

        tk.Button(root, text="Select File", command=self.select_file).pack()

        self.label = tk.Label(root, text="No file selected")
        self.label.pack()

        tk.Label(root, text="Password").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Encrypt", command=self.encrypt).pack(pady=5)
        tk.Button(root, text="Decrypt", command=self.decrypt).pack(pady=5)

        self.log = tk.Text(root, height=10)
        self.log.pack()

    def select_file(self):
        self.file = filedialog.askopenfilename()
        self.label.config(text=self.file)

    def encrypt(self):
        if not self.file:
            return

        data = fs.read_file(self.file)
        encrypted = crypto.encrypt(data, self.password.get())

        out = self.file + ".locked"
        fs.write_file(out, encrypted)

        vault.add_entry(self.file, out)

        self.log.insert(tk.END, f"Encrypted → {out}\n")

    def decrypt(self):
        if not self.file:
            return

        data = fs.read_file(self.file)
        decrypted = crypto.decrypt(data, self.password.get())

        # 🔥 RESTORE ORIGINAL FILE EXACTLY
        out = self.file.replace(".locked", "")

        fs.write_file(out, decrypted)

        self.log.insert(tk.END, f"Restored → {out}\n")