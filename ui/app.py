import tkinter as tk
from config import COLORS


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ================= ROOT =================
        self.title("Face Recognition Attendance System")
        self.geometry("1530x790+0+0")
        self.configure(bg=COLORS["bg"])

        # ================= CONTAINER =================
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        # MUST exist for page routing
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.frames = {}

        # ⛔ IMPORTANT: lazy imports (avoid circular imports)
        from auth.login import Login_System
        from ui.dashboard import Dashboard
        from features.student import Student
        from features.attendance import Attendance
        from features.train import Train
        from auth.register import Register_Teacher

        self.page_map = {
            "Login": Login_System,
            "Dashboard": Dashboard,
            "Register": Register_Teacher, 
            "Student": Student,
            "Attendance": Attendance,
            "Train": Train,
        }

        # Start app
        self.show_page(Login_System)
        
        # ================= EASING CURVES =================
    def ease_out_cubic(self, t):
        return 1 - pow(1 - t, 3)

    def ease_in_out_cubic(self, t):
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2


    # ================= PAGE CONTROL =================
    def show_page(self, PageClass):
        frame = self.frames.get(PageClass)

        if frame is None:
            frame = PageClass(self.container, self)
            self.frames[PageClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame.tkraise()
                # 🎯 Animation routing
        page_name = PageClass.__name__

        if page_name in ("Login_System", "Register", "Dashboard"):
            self.animate_fade_in()
        else:
            self.animate_slide_up(frame)


    def show_page_by_name(self, name):
        PageClass = self.page_map.get(name)
        if PageClass:
            self.show_page(PageClass)

    def logout(self):
        """Clear all pages and go back to Login (same window)"""
        self.clear_pages()
        self.show_page_by_name("Login")

    def clear_pages(self, keep_login=True):
        from auth.login import Login_System

        for PageClass, frame in list(self.frames.items()):
            if keep_login and PageClass is Login_System:
                continue
            frame.destroy()
            del self.frames[PageClass]

    def animate_fade_in(self, steps=18, delay=12):
        self.attributes("-alpha", 0.0)

        def _fade(step=0):
            t = step / steps
            eased = self.ease_out_cubic(t)
            self.attributes("-alpha", eased)

            if step < steps:
                self.after(delay, _fade, step + 1)

        _fade()



    def animate_slide_up(self, frame, start_y=60, steps=14, delay=12):
        frame.place(relx=0, rely=0, relwidth=1, relheight=1, y=start_y)

        def _slide(step=0):
            t = step / steps
            eased = self.ease_out_cubic(t)
            y = int(start_y * (1 - eased))

            frame.place_configure(y=y)

            if step < steps:
                self.after(delay, _slide, step + 1)
            else:
                frame.place_forget()
                frame.grid(row=0, column=0, sticky="nsew")

        _slide()

