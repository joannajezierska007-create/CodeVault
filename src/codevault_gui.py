import os
import base64
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

SUPPORTED_EXTENSIONS = {".cpp", ".c", ".java", ".py", ".txt", ".h"}

# -----------------------------
# Encryption core
# -----------------------------
def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def xor_data(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def encrypt_file(path, password):
    ext = os.path.splitext(path)[1]

    if ext not in SUPPORTED_EXTENSIONS:
        return "[!] Unsupported file type"

    with open(path, "rb") as f:
        data = f.read()

    key = derive_key(password)
    encrypted = xor_data(data, key)

    encoded = base64.b64encode(encrypted)

    out_path = path + ".locked"

    with open(out_path, "wb") as f:
        f.write(encoded)

    return f"[+] Encrypted → {out_path}"

def decrypt_file(path, password):
    if not path.endswith(".locked"):
        return "[!] Select a .locked file"

    with open(path, "rb") as f:
        encoded = f.read()

    try:
        encrypted = base64.b64decode(encoded)
    except:
        return "[!] Corrupted file"

    key = derive_key(password)
    decrypted = xor_data(encrypted, key)

    out_path = path.replace(".locked", ".decrypted")

    with open(out_path, "wb") as f:
        f.write(decrypted)

    return f"[+] Decrypted → {out_path}"

# -----------------------------
# GUI APP
# -----------------------------
class CodeVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Vault - Encrypt Source Code")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.file_path = ""

        # Title
        tk.Label(root, text="CODE VAULT", font=("Arial", 16, "bold")).pack(pady=10)

        # File picker
        self.file_label = tk.Label(root, text="No file selected", fg="gray")
        self.file_label.pack()

        tk.Button(root, text="Browse File", command=self.browse_file).pack(pady=5)

        # Password
        tk.Label(root, text="Password:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Encrypt", width=15, command=self.encrypt).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Decrypt", width=15, command=self.decrypt).grid(row=0, column=1, padx=5)

        # Output log
        self.log = tk.Text(root, height=6, width=55)
        self.log.pack(pady=10)

    # -------------------------
    def browse_file(self):
        file = filedialog.askopenfilename(
            title="Select source code file",
            filetypes=[
                ("Code files", "*.cpp *.c *.java *.py *.txt *.h"),
                ("All files", "*.*")
            ]
        )

        if file:
            self.file_path = file
            self.file_label.config(text=file, fg="black")

    # -------------------------
    def encrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Enter password")
            return

        result = encrypt_file(self.file_path, password)
        self.log.insert(tk.END, result + "\n")

    # -------------------------
    def decrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Enter password")
            return

        result = decrypt_file(self.file_path, password)
        self.log.insert(tk.END, result + "\n")


# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeVaultApp(root)
    root.mainloop()