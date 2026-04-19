from gui.pages.login_page import LoginPage
from gui.pages.signup_page import SignupPage
from gui.pages.dashboard import Dashboard
from gui.pages.patient_page import PatientPage
from gui.pages.doctor_page import DoctorPage
from gui.pages.appointment_page import AppointmentPage
from gui.pages.billing_page import BillingPage


class Router:
    def __init__(self, root):
        self.root = root
        self.current_frame = None

    def show(self, page_name):
        if self.current_frame is not None:
            self.current_frame.destroy()

        frame = None
        if page_name == "login":
            frame = LoginPage(self.root, self)
        elif page_name == "signup":
            frame = SignupPage(self.root, self)
        elif page_name == "dashboard":
            frame = Dashboard(self.root, self)
        elif page_name == "patients":
            frame = PatientPage(self.root, self)
        elif page_name == "doctors":
            frame = DoctorPage(self.root, self)
        elif page_name == "appointments":
            frame = AppointmentPage(self.root, self)
        elif page_name == "billing":
            frame = BillingPage(self.root, self)

        if frame:
            self.current_frame = frame
            self.current_frame.pack(fill="both", expand=True)