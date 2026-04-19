import tkinter as tk
from tkinter import ttk, messagebox
from services.appointment_service import (
    _add_appointment, _delete_appointment,
    _search_appointment, get_all_appointments
)
from auth.session import get_user


class AppointmentPage(tk.Frame):
    def __init__(self, root, router):
        super().__init__(root)
        self.router = router
        self.user = get_user()

        header = tk.Frame(self, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text="Appointment Management",
                 font=("Arial", 16, "bold"),
                 bg="#2c3e50", fg="white").pack(side="left", padx=15, pady=10)
        tk.Button(header, text="Back to Dashboard",
                  bg="#34495e", fg="white", relief="flat",
                  command=lambda: router.show("dashboard")).pack(
                  side="right", padx=15, pady=10)

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_add    = tk.Frame(self.tabs)
        self.tab_view   = tk.Frame(self.tabs)
        self.tab_search = tk.Frame(self.tabs)
        self.tab_delete = tk.Frame(self.tabs)

        self.tabs.add(self.tab_add,    text="  Add  ")
        self.tabs.add(self.tab_view,   text="  View  ")
        self.tabs.add(self.tab_search, text="  Search  ")
        self.tabs.add(self.tab_delete, text="  Delete  ")

        self._build_add_tab()
        self._build_view_tab()
        self._build_search_tab()
        self._build_delete_tab()

    def _form_row(self, parent, label, row):
        tk.Label(parent, text=label, anchor="w").grid(
            row=row, column=0, sticky="w", padx=10, pady=6)
        entry = tk.Entry(parent, width=30)
        entry.grid(row=row, column=1, padx=10, pady=6)
        return entry

    def _status_label(self, parent):
        lbl = tk.Label(parent, text="", font=("Arial", 10))
        lbl.pack(pady=5)
        return lbl

    def _show_status(self, label, message, success=True):
        label.config(text=message,
                     fg="#27ae60" if success else "#e74c3c")

    def _make_tree(self, parent):
        cols = ("ID", "Patient ID", "Doctor ID", "Date", "Time")
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        scroll = tk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            yscrollcommand=scroll.set)
        scroll.config(command=tree.yview)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")
        tree.pack(fill="both", expand=True)
        return tree

    def _populate_tree(self, tree, data):
        for row in tree.get_children():
            tree.delete(row)
        for a in data:
            tree.insert("", "end", values=a)

    def _build_add_tab(self):
        tk.Label(self.tab_add, text="Add New Appointment",
                 font=("Arial", 13, "bold")).pack(pady=15)
        form = tk.Frame(self.tab_add)
        form.pack()
        self.add_pid  = self._form_row(form, "Patient ID",       0)
        self.add_did  = self._form_row(form, "Doctor ID",        1)
        self.add_date = self._form_row(form, "Date (YYYY-MM-DD)", 2)
        self.add_time = self._form_row(form, "Time (HH:MM)",     3)
        self.add_status = self._status_label(self.tab_add)
        tk.Button(self.tab_add, text="Add Appointment",
                  command=self._handle_add).pack(pady=5)

    def _handle_add(self):
        pid  = self.add_pid.get().strip()
        did  = self.add_did.get().strip()
        date = self.add_date.get().strip()
        time = self.add_time.get().strip()

        if not all([pid, did, date, time]):
            self._show_status(self.add_status, "All fields required.", False)
            return

        result = _add_appointment(pid, did, date, time)
        self._show_status(self.add_status, result["message"], result["success"])
        if result["success"]:
            for e in [self.add_pid, self.add_did,
                      self.add_date, self.add_time]:
                e.delete(0, tk.END)

    def _build_view_tab(self):
        tk.Button(self.tab_view, text="Refresh",
                  command=self._handle_view).pack(pady=10)
        self.view_tree = self._make_tree(self.tab_view)
        self._handle_view()

    def _handle_view(self):
        self._populate_tree(self.view_tree, get_all_appointments())

    def _build_search_tab(self):
        top = tk.Frame(self.tab_search)
        top.pack(pady=15)
        tk.Label(top, text="Patient ID or Doctor ID:").pack(side="left", padx=5)
        self.search_entry = tk.Entry(top, width=25)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(top, text="Search",
                  command=self._handle_search).pack(side="left", padx=5)
        self.search_status = self._status_label(self.tab_search)
        self.search_tree = self._make_tree(self.tab_search)

    def _handle_search(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self._show_status(self.search_status, "Enter a Patient or Doctor ID.", False)
            return
        data = _search_appointment(keyword)
        if not data:
            self._show_status(self.search_status, "No appointments found.", False)
        else:
            self._show_status(self.search_status, f"{len(data)} appointment(s) found.", True)
        self._populate_tree(self.search_tree, data)

    def _build_delete_tab(self):
        tk.Label(self.tab_delete, text="Delete Appointment",
                 font=("Arial", 13, "bold")).pack(pady=15)
        top = tk.Frame(self.tab_delete)
        top.pack()
        tk.Label(top, text="Appointment ID:").pack(side="left", padx=5)
        self.delete_aid_entry = tk.Entry(top, width=20)
        self.delete_aid_entry.pack(side="left", padx=5)
        self.delete_status = self._status_label(self.tab_delete)
        tk.Button(self.tab_delete, text="Delete Appointment",
                  fg="white", bg="#e74c3c",
                  command=self._handle_delete).pack(pady=10)

    def _handle_delete(self):
        aid = self.delete_aid_entry.get().strip()
        if not aid:
            self._show_status(self.delete_status, "Enter an Appointment ID.", False)
            return
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete appointment {aid}?")
        if not confirm:
            return
        result = _delete_appointment(aid)
        self._show_status(self.delete_status, result["message"], result["success"])
        if result["success"]:
            self.delete_aid_entry.delete(0, tk.END)