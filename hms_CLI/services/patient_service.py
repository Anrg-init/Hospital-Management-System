from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty, validate_positive_number
from auth.session import get_user


def add_patient():
    user = get_user()

    if user["role"] not in ["admin", "receptionist"]:
        print("Access denied!")
        return

    name = input("Name: ")
    if not validate_non_empty(name, "name"):
        return

    age = input("Age: ")
    if not validate_positive_number(age, "age"):
        return

    gender = input("Gender: ")
    disease = input("Disease: ")
    contact = input("Contact: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        # check duplicate
        cur.execute(
            "SELECT 1 FROM patients WHERE name=%s OR contact=%s",
            (name, contact)
        )
        if cur.fetchone():
            print("Patient already exists!")
            return

        pid = generate_id()

        cur.execute(
            "INSERT INTO patients (id, name, age, gender, disease, contact) VALUES (%s,%s,%s,%s,%s,%s)",
            (pid, name, int(age), gender, disease, contact)
        )

        conn.commit()
        print("Patient added successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def view_patients():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM patients")
        data = cur.fetchall()

        if not data:
            print("No patients found!")
            return

        for p in data:
            print(f"""
ID       : {p[0]}
Name     : {p[1]}
Age      : {p[2]}
Gender   : {p[3]}
Disease  : {p[4]}
Contact  : {p[5]}
----------------------------""")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def update_patient():
    user = get_user()

    if user["role"] not in ["admin", "receptionist"]:
        print("Access denied!")
        return

    pid = input("Enter Patient ID to update: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
        p = cur.fetchone()

        if not p:
            print("Patient not found!")
            return

        print(f"Updating {p[1]}. Leave blank to keep current value.")

        new_name    = input(f"New Name [{p[1]}]: ")    or p[1]
        new_age     = input(f"New Age [{p[2]}]: ")     or p[2]
        new_gender  = input(f"New Gender [{p[3]}]: ")  or p[3]
        new_disease = input(f"New Disease [{p[4]}]: ") or p[4]
        new_contact = input(f"New Contact [{p[5]}]: ") or p[5]

        cur.execute("""
            UPDATE patients
            SET name=%s, age=%s, gender=%s, disease=%s, contact=%s
            WHERE id=%s
        """, (new_name, int(new_age), new_gender, new_disease, new_contact, pid))

        conn.commit()
        print("Patient updated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def delete_patient():
    user = get_user()

    if user["role"] != "admin":
        print("Only admin can delete!")
        return

    pid = input("Enter Patient ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT 1 FROM patients WHERE id=%s", (pid,))
        if not cur.fetchone():
            print("Patient not found!")
            return

        cur.execute("DELETE FROM patients WHERE id=%s", (pid,))
        conn.commit()
        print("Patient deleted successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def search_patient():
    keyword = input("Enter name or patient ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM patients WHERE name ILIKE %s OR id=%s",
            (f"%{keyword}%", keyword)
        )
        data = cur.fetchall()

        if not data:
            print("No patients found!")
            return

        for p in data:
            print(f"""
ID       : {p[0]}
Name     : {p[1]}
Age      : {p[2]}
Gender   : {p[3]}
Disease  : {p[4]}
Contact  : {p[5]}
----------------------------""")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()