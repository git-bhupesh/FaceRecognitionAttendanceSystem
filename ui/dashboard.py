import os
import tkinter as tk
from tkinter import Toplevel, messagebox

from config import COLORS, FONTS
from ui.components import DashboardCard, StatusBar

from features.student import Student
from features.train import Train
from features.face_recognition import Face_Recognition
from features.attendance import Attendance
from ui.buttons import RoundedButton




class Dashboard(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg=COLORS["bg"])
        self.cards = []

        self.build_ui()

    # ================= UI =================
    def build_ui(self):
        # ---------- HEADER ----------
        header = tk.Frame(self, bg=COLORS["header"], height=100)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="FACIAL RECOGNITION ATTENDANCE SYSTEM",
            font=FONTS["title"],
            bg=COLORS["header"],
            fg=COLORS["accent"]
        ).pack(pady=(18, 0))

        tk.Label(
            header,
            text="AI-Powered Attendance Monitoring System",
            font=FONTS["small"],
            bg=COLORS["header"],
            fg=COLORS["muted"]
        ).pack()

        # Divider ✅ FIXED
        tk.Frame(self, bg=COLORS["card_hover"], height=2).pack(fill=tk.X)

        # ---------- STATS BAR ----------
        stats = tk.Frame(self, bg=COLORS["card"], height=45)
        stats.pack(fill=tk.X)

        for txt in (
            "📸 Camera: Ready",
            "🧠 Model: Trained",
            "👨‍🎓 Students: Loaded",
            "📅 System Active"
        ):
            tk.Label(
                stats,
                text=txt,
                bg=COLORS["card"],
                fg=COLORS["muted"],
                font=FONTS["small"]
            ).pack(side=tk.LEFT, padx=25)

        # ---------- MAIN GRID ----------
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        cards = [
            ("STUDENT DETAILS", "assets/icons/student.png", self.student_details),
            ("FACE DETECTOR", "assets/icons/face.png", self.face_data),
            ("ATTENDANCE", "assets/icons/attendance.png", self.attendance_data),
            ("HELP SUPPORT", "assets/icons/help.png", self.open_help_support),
            ("TRAIN DATA", "assets/icons/train.png", self.train_data),
            ("PHOTOS", "assets/icons/photos.png", self.open_img),
            ("DEVELOPER", "assets/icons/dev.png", self.developer),
            # ("LOGOUT", "assets/icons/exit.png", self.exit_app),
            ("LOGOUT", "assets/icons/logout.png", self.logout),
        ]

        rows, cols = 2, 4
        for c in range(cols):
            main.columnconfigure(c, weight=1, uniform="x")
        for r in range(rows):
            main.rowconfigure(r, weight=1, uniform="y")

        for i, (text, icon, cmd) in enumerate(cards):
            r, c = divmod(i, cols)
            card = DashboardCard(main, text, icon, cmd)
            card.grid(row=r, column=c, padx=25, pady=25, sticky="nsew")
            self.cards.append(card)

        # ---------- STATUS BAR ----------
        StatusBar(self).pack(side=tk.BOTTOM, fill=tk.X)

    # ================= NAVIGATION =================
    def student_details(self):
        # self.controller.show_page(Student)
        self.controller.show_page_by_name("Student")

    def train_data(self):
        self.controller.show_page(Train)

    def face_data(self):
        self.controller.show_page(Face_Recognition)

    def attendance_data(self):
        self.controller.show_page(Attendance)

    def open_img(self):
        if os.path.exists("data"):
            os.startfile("data")
        else:
            messagebox.showerror("Error", "Data folder not found", parent=self)

    # ================= DEVELOPER =================
    def developer(self):
        dev = Toplevel(self)
        dev.title("Developer & Project Information")
        dev.geometry("720x650")
        dev.resizable(False, False)
        dev.configure(bg="#0f172a")

        tk.Label(
            dev,
            text="Developer Information",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="#22d3ee"
        ).pack(pady=15)

        content = """
 Developer Name:
     Bhupesh Dewangan

     Role:
     Python Developer | Computer Vision & AI Enthusiast

     About:
     Passionate Python developer focused on building
     real-world AI powered automation systems.

     -------------------------------------------------

     Project Name:
     Face Recognition Attendance Management System

     Objective:
     Automate attendance using face recognition
     to ensure accuracy and efficiency.

     -------------------------------------------------

     AI Model Used:
     • Haar Cascade (Face Detection)
     • LBPH Face Recognizer

     Why LBPH?
     ✔ Fast & lightweight
     ✔ Accurate for small datasets
     ✔ Works in real-time environments

     -------------------------------------------------

     Technologies:
     • Python
     • OpenCV
     • Tkinter
     • MySQL
     • NumPy & Pillow

     -------------------------------------------------

     Credits:
     • OpenCV Community
     • Python Software Foundation
     • Academic Mentors
     """

        text = tk.Text(
            dev,
            bg="#020617",
            fg="white",
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        btns = tk.Frame(dev, bg="#0f172a")
        btns.pack(pady=15)

        RoundedButton(
            btns,
            text="GitHub",
            width=150,
            height=42,
            radius=10,
            bg="#2563eb",
            command=lambda: os.startfile("https://github.com/git-bhupesh")
        ).grid(row=0, column=0, padx=10)

        RoundedButton(
            btns,
            text="Download Resume",
            width=180,
            height=42,
            radius=10,
            bg="#16a34a",
            command=lambda: os.startfile(os.path.join("data", "resume.pdf"))
        ).grid(row=0, column=1, padx=10)

    # ================= HELP =================
    def open_help_support(self):
        help_win = Toplevel(self)
        help_win.title("Help & Support")
        help_win.geometry("800x600")
        help_win.configure(bg="#111827")

        tk.Label(
            help_win,
            text="Help & Support",
            font=("Segoe UI", 22, "bold"),
            bg="#111827",
            fg="#38bdf8"
        ).pack(pady=15)

        text = tk.Text(
            help_win,
            bg="#1f2933",
            fg="white",
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        new_help_text = """
     FACE RECOGNITION ATTENDANCE SYSTEM
     ----------------------------------

     ABOUT THE SYSTEM
     This system automates student attendance using face recognition.

     MODULES
     1. Student Management
     2. Face Recognition
     3. Attendance Management

     HOW TO USE
     • Register students and capture face samples
     • Start face recognition
     • Attendance is marked automatically
     • View and export attendance records

     COMMON ISSUES
     • Camera not opening → Check permissions
     • Face not recognized → Improve lighting
     • Attendance not saved → Check database

     DATA & PRIVACY
     • All data is stored locally
     • No internet usage

     SUPPORT
     Developer: Bhupesh Dewangan
     Version: 1.0
     """

        text.insert(tk.END, new_help_text)
        text.config(state=tk.DISABLED)

    # ================= LogOut =================
    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.controller.logout()



