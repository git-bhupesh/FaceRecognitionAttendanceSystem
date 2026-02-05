
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime, timedelta
import csv
import os
from ui.buttons import RoundedButton
from config import COLORS, FONTS, BUTTONS
import tkinter as tk
class Attendance(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["bg"])
        # self.build_ui()

        # ================= VARIABLES =================
        self.filter_var = StringVar(value="ALL")
        self.search_var = StringVar()

        # ================= HEADER =================
        header = Frame(self , bg=COLORS["header"], height=70)
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
            header,
            text="ATTENDANCE MANAGEMENT",
            font=FONTS["title"],
            bg=COLORS["header"],
            fg=COLORS["accent"]
        ).pack(pady=(8, 0))

        Label(
            header,
            text="View, export and manage attendance records",
            font=FONTS["small"],
            bg=COLORS["header"],
            fg=COLORS["muted"]
        ).pack()

        # ================= MAIN =================
        main = Frame(self , bg=COLORS["bg"])
        main.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # ================= LEFT CONTROLS =================
        control = Frame(main, bg=COLORS["card"], width=280)
        control.pack(side=LEFT, fill=Y, padx=(0, 15))
        control.pack_propagate(False)

        Label(
            control, text="Controls",
            font=FONTS["card"],
            bg=COLORS["card"],
            fg=COLORS["text"]
        ).pack(anchor=W, padx=20, pady=15)

        Label(control, text="Date Filter", bg=COLORS["card"], fg=COLORS["text"]).pack(anchor=W, padx=20)

        Radiobutton(control, text="Today", variable=self.filter_var, value="TODAY",
                    bg=COLORS["card"], fg=COLORS["text"]).pack(anchor=W, padx=30)
        Radiobutton(control, text="Yesterday", variable=self.filter_var, value="YESTERDAY",
                    bg=COLORS["card"], fg=COLORS["text"]).pack(anchor=W, padx=30)
        Radiobutton(control, text="All", variable=self.filter_var, value="ALL",
                    bg=COLORS["card"], fg=COLORS["text"]).pack(anchor=W, padx=30)

        Label(control, text="Search Student", bg=COLORS["card"], fg=COLORS["text"]).pack(anchor=W, padx=20, pady=(20,5))
        Entry(control, textvariable=self.search_var).pack(fill=X, padx=20)

        RoundedButton(
            control,
            text="Apply Filter",
            width=220,
            height=44,
            radius=10,
            bg=BUTTONS["primary"],
            command=self.fetch_data
        ).pack(fill=tk.X, padx=20, pady=10)

        RoundedButton(
            control,
            text="Export to CSV",
            width=220,
            height=44,
            radius=10,
            bg=BUTTONS["secondary"],
            command=self.export_csv
        ).pack(fill=tk.X, padx=20, pady=5)

        RoundedButton(
            control,
            text="Reset View",
            width=220,
            height=44,
            radius=10,
            bg=BUTTONS["danger"],
            command=self.reset_view
        ).pack(fill=tk.X, padx=20, pady=15)

        # ================= RIGHT TABLE =================
        table_card = Frame(main, bg=COLORS["card"])
        table_card.pack(side=RIGHT, fill=BOTH, expand=True)

        Label(
            table_card, text="Attendance Records",
            font=FONTS["card"],
            bg=COLORS["card"],
            fg=COLORS["text"]
        ).pack(anchor=W, padx=20, pady=15)

        table_frame = Frame(table_card)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0,20))
        
        # ================= TREEVIEW DARK THEME =================
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Dark.Treeview",
            background=COLORS["card_hover"],
            foreground="white",
            rowheight=32,
            fieldbackground=COLORS["card_hover"],
            borderwidth=0
        )

        style.configure(
            "Dark.Treeview.Heading",
            background=COLORS["header"],
            foreground=COLORS["accent"],
            font=("Segoe UI", 11, "bold")
        )

        style.map(
            "Dark.Treeview",
            background=[("selected", COLORS["accent"])],
            foreground=[("selected", "black")]
        )


        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.table = ttk.Treeview(
                        table_frame,
                        columns=("id","roll","name","time","date","status"),
                        yscrollcommand=scroll_y.set,
                        show="headings",
                        style="Dark.Treeview"
                    )


        scroll_y.pack(side=RIGHT, fill=Y)
        self.table.pack(fill=BOTH, expand=True)
        scroll_y.config(command=self.table.yview)

        for col, txt in {
            "id":"Student ID",
            "roll":"Roll No",
            "name":"Name",
            "time":"Time",
            "date":"Date",
            "status":"Status"
        }.items():
            self.table.heading(col, text=txt)
            self.table.column(col, anchor=W, width=150)

        self.fetch_data()

    # ================= DATABASE =================
    def fetch_data(self):
        self.table.delete(*self.table.get_children())

        conn = mysql.connector.connect(
            host="localhost", user="root",
            password="park12", database="face_recognition"
        )
        cur = conn.cursor()

        base_query = "SELECT std_id, std_roll_no, std_name, std_time, std_date, std_attendance FROM stdattendance"
        params = []

        # Date filter
        if self.filter_var.get() == "TODAY":
            today = datetime.now().strftime("%d/%m/%Y")
            base_query += " WHERE std_date=%s"
            params.append(today)

        elif self.filter_var.get() == "YESTERDAY":
            yest = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
            base_query += " WHERE std_date=%s"
            params.append(yest)

        # Search filter
        if self.search_var.get():
            if "WHERE" in base_query:
                base_query += " AND"
            else:
                base_query += " WHERE"
            base_query += " (std_id LIKE %s OR std_roll_no LIKE %s OR std_name LIKE %s)"
            s = f"%{self.search_var.get()}%"
            params.extend([s, s, s])

        cur.execute(base_query, params)
        rows = cur.fetchall()
        conn.close()

        # for row in rows:
        #     self.table.insert("", END, values=row)
        
        for row in rows:
            self.table.insert("", "end", values=tuple(row))

    # ================= EXPORT =================
    def export_csv(self):
        rows = self.table.get_children()
        if not rows:
            messagebox.showerror("Error", "No data to export")
            return

        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file:
            return

        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","Roll","Name","Time","Date","Status"])
            for r in rows:
                writer.writerow(self.table.item(r)["values"])

        messagebox.showinfo("Success", "Attendance exported successfully")

    def reset_view(self):
        self.filter_var.set("ALL")
        self.search_var.set("")
        self.fetch_data()

