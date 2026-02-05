from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
import threading
import tkinter as tk
from ui.buttons import RoundedButton
from config import COLORS
# ---------- CONFIG ----------
DATA_DIR = "data/samples"
MODEL_PATH = "models/classifier.xml"

class Train(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["bg"])
        # self.build_ui()
        self.training_running = False 

        # ================= HEADER =================
        header = Frame(self , bg="#1f1f1f", height=80)
        header.pack(fill=X)
        
        RoundedButton(
            header,
            text="← Back",
            width=90,
            height=36,
            radius=8,
            bg=COLORS["card"],
            fg=COLORS["text"],
            command=lambda: self.controller.show_page_by_name("Dashboard")
        ).pack(side=tk.LEFT, padx=15, pady=10)

        Label(
            header,
            text="TRAIN DATASET",
            font=("Segoe UI", 28, "bold"),
            bg="#1f1f1f",
            fg="#00e5ff"
        ).pack(pady=(10, 0))

        Label(
            header,
            text="Train face samples to generate recognition model",
            font=("Segoe UI", 11),
            bg="#1f1f1f",
            fg="#9aa0a6"
        ).pack()

        # ================= MAIN =================
        main = Frame(self , bg="#111827")
        main.pack(fill=BOTH, expand=True, padx=30, pady=20)

        # ================= BANNER =================
        banner_frame = Frame(main, bg="#111827")
        banner_frame.pack(fill=X)

        img = Image.open("data/images/banner.png").resize((1450, 300), Image.LANCZOS)
        self.banner_img = ImageTk.PhotoImage(img)
        Label(banner_frame, image=self.banner_img, bg="#111827").pack()

        # ================= STATS =================
        stats = Frame(main, bg="#111827")
        stats.pack(pady=20)

        self.faces_var = StringVar(value="Faces: 0")
        self.students_var = StringVar(value="Students: 0")

        self.stat_card(stats, self.faces_var).pack(side=LEFT, padx=15)
        self.stat_card(stats, self.students_var).pack(side=LEFT, padx=15)

        # ================= STATUS =================
        self.stage_var = StringVar(value="Idle")
        Label(
            main,
            textvariable=self.stage_var,
            font=("Segoe UI", 12, "bold"),
            bg="#111827",
            fg="#9aa0a6"
        ).pack(pady=(10, 6))

        # ================= PROGRESS =================
        self.progress = ttk.Progressbar(
            main,
            orient=HORIZONTAL,
            length=600,
            mode="determinate"
        )
        self.progress.pack(pady=(0, 20))

        # ================= BUTTONS =================
        btns = Frame(main, bg="#111827")
        btns.pack()

        self.train_btn = RoundedButton(
        btns,
        text="Start Training",
        width=180,      # approx same as width=18
        height=48,      # approx same as height=2
        radius=12,
        bg="#2563eb",
        command=self.confirm_train
    )

        # self.train_btn.pack(pady=10)
        self.train_btn.pack(side=LEFT, padx=10)

        self.clean_btn = RoundedButton(
            btns,
            text="Clean Invalid Samples",
            width=200,     # equivalent to width=20
            height=44,     # equivalent to height=2
            radius=10,
            bg="#374151",
            command=self.clean_samples
        )

        self.clean_btn.pack(side=tk.LEFT, padx=10)

        self.update_stats()

    # ================= UI HELPERS =================
    def stat_card(self, parent, var):
        card = Frame(parent, bg="#1f2937", width=180, height=80)
        card.pack_propagate(False)
        Label(
            card,
            textvariable=var,
            font=("Segoe UI", 14, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(expand=True)
        return card

    # ================= TRAIN FLOW =================
    def confirm_train(self):
        if messagebox.askyesno(
            "Retrain Confirmation",
            "Retraining will overwrite the existing model.\n\nContinue?"
        ):
            self.start_training()

    def start_training(self):
        if self.training_running:
            return

        self.training_running = True
        # self.train_btn.config(state=DISABLED)
        self.train_btn.disable()
        self.clean_btn.disable()
        self.progress["value"] = 0
        self.stage_var.set("Scanning training images...")

        threading.Thread(target=self.train_classifier, daemon=True).start()

    def train_classifier(self):
        if not os.path.exists(DATA_DIR):
            self.fail("Training directory not found")
            return

        image_paths = [
            os.path.join(DATA_DIR, f)
            for f in os.listdir(DATA_DIR)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ]

        faces, ids = [], []

        total = len(image_paths)
        if total == 0:
            self.fail("No training images found")
            return

        for idx, image in enumerate(image_paths, start=1):
            try:
                img = Image.open(image).convert("L")
                img_np = np.array(img, "uint8")
                sid = int(os.path.basename(image).split(".")[1])
                faces.append(img_np)
                ids.append(sid)
            except:
                continue

            progress = int((idx / total) * 60)
            self.update_progress(progress, "Extracting face data...")

        self.update_progress(70, "Training recognition model...")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, np.array(ids))
        clf.write(MODEL_PATH)

        self.update_progress(100, "Training completed successfully")
        self.finish(len(faces), len(set(ids)))

    # ================= UTIL =================
    def update_progress(self, value, stage):
        self .after(0, lambda: (
            self.progress.config(value=value),
            self.stage_var.set(stage)
        ))

    def finish(self, faces, students):
        self .after(0, lambda: (
            self.faces_var.set(f"Faces: {faces}"),
            self.students_var.set(f"Students: {students}"),
            self.train_btn.config(text="Retrain Dataset", state=NORMAL),
            self.clean_btn.config(state=NORMAL),
            messagebox.showinfo("Success", "Training completed successfully!")
        ))
        self.training_running = False

    def fail(self, msg):
        self .after(0, lambda: messagebox.showerror("Error", msg))
        self.training_running = False

    def clean_samples(self):
        if not messagebox.askyesno(
            "Confirm Cleanup",
            "This will remove improperly named samples.\nContinue?"
        ):
            return

        removed = 0
        for f in os.listdir(DATA_DIR):
            if not f.count(".") >= 2:
                os.remove(os.path.join(DATA_DIR, f))
                removed += 1

        messagebox.showinfo("Cleanup Done", f"Removed {removed} invalid samples")

    def update_stats(self):
        if not os.path.exists(DATA_DIR):
            return

        images = os.listdir(DATA_DIR)
        faces = len(images)
        students = len(set(
            f.split(".")[1] for f in images if f.count(".") >= 2
        ))

        self.faces_var.set(f"Faces: {faces}")
        self.students_var.set(f"Students: {students}")


