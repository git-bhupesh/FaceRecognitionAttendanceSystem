import tkinter as tk
from PIL import Image, ImageTk
from config import COLORS, FONTS


class DashboardCard(tk.Frame):
    def __init__(self, parent, text, icon_path, command):
        super().__init__(
            parent,
            bg=COLORS["card"],
            highlightthickness=1,
            highlightbackground=COLORS["card_hover"]
        )

        self.command = command
        self.icon_path = icon_path
        self.text = text
        self.pack_propagate(False)

        self.build_ui()
        self.bind_events()

    # ================= UI =================
    def build_ui(self):
        # ---------- TOP ICON ----------
        img = Image.open(self.icon_path).resize((140, 140), Image.LANCZOS)
        self.top_icon_img = ImageTk.PhotoImage(img)

        self.icon = tk.Label(
            self,
            image=self.top_icon_img,
            bg=COLORS["card"]
        )
        self.icon.pack(pady=(22, 12))

        # ---------- ROUNDED BUTTON ----------
        self.btn_canvas = tk.Canvas(
            self,
            height=52,          # Increased button height
            bg=COLORS["card"],
            highlightthickness=0
        )
        self.btn_canvas.pack(fill="x", padx=18, pady=(0, 18))

        self.draw_button()

    def draw_button(self):
        self.btn_canvas.delete("all")

        radius = 12  # Rounded corners (8–12px)
        w = self.btn_canvas.winfo_width() or 320
        h = 52

        self.btn_bg = self._round_rect(
            0, 0, w, h,
            radius,
            fill=COLORS["accent_dark"]
        )

        # Button icon (left)
        icon = Image.open(self.icon_path).resize((22, 22), Image.LANCZOS)
        self.btn_icon_img = ImageTk.PhotoImage(icon)
        self.btn_canvas.create_image(28, h // 2, image=self.btn_icon_img)

        # Button text
        self.btn_text = self.btn_canvas.create_text(
            w // 2 + 10,
            h // 2,
            text=self.text,
            fill=COLORS["text"],
            font=FONTS["card"]
        )

    # ================= ROUNDED RECT =================
    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.btn_canvas.create_polygon(
            points,
            smooth=True,
            **kwargs
        )

    # ================= EVENTS =================
    def bind_events(self):
        for w in (self, self.icon, self.btn_canvas):
            w.bind("<Button-1>", lambda e: self.command())
            w.bind("<Enter>", self.on_enter)
            w.bind("<Leave>", self.on_leave)
            w.config(cursor="hand2")

        self.btn_canvas.bind("<Configure>", lambda e: self.draw_button())

    def on_enter(self, e):
        self.configure(bg=COLORS["card_hover"])
        self.icon.configure(bg=COLORS["card_hover"])
        self.btn_canvas.itemconfig(self.btn_bg, fill=COLORS["accent"])
        self.btn_canvas.itemconfig(self.btn_text, fill="#000")

    def on_leave(self, e):
        self.configure(bg=COLORS["card"])
        self.icon.configure(bg=COLORS["card"])
        self.btn_canvas.itemconfig(self.btn_bg, fill=COLORS["accent_dark"])
        self.btn_canvas.itemconfig(self.btn_text, fill=COLORS["text"])


class StatusBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["header"], height=30)
        self.pack_propagate(False)

        tk.Label(
            self,
            text="🟢 Camera: Ready",
            bg=COLORS["header"],
            fg=COLORS["muted"],
            font=FONTS["small"]
        ).pack(side="left", padx=15)

        tk.Label(
            self,
            text="🧠 Model: Trained",
            bg=COLORS["header"],
            fg=COLORS["muted"],
            font=FONTS["small"]
        ).pack(side="left", padx=25)

        tk.Label(
            self,
            text="v1.0 • FaceAttendanceSystem • © Bhupesh",
            bg=COLORS["header"],
            fg=COLORS["muted"],
            font=FONTS["small"]
        ).pack(side="right", padx=15)
