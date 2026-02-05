import tkinter as tk
from PIL import Image, ImageTk
from config import COLORS, FONTS


class RoundedButton(tk.Frame):
    def __init__(
        self,
        parent,
        text,
        command=None,
        icon_path=None,
        width=220,
        height=48,
        radius=10,
        bg="#2563eb",
        fg="white"
    ):
        super().__init__(parent, bg=parent["bg"])

        self.command = command
        self.text = text
        self.icon_path = icon_path
        self.width = width
        self.height = height
        self.radius = radius
        self.bg = bg
        self.fg = fg

        self.disabled = False  # ✅ important

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=parent["bg"],
            highlightthickness=0
        )
        self.canvas.pack()

        self.draw()
        self.bind_events()

    # ---------------- DRAW ----------------
    def draw(self, hover=False):
        self.canvas.delete("all")

        if self.disabled:
            bg = "#374151"      # disabled gray
            fg = "#9ca3af"
        else:
            bg = COLORS["accent"] if hover else COLORS["accent_dark"]
            fg = "#000" if hover else COLORS["text"]

        self.bg_id = self.round_rect(
            0, 0,
            self.width, self.height,
            self.radius,
            fill=bg
        )

        x = self.width // 2

        # Icon (optional)
        if self.icon_path:
            icon = Image.open(self.icon_path).resize((20, 20), Image.LANCZOS)
            self.icon_img = ImageTk.PhotoImage(icon)
            self.canvas.create_image(26, self.height // 2, image=self.icon_img)
            x += 14

        self.text_id = self.canvas.create_text(
            x,
            self.height // 2,
            text=self.text,
            font=FONTS["card"],
            fill=fg
        )

    # ---------------- ROUND RECT ----------------
    def round_rect(self, x1, y1, x2, y2, r, **kwargs):
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
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    # ---------------- EVENTS ----------------
    def bind_events(self):
        for w in (self, self.canvas):
            w.bind("<Button-1>", self._on_click)
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.config(cursor="hand2")

    def _on_click(self, event):
        if not self.disabled and self.command:
            self.command()

    def _on_enter(self, event):
        if not self.disabled:
            self.draw(hover=True)

    def _on_leave(self, event):
        if not self.disabled:
            self.draw(hover=False)

    # ---------------- PUBLIC API ----------------
    def disable(self):
        self.disabled = True
        self.draw()
        self.configure(cursor="arrow")

    def enable(self):
        self.disabled = False
        self.draw()
        self.configure(cursor="hand2")
