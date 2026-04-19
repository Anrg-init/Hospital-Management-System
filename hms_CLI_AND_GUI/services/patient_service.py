from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty, validate_positive_number
from auth.session import get_user


# ─── CORE FUNCTIONS (GUI calls these) ────────────────────────────────

def _add_patient(name, age, gender, disease, contact):
    user = get_user()
    if user["role"] not in ["admin", "receptionist"]:
        return {"success": False, "message": "Access denied"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT 1 FROM patients WHERE name=%s OR contact=%s",
            (name, contact)
        )
        if cur.fetchone():
            return {"success": False, "message": "Patient already exists"}

        pid = generate_id()
        cur.execute(
            "INSERT INTO patients (id, name, age, gender, disease, contact) VALUES (%s,%s,%s,%s,%s,%s)",
            (pid, name, int(age), gender, disease, contact)
        )
        conn.commit()
        return {"success": True, "message": "Patient added successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def get_all_patients():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM patients")
        data = cur.fetchall()
        return data if data else []

    except Exception as e:
        return []

    finally:
        cur.close()
        conn.close()


def _update_patient(pid, name, age, gender, disease, contact):
    user = get_user()
    if user["role"] not in ["admin", "receptionist"]:
        return {"success": False, "message": "Access denied"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
        p = cur.fetchone()
        if not p:
            return {"success": False, "message": "Patient not found"}

        new_name    = name    or p[1]
        new_age     = age     or p[2]
        new_gender  = gender  or p[3]
        new_disease = disease or p[4]
        new_contact = contact or p[5]

        cur.execute("""
            UPDATE patients
            SET name=%s, age=%s, gender=%s, disease=%s, contact=%s
            WHERE id=%s
        """, (new_name, int(new_age), new_gender, new_disease, new_contact, pid))
        conn.commit()
        return {"success": True, "message": "Patient updated successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def _delete_patient(pid):
    user = get_user()
    if user["role"] != "admin":
        return {"success": False, "message": "Only admin can delete"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM patients WHERE id=%s", (pid,))
        if not cur.fetchone():
            return {"success": False, "message": "Patient not found"}

        cur.execute("DELETE FROM patients WHERE id=%s", (pid,))
        conn.commit()
        return {"success": True, "message": "Patient deleted successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def _search_patient(keyword):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM patients WHERE name ILIKE %s OR id=%s",
            (f"%{keyword}%", keyword)
        )
        data = cur.fetchall()
        return data if data else []

    except Exception as e:
        return []

    finally:
        cur.close()
        conn.close()


# ─── CLI WRAPPERS (menu.py calls these — zero changes to menu.py) ────

def add_patient():
    name = input("Name: ")
    if not validate_non_empty(name, "name"): return

    age = input("Age: ")
    if not validate_positive_number(age, "age"): return

    gender  = input("Gender: ")
    disease = input("Disease: ")
    contact = input("Contact: ")

    result = _add_patient(name, age, gender, disease, contact)
    print(result["message"])


def view_patients():
    data = get_all_patients()
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


def update_patient():
    pid = input("Enter Patient ID to update: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
    p = cur.fetchone()
    cur.close()
    conn.close()

    if not p:
        print("Patient not found!")
        return

    print(f"Updating {p[1]}. Leave blank to keep current value.")
    name    = input(f"New Name [{p[1]}]: ")
    age     = input(f"New Age [{p[2]}]: ")
    gender  = input(f"New Gender [{p[3]}]: ")
    disease = input(f"New Disease [{p[4]}]: ")
    contact = input(f"New Contact [{p[5]}]: ")

    result = _update_patient(pid, name, age, gender, disease, contact)
    print(result["message"])


def delete_patient():
    pid = input("Enter Patient ID: ")
    result = _delete_patient(pid)
    print(result["message"])


def search_patient():
    keyword = input("Enter name or patient ID: ")
    data = _search_patient(keyword)
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