import uuid


def generate_id():
    return str(uuid.uuid4())[:8]


def validate_non_empty(value, field):
    if not value.strip():
        print(f"{field} cannot be empty!")
        return False
    return True


def validate_positive_number(value, field):
    try:
        val = float(value)
        if val <= 0:
            raise ValueError
        return val
    except:
        print(f"{field} must be a positive number!")
        return None


def print_patient(p):
    print(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Disease: {p['disease']} | Contact: {p['contact']}")


def print_doctor(d):
    print(f"ID: {d['id']} | Name: {d['name']} | Specialization: {d['specialization']} | Availability: {d['availability']}")


def print_appointment(a):
    print(f"ID: {a['id']} | Patient: {a['patient_id']} | Doctor: {a['doctor_id']} | Date: {a['date']} | Time: {a['time']}")


def print_bill(b):
    print(f"ID: {b['id']} | Patient: {b['patient_id']} | Amount: {b['amount']} | Status: {b['status']}")