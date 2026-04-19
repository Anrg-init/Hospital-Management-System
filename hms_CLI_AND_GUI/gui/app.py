import tkinter as tk
from gui.router import Router


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1000x600")
        self.minsize(800, 500)
        self.resizable(True, True)
        self.router = Router(self)
        self.router.show("login")


if __name__ == "__main__":
    app = App()
    app.mainloop()