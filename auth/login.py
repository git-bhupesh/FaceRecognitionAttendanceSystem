import tkinter as tk
from tkinter import messagebox
import mysql.connector
from ui.buttons import RoundedButton
from ui.dashboard import Dashboard   # OK: used after login


class Login_System(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg="#020617")

        self.show_pwd = False
        self.build_ui()

        # make frame visible
        self.grid(row=0, column=0, sticky="nsew")

    # ================= UI =================
    def build_ui(self):
        # Root grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ================= MAIN CONTAINER =================
        container = tk.Frame(self, bg="#020617")
        container.grid(row=0, column=0, sticky="nsew")

        container.columnconfigure(0, weight=4)  # left
        container.columnconfigure(1, weight=6)  # right
        container.rowconfigure(0, weight=1)

        # ================= LEFT: LOGIN =================
        left = tk.Frame(container, bg="#020617")
        left.grid(row=0, column=0, sticky="nsew")

        # Login Card
        card = tk.Frame(
            left,
            bg="#111827",
            width=420,
            height=520,
            highlightthickness=1,
            highlightbackground="#1e293b"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Title
        tk.Label(
            card,
            text="Teacher Login",
            font=("Segoe UI", 24, "bold"),
            bg="#111827",
            fg="#38bdf8"
        ).pack(pady=(40, 6))

        tk.Label(
            card,
            text="Sign in to continue",
            font=("Segoe UI", 11),
            bg="#111827",
            fg="#94a3b8"
        ).pack(pady=(0, 30))

        # ================= FORM =================
        form = tk.Frame(card, bg="#111827")
        form.pack(fill="x", padx=40)

        # Email
        tk.Label(form, text="Email Address", bg="#111827", fg="white").pack(anchor="w")
        self.txt_user = tk.Entry(
            form,
            font=("Segoe UI", 12),
            bg="#1f2933",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.txt_user.pack(fill="x", pady=(6, 20), ipady=8)

        # Password
        tk.Label(form, text="Password", bg="#111827", fg="white").pack(anchor="w")
        pwd_frame = tk.Frame(form, bg="#111827")
        pwd_frame.pack(fill="x", pady=(6, 30))

        self.txt_pass = tk.Entry(
            pwd_frame,
            font=("Segoe UI", 12),
            bg="#1f2933",
            fg="white",
            insertbackground="white",
            relief="flat",
            show="•"
        )
        self.txt_pass.pack(side="left", fill="x", expand=True, ipady=8)

        self.eye_btn = tk.Button(
            pwd_frame,
            text="👁",
            bg="#1f2933",
            fg="#94a3b8",
            relief="flat",
            cursor="hand2",
            command=self.toggle_password
        )
        self.eye_btn.pack(side="right", padx=8)

        # Login Button
        RoundedButton(
                card,
                text="Login",
                width=260,
                height=48,
                radius=12,
                bg="#2563eb",
                command=self.login
            ).pack(fill="x", padx=40, pady=(0, 12))

        # 🔥 REGISTER BUTTON (FIXED)
        tk.Button(
            card,
            text="New Teacher? Register Here",
            command=lambda: self.controller.show_page_by_name("Register"),
            bg="#111827",
            fg="#38bdf8",
            relief="flat",
            cursor="hand2"
        ).pack(pady=18)

        # Footer
        tk.Label(
            card,
            text="Authorized Personnel Only",
            font=("Segoe UI", 9),
            bg="#111827",
            fg="#64748b"
        ).pack(pady=(0, 25))

        # ================= RIGHT: BRANDING =================
        right = tk.Frame(container, bg="#020617")
        right.grid(row=0, column=1, sticky="nsew")

        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        brand = tk.Frame(right, bg="#020617")
        brand.place(relx=0.15, rely=0.45, anchor="w")

        tk.Label(
            brand,
            text="FACE RECOGNITION\nATTENDANCE SYSTEM",
            font=("Segoe UI", 28, "bold"),
            fg="#38bdf8",
            bg="#020617",
            justify="left",
            wraplength=500
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="AI-powered attendance\nusing computer vision",
            font=("Segoe UI", 14),
            fg="#94a3b8",
            bg="#020617",
            justify="left",
            wraplength=480
        ).pack(anchor="w", pady=(10, 0))

    # ================= LOGIC =================
    def login(self):
        email = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="park12",
                database="face_recognition"
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT fname FROM regteach WHERE email=%s AND pwd=%s",
                (email, password)
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                messagebox.showinfo("Welcome", f"Welcome {row[0]} 👋")
                self.controller.show_page_by_name("Dashboard")
            else:
                messagebox.showerror("Invalid", "Invalid Email or Password")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ================= HELPERS =================
    def toggle_password(self):
        self.show_pwd = not self.show_pwd
        self.txt_pass.config(show="" if self.show_pwd else "•")
        self.eye_btn.config(text="🙈" if self.show_pwd else "👁")
