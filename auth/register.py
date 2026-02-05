import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from ui.buttons import RoundedButton


class Register_Teacher(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg="#020617")

        # ❌ DO NOT grid/pack this frame here
        # Layout is controlled by app.py

        # ================= VARIABLES =================
        self.var_fname = tk.StringVar()
        self.var_lname = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_securityQ = tk.StringVar()
        self.var_securityA = tk.StringVar()
        self.var_pass = tk.StringVar()
        self.var_confpass = tk.StringVar()

        self.build_ui()
        self.after(200, lambda: self.fname_entry.focus_set())

    # ================= UI =================
    def build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self, bg="#020617")
        container.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # ================= LEFT BRAND =================
        left = tk.Frame(container, bg="#020617")
        left.grid(row=0, column=0, sticky="nsew")

        brand = tk.Frame(left, bg="#020617")
        brand.place(relx=0.15, rely=0.42, anchor="w")

        tk.Label(
            brand,
            text="FACE RECOGNITION\nATTENDANCE SYSTEM",
            font=("Segoe UI", 28, "bold"),
            fg="#38bdf8",
            bg="#020617",
            justify="left",
            wraplength=520
        ).pack(anchor="w")

        tk.Frame(brand, bg="#2563eb", height=3, width=80).pack(anchor="w", pady=(12, 18))

        tk.Label(
            brand,
            text="AI-powered attendance\nusing computer vision",
            font=("Segoe UI", 14),
            fg="#94a3b8",
            bg="#020617",
            justify="left",
            wraplength=500
        ).pack(anchor="w")

        # ================= RIGHT CARD =================
        right = tk.Frame(container, bg="#0f172a")
        right.grid(row=0, column=1, sticky="nsew")

        card = tk.Frame(right, bg="#111827", padx=48, pady=38)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # ---------- TITLE ----------
        tk.Label(
            card,
            text="Teacher Registration",
            font=("Segoe UI", 22, "bold"),
            bg="#111827",
            fg="#38bdf8"
        ).pack(pady=(0, 6))

        tk.Label(
            card,
            text="Create a new teacher account",
            font=("Segoe UI", 11),
            bg="#111827",
            fg="#94a3b8"
        ).pack(pady=(0, 25))

        form = tk.Frame(card, bg="#111827")
        form.pack(fill="x")

        self._entry_pair(form, "First Name", self.var_fname, "Last Name", self.var_lname)
        self._entry_pair(form, "Contact No", self.var_contact, "Email", self.var_email)

        self._divider(form)

        tk.Label(form, text="Security Question", bg="#111827", fg="white").pack(anchor="w")
        sec_q = ttk.Combobox(
            form,
            textvariable=self.var_securityQ,
            values=("Select", "Your Birth Place", "Your Nick Name", "Your Pet Name"),
            state="readonly"
        )
        sec_q.current(0)
        sec_q.pack(fill="x", pady=(6, 16))

        tk.Label(form, text="Security Answer", bg="#111827", fg="white").pack(anchor="w")
        tk.Entry(
            form,
            textvariable=self.var_securityA,
            bg="#1f2937",
            fg="white",
            relief="flat",
            insertbackground="white"
        ).pack(fill="x", pady=(6, 18), ipady=8)

        self._divider(form)

        self._password_field(form, "Password", self.var_pass)
        self._password_field(form, "Confirm Password", self.var_confpass)

        # ---------- BUTTONS ----------
        btns = tk.Frame(card, bg="#111827")
        btns.pack(fill="x", pady=22)

        RoundedButton(
            btns,
            text="Register",
            width=220,
            height=48,
            radius=12,
            bg="#2563eb",
            command=self.register_data
        ).pack(side="left", expand=True, fill="x", padx=8)

        RoundedButton(
            btns,
            text="← Back to Login",
            width=220,
            height=48,
            radius=12,
            bg="#1f2937",
            command=self.back_to_login
        ).pack(side="right", expand=True, fill="x", padx=8)

    # ================= HELPERS =================
    def _divider(self, parent):
        tk.Frame(parent, bg="#1e293b", height=1).pack(fill="x", pady=18)

    def _entry_pair(self, parent, l1, v1, l2, v2):
        row = tk.Frame(parent, bg="#111827")
        row.pack(fill="x", pady=8)

        for label, var in [(l1, v1), (l2, v2)]:
            col = tk.Frame(row, bg="#111827")
            col.pack(side="left", expand=True, fill="x", padx=6)

            tk.Label(col, text=label, bg="#111827", fg="white").pack(anchor="w")
            entry = tk.Entry(
                col,
                textvariable=var,
                bg="#1f2937",
                fg="white",
                relief="flat",
                insertbackground="white"
            )
            entry.pack(fill="x", ipady=8)

            if label == "First Name":
                self.fname_entry = entry

    def _password_field(self, parent, label, variable):
        tk.Label(parent, text=label, bg="#111827", fg="white").pack(anchor="w")

        frame = tk.Frame(parent, bg="#111827")
        frame.pack(fill="x", pady=(6, 16))

        entry = tk.Entry(
            frame,
            textvariable=variable,
            show="•",
            bg="#1f2937",
            fg="white",
            relief="flat",
            insertbackground="white"
        )
        entry.pack(side="left", fill="x", expand=True, ipady=8)

        tk.Button(
            frame,
            text="👁",
            bg="#1f2937",
            fg="#94a3b8",
            relief="flat",
            cursor="hand2",
            command=lambda e=entry: e.config(show="" if e.cget("show") else "•")
        ).pack(side="right", padx=6)

    # ================= LOGIC =================
    def register_data(self):
        if not self.var_fname.get() or not self.var_email.get() or self.var_securityQ.get() == "Select":
            messagebox.showerror("Error", "All fields are required", parent=self)
            return

        if self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error", "Passwords do not match", parent=self)
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="park12",
                database="face_recognition"
            )
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM regteach WHERE email=%s", (self.var_email.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Email already registered", parent=self)
                conn.close()
                return

            cur.execute(
                "INSERT INTO regteach (fname, lname, cnum, email, ssq, sa, pwd) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_contact.get(),
                    self.var_email.get(),
                    self.var_securityQ.get(),
                    self.var_securityA.get(),
                    self.var_pass.get()
                )
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registered Successfully!")
            self.back_to_login()

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    # ================= NAVIGATION =================
    def back_to_login(self):
        self.controller.show_page_by_name("Login")
