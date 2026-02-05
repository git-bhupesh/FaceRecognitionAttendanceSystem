from tkinter import *
from tkinter import messagebox
import mysql.connector
import cv2
from datetime import datetime
from config import COLORS, FONTS, BUTTONS
from PIL import Image, ImageTk
from ui.buttons import RoundedButton
import tkinter as tk
import winsound


class Face_Recognition(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["bg"])

        # ================= STATE =================
        self.cap = None
        self.recognition_running = False
        self.session_completed = False

        self.total_detected = 0
        self.new_marked = 0
        self.already_marked = 0

        # ================= LOAD MODELS =================
        self.faceCascade = cv2.CascadeClassifier(
            "models/haarcascade_frontalface_default.xml"
        )
        self.clf = cv2.face.LBPHFaceRecognizer_create()
        self.clf.read("models/classifier.xml")

        # ================= HEADER =================
        header = Frame(self, bg=COLORS["header"], height=70)
        header.pack(fill=X)

        RoundedButton(
            header,
            text="← Back",
            width=90,
            height=36,
            radius=8,
            bg=COLORS["card"],
            command=lambda: self.controller.show_page_by_name("Dashboard")
        ).pack(side=tk.LEFT, padx=15, pady=10)

        Label(
            header, text="FACE RECOGNITION",
            font=FONTS["title"],
            bg=COLORS["header"],
            fg=COLORS["accent"]
        ).pack(pady=(8, 0))

        Label(
            header, text="Live recognition & attendance monitoring",
            font=FONTS["small"],
            bg=COLORS["header"],
            fg=COLORS["muted"]
        ).pack()

        # ================= MAIN =================
        main = Frame(self, bg=COLORS["bg"])
        main.pack(fill=BOTH, expand=True, padx=30, pady=20)

        camera_card = Frame(main, bg=COLORS["card"])
        camera_card.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 15))

        Label(
            camera_card, text="Live Camera Feed",
            font=FONTS["card"],
            bg=COLORS["card"],
            fg=COLORS["text"]
        ).pack(anchor=W, padx=20, pady=15)

        self.preview = Label(
            camera_card,
            text="Camera Preview\n(Click Start Recognition)",
            bg=COLORS["card_hover"],
            fg=COLORS["muted"],
            font=("Segoe UI", 14),
            relief=RIDGE
        )
        self.preview.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        self.overlay = Frame(self.preview, bg=COLORS["card_hover"])
        self.overlay.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(
            self.overlay,
            text="Ready to Start",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS["card_hover"],
            fg="white"
        ).pack(pady=(0, 10))

        self.start_btn = RoundedButton(
            self.overlay,
            text="Start Face Recognition",
            width=220,
            height=50,
            radius=12,
            bg=BUTTONS["primary"],
            command=self.start_recognition
        )
        self.start_btn.pack(pady=12)

        # ================= LOG =================
        log_card = Frame(main, bg=COLORS["card"], width=420)
        log_card.pack(side=RIGHT, fill=Y)
        log_card.pack_propagate(False)

        self.log_box = Text(
            log_card,
            bg=COLORS["card_hover"],
            fg="white",
            font=("Consolas", 11),
            relief=FLAT
        )
        self.log_box.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.log("System Ready")

        # ================= FOOTER =================
        footer = Frame(self, bg=COLORS["card"], height=60)
        footer.pack(fill=X)

        self.status_var = StringVar(value="IDLE")
        Label(
            footer,
            textvariable=self.status_var,
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["card"],
            fg=COLORS["accent"]
        ).pack(side=LEFT, padx=30)

    # ================= LOG =================
    def log(self, text):
        time = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(END, f"[{time}] {text}\n")
        self.log_box.see(END)

    # ================= START =================
    def start_recognition(self):
        self.session_completed = False
        self.total_detected = 0
        self.new_marked = 0
        self.already_marked = 0

        self.status_var.set("RUNNING")
        self.start_btn.disable()

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Camera not accessible")
            self.reset_ui()
            return

        self.recognition_running = True
        self.overlay.place_forget()
        self.update_frame()

    # ================= CAMERA LOOP =================
    def update_frame(self):
        if not self.recognition_running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.stop_recognition()
            return

        frame = self.process_frame(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (880, 480))

        img = ImageTk.PhotoImage(Image.fromarray(frame))
        self.preview.imgtk = img
        self.preview.config(image=img, text="")

        if self.session_completed:
            self.recognition_running = False
            self.after(1000, self.stop_recognition)
            return

        self.after(10, self.update_frame)

    # ================= FACE PROCESSING =================
    def process_frame(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.1, 10)

        for (x, y, w, h) in faces:
            if self.session_completed:
                break

            id, predict = self.clf.predict(gray[y:y+h, x:x+w])
            confidence = int(100 * (1 - predict / 300))

            # ---------- UNKNOWN ----------
            if confidence <= 77:
                cv2.rectangle(img, (x, y), (x+w, y+h), (40, 40, 220), 2)
                cv2.putText(
                    img, "UNKNOWN",
                    (x, y-12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (40, 40, 220), 2
                )
                continue

            # ---------- FETCH STUDENT ----------
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="park12", database="face_recognition"
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT Name, Roll_No FROM student WHERE Student_ID=%s",
                (str(id),)
            )
            data = cur.fetchone()
            conn.close()

            if not data:
                continue

            name, roll = data
            date = datetime.now().strftime("%d/%m/%Y")

            # ---------- STATUS ----------
            if self.check_already_marked(id, date):
                label = "ALREADY MARKED"
                box_color = (0, 165, 255)
                self.already_marked += 1
                self.status_var.set("ALREADY MARKED")
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                self.log(f"ℹ️ {name} ({roll}) already marked")
            else:
                label = "SUCCESS"
                box_color = (0, 200, 80)
                self.new_marked += 1
                self.mark_attendance(id, roll, name)
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
                self.log(f"✅ Attendance marked: {name} ({roll})")

            self.session_completed = True

            # ---------- FACE BOX ----------
            cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 3)

            # ---------- INFO PANEL ----------
            panel_y = y - 65 if y > 70 else y + h + 10
            cv2.rectangle(
                img,
                (x, panel_y),
                (x+w, panel_y + 55),
                box_color,
                -1
            )

            cv2.putText(
                img, f"{name}",
                (x + 6, panel_y + 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 2
            )

            cv2.putText(
                img, f"Roll: {roll}",
                (x + 6, panel_y + 36),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (255, 255, 255), 1
            )

            cv2.putText(
                img, f"{label}  {confidence}%",
                (x + 6, panel_y + 52),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 1
            )

            break

        return img


    # ================= STOP =================
    def stop_recognition(self):
        if self.cap:
            self.cap.release()
            self.cap = None

        self.log("🛑 Recognition stopped")
        self.log(f"📊 New: {self.new_marked}, Already: {self.already_marked}")
        self.reset_ui()

    def reset_ui(self):
        self.recognition_running = False
        self.status_var.set("IDLE")
        self.start_btn.enable()
        self.preview.config(image="", text="Camera Preview\n(Click Start Recognition)")
        self.overlay.place(relx=0.5, rely=0.5, anchor=CENTER)

    # ================= DB =================
    def check_already_marked(self, student_id, current_date):
        conn = mysql.connector.connect(
            host="localhost", user="root",
            password="park12", database="face_recognition"
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM stdattendance WHERE std_id=%s AND std_date=%s",
            (str(student_id), str(current_date))
        )
        result = cur.fetchone()
        conn.close()
        return bool(result)

    def mark_attendance(self, sid, roll, name):
        now = datetime.now()
        conn = mysql.connector.connect(
            host="localhost", user="root",
            password="park12", database="face_recognition"
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO stdattendance VALUES (%s,%s,%s,%s,%s,%s)",
            (
                sid,
                roll,
                name,
                now.strftime("%H:%M:%S"),
                now.strftime("%d/%m/%Y"),
                "Present"
            )
        )
        conn.commit()
        conn.close()
