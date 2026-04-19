import tkinter as tk
from tkinter import ttk, messagebox
from services.patient_service import (
    _add_patient,
    _update_patient,
    _delete_patient,
    _search_patient,
    get_all_patients
)
from auth.session import get_user


class PatientPage(tk.Frame):
    def __init__(self, root, router):
        super().__init__(root)
        self.router = router
        self.user = get_user()

        # ── top header ──────────────────────────────────────────────
        header = tk.Frame(self, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text="Patient Management", font=("Arial", 16, "bold"),
                 bg="#2c3e50", fg="white").pack(side="left", padx=15, pady=10)
        tk.Button(header, text="Back to Dashboard", bg="#34495e", fg="white",
                  relief="flat", command=lambda: router.show("dashboard")
                  ).pack(side="right", padx=15, pady=10)

        # ── tabs ─────────────────────────────────────────────────────
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_add        = tk.Frame(self.tabs)
        self.tab_view       = tk.Frame(self.tabs)
        self.tab_search     = tk.Frame(self.tabs)
        self.tab_update     = tk.Frame(self.tabs)
        self.tab_delete     = tk.Frame(self.tabs)

        self.tabs.add(self.tab_add,    text="  Add  ")
        self.tabs.add(self.tab_view,   text="  View  ")
        self.tabs.add(self.tab_search, text="  Search  ")
        self.tabs.add(self.tab_update, text="  Update  ")

        # delete tab only for admin
        if self.user["role"] == "admin":
            self.tabs.add(self.tab_delete, text="  Delete  ")

        self._build_add_tab()
        self._build_view_tab()
        self._build_search_tab()
        self._build_update_tab()
        if self.user["role"] == "admin":
            self._build_delete_tab()

    # ── helpers ──────────────────────────────────────────────────────

    def _form_row(self, parent, label, row, show=None):
        tk.Label(parent, text=label, anchor="w").grid(
            row=row, column=0, sticky="w", padx=10, pady=6)
        entry = tk.Entry(parent, width=30, show=show or "")
        entry.grid(row=row, column=1, padx=10, pady=6)
        return entry

    def _status_label(self, parent):
        lbl = tk.Label(parent, text="", font=("Arial", 10))
        lbl.pack(pady=5)
        return lbl

    def _show_status(self, label, message, success=True):
        label.config(
            text=message,
            fg="#27ae60" if success else "#e74c3c"
        )

    def _populate_tree(self, tree, data):
        for row in tree.get_children():
            tree.delete(row)
        for p in data:
            tree.insert("", "end", values=p)

    def _make_tree(self, parent):
        cols = ("ID", "Name", "Age", "Gender", "Disease", "Contact")
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scroll = tk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            yscrollcommand=scroll.set)
        scroll.config(command=tree.yview)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        tree.pack(fill="both", expand=True)
        return tree

    # ── ADD TAB ──────────────────────────────────────────────────────

    def _build_add_tab(self):
        tk.Label(self.tab_add, text="Add New Patient",
                 font=("Arial", 13, "bold")).pack(pady=15)

        form = tk.Frame(self.tab_add)
        form.pack()

        self.add_name    = self._form_row(form, "Name",    0)
        self.add_age     = self._form_row(form, "Age",     1)
        self.add_gender  = self._form_row(form, "Gender",  2)
        self.add_disease = self._form_row(form, "Disease", 3)
        self.add_contact = self._form_row(form, "Contact", 4)

        self.add_status = self._status_label(self.tab_add)

        tk.Button(self.tab_add, text="Add Patient",
                  command=self._handle_add).pack(pady=5)

    def _handle_add(self):
        name    = self.add_name.get().strip()
        age     = self.add_age.get().strip()
        gender  = self.add_gender.get().strip()
        disease = self.add_disease.get().strip()
        contact = self.add_contact.get().strip()

        if not all([name, age, gender, disease, contact]):
            self._show_status(self.add_status, "All fields are required.", False)
            return

        if not age.isdigit() or int(age) <= 0:
            self._show_status(self.add_status, "Age must be a positive number.", False)
            return

        result = _add_patient(name, age, gender, disease, contact)
        self._show_status(self.add_status, result["message"], result["success"])

        if result["success"]:
            for e in [self.add_name, self.add_age, self.add_gender,
                      self.add_disease, self.add_contact]:
                e.delete(0, tk.END)

    # ── VIEW TAB ─────────────────────────────────────────────────────

    def _build_view_tab(self):
        tk.Button(self.tab_view, text="Refresh",
                  command=self._handle_view).pack(pady=10)
        self.view_tree = self._make_tree(self.tab_view)
        self._handle_view()

    def _handle_view(self):
        data = get_all_patients()
        self._populate_tree(self.view_tree, data)

    # ── SEARCH TAB ───────────────────────────────────────────────────

    def _build_search_tab(self):
        top = tk.Frame(self.tab_search)
        top.pack(pady=15)

        tk.Label(top, text="Name or ID:").pack(side="left", padx=5)
        self.search_entry = tk.Entry(top, width=25)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(top, text="Search",
                  command=self._handle_search).pack(side="left", padx=5)

        self.search_status = self._status_label(self.tab_search)
        self.search_tree = self._make_tree(self.tab_search)

    def _handle_search(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self._show_status(self.search_status, "Enter a name or ID.", False)
            return
        data = _search_patient(keyword)
        if not data:
            self._show_status(self.search_status, "No patients found.", False)
        else:
            self._show_status(self.search_status, f"{len(data)} patient(s) found.", True)
        self._populate_tree(self.search_tree, data)

    # ── UPDATE TAB ───────────────────────────────────────────────────

    def _build_update_tab(self):
        top = tk.Frame(self.tab_update)
        top.pack(pady=10)

        tk.Label(top, text="Patient ID:").pack(side="left", padx=5)
        self.update_pid_entry = tk.Entry(top, width=20)
        self.update_pid_entry.pack(side="left", padx=5)
        tk.Button(top, text="Load",
                  command=self._handle_load).pack(side="left", padx=5)

        self.update_status = self._status_label(self.tab_update)

        form = tk.Frame(self.tab_update)
        form.pack()

        self.upd_name    = self._form_row(form, "Name",    0)
        self.upd_age     = self._form_row(form, "Age",     1)
        self.upd_gender  = self._form_row(form, "Gender",  2)
        self.upd_disease = self._form_row(form, "Disease", 3)
        self.upd_contact = self._form_row(form, "Contact", 4)

        tk.Button(self.tab_update, text="Update Patient",
                  command=self._handle_update).pack(pady=10)

    def _handle_load(self):
        pid = self.update_pid_entry.get().strip()
        if not pid:
            self._show_status(self.update_status, "Enter a Patient ID.", False)
            return

        from database.connection import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
        p = cur.fetchone()
        cur.close()
        conn.close()

        if not p:
            self._show_status(self.update_status, "Patient not found.", False)
            return

        # fill fields with current values
        for entry, val in zip(
            [self.upd_name, self.upd_age, self.upd_gender,
             self.upd_disease, self.upd_contact],
            [p[1], p[2], p[3], p[4], p[5]]
        ):
            entry.delete(0, tk.END)
            entry.insert(0, str(val))

        self._show_status(self.update_status, f"Loaded: {p[1]}", True)

    def _handle_update(self):
        pid = self.update_pid_entry.get().strip()
        if not pid:
            self._show_status(self.update_status, "Load a patient first.", False)
            return

        name    = self.upd_name.get().strip()
        age     = self.upd_age.get().strip()
        gender  = self.upd_gender.get().strip()
        disease = self.upd_disease.get().strip()
        contact = self.upd_contact.get().strip()

        result = _update_patient(pid, name, age, gender, disease, contact)
        self._show_status(self.update_status, result["message"], result["success"])

    # ── DELETE TAB ───────────────────────────────────────────────────

    def _build_delete_tab(self):
        tk.Label(self.tab_delete, text="Delete Patient (Admin Only)",
                 font=("Arial", 13, "bold"), fg="#e74c3c").pack(pady=15)

        top = tk.Frame(self.tab_delete)
        top.pack()

        tk.Label(top, text="Patient ID:").pack(side="left", padx=5)
        self.delete_pid_entry = tk.Entry(top, width=20)
        self.delete_pid_entry.pack(side="left", padx=5)

        self.delete_status = self._status_label(self.tab_delete)

        tk.Button(self.tab_delete, text="Delete Patient",
                  fg="white", bg="#e74c3c",
                  command=self._handle_delete).pack(pady=10)

    def _handle_delete(self):
        pid = self.delete_pid_entry.get().strip()
        if not pid:
            self._show_status(self.delete_status, "Enter a Patient ID.", False)
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete patient {pid}?"
        )
        if not confirm:
            return

        result = _delete_patient(pid)
        self._show_status(self.delete_status, result["message"], result["success"])
        if result["success"]:
            self.delete_pid_entry.delete(0, tk.END)