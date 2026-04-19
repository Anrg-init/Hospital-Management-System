import tkinter as tk
from auth.auth_service import login_user
from auth.session import set_user


class LoginPage(tk.Frame):
    def __init__(self, root, router):
        super().__init__(root)
        self.router = router

        tk.Label(self, text="Hospital Management System",
                 font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="Login", font=("Arial", 14)).pack(pady=5)

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

        self.status = tk.Label(self, text="", fg="red")
        self.status.pack(pady=5)

        tk.Button(self, text="Login", width=15,
                  command=self.handle_login).pack(pady=5)
        tk.Button(self, text="Signup", width=15,
                  command=lambda: router.show("signup")).pack(pady=3)

    def handle_login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            self.status.config(text="Username and password required.")
            return

        result = login_user(username, password)
        if result["success"]:
            set_user(result["user"])
            self.router.show("dashboard")
        else:
            self.status.config(text=result["message"])