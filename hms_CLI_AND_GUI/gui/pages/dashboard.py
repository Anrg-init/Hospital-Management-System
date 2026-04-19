import tkinter as tk
from auth.session import get_user, set_user


class Dashboard(tk.Frame):
    def __init__(self, root, router):
        super().__init__(root)
        self.router = router
        user = get_user()

        header = tk.Frame(self, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text="Hospital Management System",
                 font=("Arial", 16, "bold"),
                 bg="#2c3e50", fg="white").pack(side="left", padx=15, pady=12)
        tk.Label(header, text=f"{user['username']} ({user['role']})",
                 bg="#2c3e50", fg="#bdc3c7").pack(side="right", padx=15)

        tk.Label(self, text="Dashboard",
                 font=("Arial", 14)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Patients", width=20, height=2,
                  command=lambda: router.show("patients")).grid(
                  row=0, column=0, padx=10, pady=8)
        tk.Button(btn_frame, text="Doctors", width=20, height=2,
                  command=lambda: router.show("doctors")).grid(
                  row=0, column=1, padx=10, pady=8)
        tk.Button(btn_frame, text="Appointments", width=20, height=2,
                  command=lambda: router.show("appointments")).grid(
                  row=1, column=0, padx=10, pady=8)
        tk.Button(btn_frame, text="Billing", width=20, height=2,
                  command=lambda: router.show("billing")).grid(
                  row=1, column=1, padx=10, pady=8)

        tk.Button(self, text="Logout", fg="red", width=15,
                  command=self.handle_logout).pack(pady=20)

    def handle_logout(self):
        set_user(None)
        self.router.show("login")