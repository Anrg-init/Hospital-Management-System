import tkinter as tk
from auth.auth_service import register_user


class SignupPage(tk.Frame):
    def __init__(self, root, router):
        super().__init__(root)
        self.router = router

        tk.Label(self, text="Create Account",
                 font=("Arial", 16, "bold")).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Username", anchor="w").grid(
            row=0, column=0, padx=10, pady=8, sticky="w")
        self.username = tk.Entry(form, width=25)
        self.username.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(form, text="Password", anchor="w").grid(
            row=1, column=0, padx=10, pady=8, sticky="w")
        self.password = tk.Entry(form, width=25, show="*")
        self.password.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(form, text="Role", anchor="w").grid(
            row=2, column=0, padx=10, pady=8, sticky="w")
        self.role = tk.StringVar(value="receptionist")
        role_frame = tk.Frame(form)
        role_frame.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        tk.Radiobutton(role_frame, text="Admin",
                       variable=self.role, value="admin").pack(side="left")
        tk.Radiobutton(role_frame, text="Receptionist",
                       variable=self.role, value="receptionist").pack(side="left")

        self.status = tk.Label(self, text="", fg="red")
        self.status.pack(pady=5)

        tk.Button(self, text="Register", width=15,
                  command=self.handle_register).pack(pady=5)
        tk.Button(self, text="Back to Login", width=15,
                  command=lambda: router.show("login")).pack(pady=3)

    def handle_register(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        role     = self.role.get()

        if not username or not password:
            self.status.config(text="All fields required.", fg="red")
            return

        result = register_user(username, password, role)
        if result["success"]:
            self.status.config(text="Registered! Please login.", fg="green")
            self.router.show("login")
        else:
            self.status.config(text=result["message"], fg="red")