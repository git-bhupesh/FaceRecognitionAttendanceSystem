import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import cv2
import os
from PIL import Image, ImageTk

from config import COLORS, FONTS, SIZES, BUTTONS
from ui.buttons import RoundedButton


class Student(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["bg"])
        self.cap = None  # camera handle

        # ================= STYLES =================
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Dark.TEntry",
            fieldbackground="#020617",
            background="#020617",
            foreground="white",
            insertcolor="white"
        )

        style.configure(
            "Dark.TCombobox",
            fieldbackground="#020617",
            background="#020617",
            foreground="white",
            arrowcolor="white",
            bordercolor="#334155"
        )

        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", "#020617")],
            foreground=[("readonly", "white")]
        )

        style.configure(
            "Dark.Treeview",
            background="#1f2937",
            foreground="white",
            rowheight=28,
            fieldbackground="#1f2937"
        )

        style.map(
            "Dark.Treeview",
            background=[("selected", "#2563eb")]
        )

        style.configure(
            "Dark.Treeview.Heading",
            background="#111827",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )

        # ================= HEADER =================
        header = tk.Frame(self, bg=COLORS["header"], height=SIZES["header_h"])
        header.pack(fill=tk.X)

        RoundedButton(
            header,
            text="← Back",
            width=90,
            height=36,
            radius=8,
            bg=COLORS["card"],
            command=self.go_back
        ).pack(side=tk.LEFT, padx=15, pady=12)

        tk.Label(
            header,
            text="STUDENT MANAGEMENT",
            font=FONTS["title"],
            bg=COLORS["header"],
            fg=COLORS["accent"]
        ).pack(pady=(10, 0))

        tk.Label(
            header,
            text="Create, update and manage student records",
            font=FONTS["small"],
            bg=COLORS["header"],
            fg=COLORS["muted"]
        ).pack()

        # ================= VARIABLES =================
        self.var_dep = tk.StringVar(value="Select Department")
        self.var_course = tk.StringVar(value="Select Course")
        self.var_year = tk.StringVar(value="Select Year")
        self.var_sem = tk.StringVar(value="Select Semester")
        self.var_std_id = tk.StringVar()
        self.var_std_name = tk.StringVar()
        self.var_div = tk.StringVar(value="Select")
        self.var_roll = tk.StringVar()
        self.var_gender = tk.StringVar(value="Select")
        self.var_dob = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_teacher = tk.StringVar()
        self.var_radio1 = tk.StringVar(value="No")

        self.var_search_combo = tk.StringVar()
        self.var_search_txt = tk.StringVar()

        # ================= MAIN =================
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        # ================= LEFT =================
        left = tk.Frame(main, bg=COLORS["card"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        tk.Label(left, text="▌ Student Details",
                 bg=COLORS["card"], fg=COLORS["text"],
                 font=FONTS["card"]).pack(anchor="w", padx=20, pady=15)

        # ---------- COURSE ----------
        course = tk.Frame(left, bg=COLORS["card_hover"])
        course.pack(fill=tk.X, padx=20, pady=(0, 15))

        tk.Label(course, text="Current Course",
                 bg=COLORS["card_hover"], fg=COLORS["accent"],
                 font=FONTS["section"]).grid(
            row=0, column=0, columnspan=4, padx=10, pady=12, sticky="w"
        )

        fields = [
            ("Department", self.var_dep, ("Select Department", "MCA", "BCA", "IT")),
            ("Course", self.var_course, ("Select Course", "MCA", "BCA", "CS")),
            ("Year", self.var_year, ("2024-25", "2025-26")),
            ("Semester", self.var_sem, ("Sem-1", "Sem-2")),
        ]

        for i, (lbl, var, values) in enumerate(fields):
            r, c = divmod(i, 2)
            tk.Label(course, text=lbl, bg=COLORS["card_hover"], fg="white")\
                .grid(row=r+1, column=c*2, padx=10, pady=6, sticky="w")
            ttk.Combobox(
                course, textvariable=var, values=values,
                style="Dark.TCombobox", state="readonly", width=18
            ).grid(row=r+1, column=c*2+1, pady=6)

        # ---------- STUDENT INFO ----------
        info = tk.Frame(left, bg=COLORS["card_hover"])
        info.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        tk.Label(info, text="Class Student Information",
                 bg=COLORS["card_hover"], fg=COLORS["accent"],
                 font=FONTS["section"]).grid(
            row=0, column=0, columnspan=4, padx=10, pady=12, sticky="w"
        )

        entries = [
            ("Std ID", self.var_std_id),
            ("Name", self.var_std_name),
            ("Division", self.var_div),
            ("Roll No", self.var_roll),
            ("Gender", self.var_gender),
            ("DOB", self.var_dob),
            ("Email", self.var_email),
            ("Mobile", self.var_phone),
            ("Address", self.var_address),
            ("Tutor", self.var_teacher),
        ]

        row = 1
        for i in range(0, len(entries), 2):
            tk.Label(info, text=entries[i][0], bg=COLORS["card_hover"], fg="white")\
                .grid(row=row, column=0, padx=10, pady=6, sticky="w")

            if entries[i][0] == "Division":
                ttk.Combobox(info, textvariable=self.var_div,
                             values=("Select", "A", "B", "C"),
                             style="Dark.TCombobox", state="readonly", width=18)\
                    .grid(row=row, column=1)
            elif entries[i][0] == "Gender":
                ttk.Combobox(info, textvariable=self.var_gender,
                             values=("Select", "Male", "Female", "Other"),
                             style="Dark.TCombobox", state="readonly", width=18)\
                    .grid(row=row, column=1)
            else:
                ttk.Entry(info, textvariable=entries[i][1],
                          style="Dark.TEntry", width=20)\
                    .grid(row=row, column=1)

            tk.Label(info, text=entries[i+1][0], bg=COLORS["card_hover"], fg="white")\
                .grid(row=row, column=2, padx=10, sticky="w")
            ttk.Entry(info, textvariable=entries[i+1][1],
                      style="Dark.TEntry", width=20)\
                .grid(row=row, column=3)

            row += 1

        # ---------- RADIO ----------
        radio = tk.Frame(info, bg=COLORS["card_hover"])
        radio.grid(row=row, column=0, columnspan=4, pady=10)

        ttk.Radiobutton(
            radio, text="Take Photo Sample",
            variable=self.var_radio1, value="Yes",
            command=self.start_camera_preview
        ).pack(side=tk.LEFT, padx=15)

        ttk.Radiobutton(
            radio, text="No Photo Sample",
            variable=self.var_radio1, value="No",
            command=self.stop_camera_preview
        ).pack(side=tk.LEFT)

        # ---------- CAMERA PREVIEW ----------
        preview = tk.Frame(left, bg="#020617", height=220,
                           highlightthickness=1, highlightbackground="#334155")
        preview.pack(fill="x", padx=20, pady=(5, 15))
        preview.pack_propagate(False)

        tk.Label(preview, text="Camera Preview",
                 bg="#020617", fg="#94a3b8").pack(anchor="w", padx=10, pady=5)

        self.camera_label = tk.Label(preview, bg="#020617")
        self.camera_label.pack(expand=True)

        # ---------- ACTION BUTTONS ----------
        btns = tk.Frame(left, bg=COLORS["card_hover"])
        btns.pack(fill=tk.X, padx=20, pady=15)

        actions = [
            ("Save", self.add_data, BUTTONS["primary"]),
            ("Update", self.update_data, BUTTONS["primary"]),
            ("Delete", self.delete_data, BUTTONS["danger"]),
            ("Reset", self.reset_data, BUTTONS["secondary"]),
            ("Take Pic", self.generate_dataset, BUTTONS["primary"]),
        ]

        for i, (txt, cmd, color) in enumerate(actions):
            RoundedButton(
                btns, text=txt, command=cmd,
                width=130, height=40, radius=10,
                bg=color
            ).grid(row=i//3, column=i % 3, padx=10, pady=10)

        # ================= RIGHT =================
        right = tk.Frame(main, bg=COLORS["card"])
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        tk.Label(right, text="▌ Student Records",
                 bg=COLORS["card"], fg=COLORS["text"],
                 font=FONTS["card"]).pack(anchor="w", padx=20, pady=15)

        search = tk.Frame(right, bg=COLORS["card_hover"])
        search.pack(fill=tk.X, padx=20)

        ttk.Combobox(search, textvariable=self.var_search_combo,
                     values=("Student_ID", "Roll_No"),
                     style="Dark.TCombobox", state="readonly", width=18)\
            .grid(row=0, column=0, padx=10, pady=10)

        ttk.Entry(search, textvariable=self.var_search_txt,
                  style="Dark.TEntry", width=28)\
            .grid(row=0, column=1, pady=10)

        RoundedButton(search, text="Search", width=110, height=36,
                      radius=8, bg=BUTTONS["primary"],
                      command=self.search_data)\
            .grid(row=0, column=2, padx=6)

        RoundedButton(search, text="Show All", width=110, height=36,
                      radius=8, bg=BUTTONS["secondary"],
                      command=self.fetch_data)\
            .grid(row=0, column=3, padx=6)

        table_frame = tk.Frame(right, bg=COLORS["card_hover"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "dep", "course", "year", "sem"),
            show="headings",
            style="Dark.Treeview"
        )
        self.student_table.pack(fill=tk.BOTH, expand=True)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

        for col, txt in {
            "id": "Student ID",
            "name": "Name",
            "dep": "Department",
            "course": "Course",
            "year": "Year",
            "sem": "Semester"
        }.items():
            self.student_table.heading(col, text=txt)
            self.student_table.column(col, width=140)

        self.fetch_data()

    # ================= CAMERA =================
    def start_camera_preview(self):
        if self.cap and self.cap.isOpened():
            return

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        def update():
            if not self.cap or not self.cap.isOpened():
                return
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (300, 180))
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.camera_label.img = img
                self.camera_label.config(image=img)
            self.after(30, update)

        update()

    def stop_camera_preview(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.cap = None
        self.camera_label.config(image="")

    def go_back(self):
        self.stop_camera_preview()
        self.controller.show_page_by_name("Dashboard")

    # ================= DATABASE =================
    def fetch_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="park12",
            database="face_recognition"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        self.student_table.delete(*self.student_table.get_children())
        for r in rows:
            self.student_table.insert("", tk.END, values=r[:6])

        conn.close()

    def search_data(self):
        if not self.var_search_combo.get():
            messagebox.showerror("Error", "Select Search Category")
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="park12",
            database="face_recognition"
        )
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM student WHERE {self.var_search_combo.get()} LIKE '%{self.var_search_txt.get()}%'"
        )
        rows = cur.fetchall()

        self.student_table.delete(*self.student_table.get_children())
        for r in rows:
            self.student_table.insert("", tk.END, values=r[:6])

        conn.close()

    def get_cursor(self, _=None):
        row = self.student_table.focus()
        data = self.student_table.item(row)["values"]
        if not data:
            return

        self.var_std_id.set(data[0])
        self.var_std_name.set(data[1])
        self.var_dep.set(data[2])
        self.var_course.set(data[3])
        self.var_year.set(data[4])
        self.var_sem.set(data[5])

    def reset_data(self):
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_sem.set("Select Semester")
        self.var_div.set("Select")
        self.var_roll.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("No")
        self.stop_camera_preview()

    def add_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self )
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="park12", database="face_recognition")
                my_cursor = conn.cursor()
                query = ("INSERT INTO student (Student_ID, Name, Department, Course, Year, Semester, "
                         "Division, Gender, DOB, Mobile_No, Address, Roll_No, Email, Teacher_Name, PhotoSample) "
                         "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                
                values = (self.var_std_id.get(), self.var_std_name.get(), self.var_dep.get(), self.var_course.get(), self.var_year.get(), self.var_sem.get(), self.var_div.get(), self.var_gender.get(), self.var_dob.get(), self.var_phone.get(), self.var_address.get(), self.var_roll.get(), self.var_email.get(), self.var_teacher.get(), self.var_radio1.get())

                my_cursor.execute(query, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Student details added Successfully")
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}")
    def update_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="park12", database="face_recognition")
            my_cursor = conn.cursor()
            my_cursor.execute("UPDATE student SET Name=%s, Department=%s, Course=%s, Year=%s, Semester=%s, Division=%s, Gender=%s, DOB=%s, Mobile_No=%s, Address=%s, Roll_No=%s, Email=%s, Teacher_Name=%s, PhotoSample=%s WHERE Student_ID=%s", (
                self.var_std_name.get(), self.var_dep.get(), self.var_course.get(), self.var_year.get(), self.var_sem.get(), self.var_div.get(), self.var_gender.get(), self.var_dob.get(), self.var_phone.get(), self.var_address.get(), self.var_roll.get(), self.var_email.get(), self.var_teacher.get(), self.var_radio1.get(), self.var_std_id.get()
            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Student updated successfully")
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}")

    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="park12", database="face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute("DELETE FROM student WHERE Student_ID=%s", (self.var_std_id.get(),))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete", "Student deleted successfully")
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}")

    def reset_data(self):
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_sem.set("Select Semester")
        self.var_div.set("Select")
        self.var_roll.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")


    def generate_dataset(self):
        # ================= VALIDATION =================
        if self.var_std_id.get() == "" or self.var_std_name.get() == "":
            messagebox.showerror(
                "Error",
                "Student ID and Name are required!",
                parent=self
            )
            return

        try:
            # ================= DATABASE UPDATE =================
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="park12",
                database="face_recognition",
                port=3306
            )
            cursor = conn.cursor()

            sql = (
                "UPDATE student SET Name=%s, Department=%s, Course=%s, Year=%s, "
                "Semester=%s, Division=%s, Gender=%s, DOB=%s, Mobile_No=%s, "
                "Address=%s, Roll_No=%s, Email=%s, Teacher_Name=%s, PhotoSample=%s "
                "WHERE Student_ID=%s"
            )

            values = (
                self.var_std_name.get(),
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_sem.get(),
                self.var_div.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_phone.get(),
                self.var_address.get(),
                self.var_roll.get(),
                self.var_email.get(),
                self.var_teacher.get(),
                "Yes",
                self.var_std_id.get()
            )

            cursor.execute(sql, values)
            conn.commit()
            conn.close()

            # ================= FACE CLASSIFIER =================
            face_classifier = cv2.CascadeClassifier(
                "models/haarcascade_frontalface_default.xml"
            )
            if face_classifier.empty():
                messagebox.showerror(
                    "Error",
                    "Face classifier file not found!",
                    parent=self
                )
                return

            # ================= CAMERA INIT (SAFE) =================
            # Release old camera if exists (IMPORTANT for single-tab apps)
            if hasattr(self, "cap") and self.cap is not None:
                try:
                    if self.cap.isOpened():
                        self.cap.release()
                except:
                    pass

            # Force DirectShow (Windows stable backend)
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not self.cap.isOpened():
                messagebox.showerror(
                    "Camera Error",
                    "Webcam not found or currently in use by another app.",
                    parent=self
                )
                return

            cv2.waitKey(800)  # allow camera to warm up

            # ================= DATASET CAPTURE =================
            img_id = 0

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    img_id += 1

                    face_img = gray[y:y + h, x:x + w]
                    face_img = cv2.resize(face_img, (200, 200))

                    os.makedirs("data/samples", exist_ok=True)

                    path = f"data/samples/std.{self.var_std_id.get()}.{img_id}.jpg"
                    cv2.imwrite(path, face_img)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"Captured: {img_id}",
                        (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                cv2.imshow(
                    "Capturing Dataset (Press Enter to Finish)",
                    frame
                )

                if cv2.waitKey(1) == 13 or img_id >= 100:
                    break

            # ================= CLEANUP =================
            self.cap.release()
            cv2.destroyAllWindows()

            messagebox.showinfo(
                "Success",
                "Dataset generated successfully!",
                parent=self
            )

        except Exception as e:
            try:
                if hasattr(self, "cap") and self.cap.isOpened():
                    self.cap.release()
                cv2.destroyAllWindows()
            except:
                pass

            messagebox.showerror(
                "Error",
                f"Error occurred:\n{str(e)}",
                parent=self
            )
