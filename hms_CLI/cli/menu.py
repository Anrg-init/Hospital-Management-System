from services import patient_service, doctor_service, appointment_service, billing_service


def patient_menu():
    while True:
        print("\n--- Patient Menu ---")
        print("1 Add Patient")
        print("2 View Patients")
        print("3 Search Patient")
        print("4 Delete Patient")
        print("5 Update Patient")
        print("6 Back")

        c = input("Choice: ")

        if c == "1": patient_service.add_patient()
        elif c == "2": patient_service.view_patients()
        elif c == "3": patient_service.search_patient()
        elif c == "4": patient_service.delete_patient()
        elif c == "5": patient_service.update_patient()
        elif c == "6": break


def doctor_menu():
    while True:
        print("\n--- Doctor Menu ---")
        print("1 Add Doctor")
        print("2 View Doctors")
        print("3 Back")

        c = input("Choice: ")

        if c == "1": doctor_service.add_doctor()
        elif c == "2": doctor_service.view_doctors()
        elif c == "3": break


def appointment_menu():
    while True:
        print("\n--- Appointment Menu ---")
        print("1 Add Appointment")
        print("2 View Appointments")
        print("3 Back")

        c = input("Choice: ")

        if c == "1": appointment_service.add_appointment()
        elif c == "2": appointment_service.view_appointments()
        elif c == "3": break


def billing_menu():
    while True:
        print("\n--- Billing Menu ---")
        print("1 Create Bill")
        print("2 View Bills")
        print("3 Mark Paid")
        print("4 Back")

        c = input("Choice: ")

        if c == "1": billing_service.create_bill()
        elif c == "2": billing_service.view_bills()
        elif c == "3": billing_service.mark_paid()
        elif c == "4": break