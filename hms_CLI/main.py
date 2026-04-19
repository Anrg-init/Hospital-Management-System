from cli import menu as main_menu
from auth.auth_service import register, login
from auth.session import set_user


def menu():
    
    print("Enter 1: Register")
    print("Enter 2: Login")

    user_in = input("Enter value: ")

    if user_in == "1":
        register()
        user = login()
    elif user_in == "2":
        user = login()
    else:
        print("Invalid choice!")
        return

    if not user:
        return

    set_user(user)  # ✅ only set after confirmed login

    while True:
        print("""
        1. Patient Management
        2. Doctor Management
        3. Appointment Management
        4. Billing
        5. Exit
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            main_menu.patient_menu()
        elif choice == "2":
            main_menu.doctor_menu()
        elif choice == "3":
            main_menu.appointment_menu()
        elif choice == "4":
            main_menu.billing_menu()
        elif choice == "5":
            break
        else:
            print("Enter valid choice!")


if __name__ == "__main__":
    menu()