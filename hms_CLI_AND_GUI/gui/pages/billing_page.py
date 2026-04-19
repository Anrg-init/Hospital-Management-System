import tkinter as tk
from tkinter import ttk, messagebox
from services.billing_service import (
    _create_bill, _mark_paid, _delete_bill,
    _search_bill, get_all_bills
)
from auth.session import get_user


class BillingPage(tk.Frame):
    def __init__(self, root, router):
        super().__init__(root)
        self.router = router
        self.user = get_user()

        header = tk.Frame(self, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text="Billing Management",
                 font=("Arial", 16, "bold"),
                 bg="#2c3e50", fg="white").pack(side="left", padx=15, pady=10)
        tk.Button(header, text="Back to Dashboard",
                  bg="#34495e", fg="white", relief="flat",
                  command=lambda: router.show("dashboard")).pack(
                  side="right", padx=15, pady=10)

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_create = tk.Frame(self.tabs)
        self.tab_view   = tk.Frame(self.tabs)
        self.tab_search = tk.Frame(self.tabs)
        self.tab_paid   = tk.Frame(self.tabs)
        self.tab_delete = tk.Frame(self.tabs)

        self.tabs.add(self.tab_create, text="  Create  ")
        self.tabs.add(self.tab_view,   text="  View  ")
        self.tabs.add(self.tab_search, text="  Search  ")
        self.tabs.add(self.tab_paid,   text="  Mark Paid  ")
        if self.user["role"] == "admin":
            self.tabs.add(self.tab_delete, text="  Delete  ")

        self._build_create_tab()
        self._build_view_tab()
        self._build_search_tab()
        self._build_paid_tab()
        if self.user["role"] == "admin":
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
        cols = ("ID", "Patient ID", "Amount", "Status")
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        scroll = tk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            yscrollcommand=scroll.set)
        scroll.config(command=tree.yview)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor="center")
        tree.pack(fill="both", expand=True)
        return tree

    def _populate_tree(self, tree, data):
        for row in tree.get_children():
            tree.delete(row)
        for b in data:
            tree.insert("", "end", values=b)

    def _build_create_tab(self):
        tk.Label(self.tab_create, text="Create New Bill",
                 font=("Arial", 13, "bold")).pack(pady=15)
        form = tk.Frame(self.tab_create)
        form.pack()
        self.create_pid    = self._form_row(form, "Patient ID", 0)
        self.create_amount = self._form_row(form, "Amount",     1)
        self.create_status = self._status_label(self.tab_create)
        tk.Button(self.tab_create, text="Create Bill",
                  command=self._handle_create).pack(pady=5)

    def _handle_create(self):
        pid    = self.create_pid.get().strip()
        amount = self.create_amount.get().strip()

        if not pid or not amount:
            self._show_status(self.create_status, "All fields required.", False)
            return
        try:
            if float(amount) <= 0:
                raise ValueError
        except ValueError:
            self._show_status(self.create_status, "Amount must be a positive number.", False)
            return

        result = _create_bill(pid, amount)
        self._show_status(self.create_status, result["message"], result["success"])
        if result["success"]:
            self.create_pid.delete(0, tk.END)
            self.create_amount.delete(0, tk.END)

    def _build_view_tab(self):
        tk.Button(self.tab_view, text="Refresh",
                  command=self._handle_view).pack(pady=10)
        self.view_tree = self._make_tree(self.tab_view)
        self._handle_view()

    def _handle_view(self):
        self._populate_tree(self.view_tree, get_all_bills())

    def _build_search_tab(self):
        top = tk.Frame(self.tab_search)
        top.pack(pady=15)
        tk.Label(top, text="Patient ID:").pack(side="left", padx=5)
        self.search_entry = tk.Entry(top, width=25)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(top, text="Search",
                  command=self._handle_search).pack(side="left", padx=5)
        self.search_status = self._status_label(self.tab_search)
        self.search_tree = self._make_tree(self.tab_search)

    def _handle_search(self):
        pid = self.search_entry.get().strip()
        if not pid:
            self._show_status(self.search_status, "Enter a Patient ID.", False)
            return
        data = _search_bill(pid)
        if not data:
            self._show_status(self.search_status, "No bills found.", False)
        else:
            self._show_status(self.search_status, f"{len(data)} bill(s) found.", True)
        self._populate_tree(self.search_tree, data)

    def _build_paid_tab(self):
        tk.Label(self.tab_paid, text="Mark Bill as Paid",
                 font=("Arial", 13, "bold")).pack(pady=15)
        top = tk.Frame(self.tab_paid)
        top.pack()
        tk.Label(top, text="Bill ID:").pack(side="left", padx=5)
        self.paid_bid_entry = tk.Entry(top, width=20)
        self.paid_bid_entry.pack(side="left", padx=5)
        self.paid_status = self._status_label(self.tab_paid)
        tk.Button(self.tab_paid, text="Mark as Paid",
                  fg="white", bg="#27ae60",
                  command=self._handle_paid).pack(pady=10)

    def _handle_paid(self):
        bid = self.paid_bid_entry.get().strip()
        if not bid:
            self._show_status(self.paid_status, "Enter a Bill ID.", False)
            return
        result = _mark_paid(bid)
        self._show_status(self.paid_status, result["message"], result["success"])
        if result["success"]:
            self.paid_bid_entry.delete(0, tk.END)

    def _build_delete_tab(self):
        tk.Label(self.tab_delete, text="Delete Bill (Admin Only)",
                 font=("Arial", 13, "bold"), fg="#e74c3c").pack(pady=15)
        top = tk.Frame(self.tab_delete)
        top.pack()
        tk.Label(top, text="Bill ID:").pack(side="left", padx=5)
        self.delete_bid_entry = tk.Entry(top, width=20)
        self.delete_bid_entry.pack(side="left", padx=5)
        self.delete_status = self._status_label(self.tab_delete)
        tk.Button(self.tab_delete, text="Delete Bill",
                  fg="white", bg="#e74c3c",
                  command=self._handle_delete).pack(pady=10)

    def _handle_delete(self):
        bid = self.delete_bid_entry.get().strip()
        if not bid:
            self._show_status(self.delete_status, "Enter a Bill ID.", False)
            return
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete bill {bid}?")
        if not confirm:
            return
        result = _delete_bill(bid)
        self._show_status(self.delete_status, result["message"], result["success"])
        if result["success"]:
            self.delete_bid_entry.delete(0, tk.END)