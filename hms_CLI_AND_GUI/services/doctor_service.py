from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty, validate_positive_number
from auth.session import get_user


# ─── CORE FUNCTIONS (GUI calls these) ────────────────────────────────

def _add_doctor(name, age, gender, spec, avail):
    user = get_user()
    if user["role"] != "admin":
        return {"success": False, "message": "Only admin can add doctor"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM doctors WHERE name=%s", (name,))
        if cur.fetchone():
            return {"success": False, "message": "Doctor already exists"}

        did = generate_id()
        cur.execute("""
            INSERT INTO doctors (id, name, age, gender, specialization, availability)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (did, name, int(age), gender, spec, avail))
        conn.commit()
        return {"success": True, "message": "Doctor added successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def get_all_doctors():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM doctors")
        data = cur.fetchall()
        return data if data else []
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()


def _update_doctor(did, name, age, gender, spec, avail):
    user = get_user()
    if user["role"] != "admin":
        return {"success": False, "message": "Only admin can update doctor"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM doctors WHERE id=%s", (did,))
        d = cur.fetchone()
        if not d:
            return {"success": False, "message": "Doctor not found"}

        new_name   = name   or d[1]
        new_age    = age    or d[2]
        new_gender = gender or d[3]
        new_spec   = spec   or d[4]
        new_avail  = avail  or d[5]

        cur.execute("""
            UPDATE doctors
            SET name=%s, age=%s, gender=%s, specialization=%s, availability=%s
            WHERE id=%s
        """, (new_name, int(new_age), new_gender, new_spec, new_avail, did))
        conn.commit()
        return {"success": True, "message": "Doctor updated successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def _delete_doctor(did):
    user = get_user()
    if user["role"] != "admin":
        return {"success": False, "message": "Only admin can delete doctor"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM doctors WHERE id=%s", (did,))
        if not cur.fetchone():
            return {"success": False, "message": "Doctor not found"}

        cur.execute("DELETE FROM doctors WHERE id=%s", (did,))
        conn.commit()
        return {"success": True, "message": "Doctor deleted successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def _search_doctor(keyword):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM doctors WHERE name ILIKE %s OR id=%s",
            (f"%{keyword}%", keyword)
        )
        data = cur.fetchall()
        return data if data else []
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()


# ─── CLI WRAPPERS (menu.py calls these) ──────────────────────────────

def add_doctor():
    name = input("Name: ")
    if not validate_non_empty(name, "name"): return

    age = input("Age: ")
    if not validate_positive_number(age, "age"): return

    gender = input("Gender: ")
    spec   = input("Specialization: ")
    avail  = input("Availability: ")

    result = _add_doctor(name, age, gender, spec, avail)
    print(result["message"])


def view_doctor():
    data = get_all_doctors()
    if not data:
        print("No doctors found!")
        return
    for d in data:
        print(f"""
ID             : {d[0]}
Name           : {d[1]}
Age            : {d[2]}
Gender         : {d[3]}
Specialization : {d[4]}
Availability   : {d[5]}
----------------------------""")


def update_doctor():
    did = input("Enter Doctor ID to update: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors WHERE id=%s", (did,))
    d = cur.fetchone()
    cur.close()
    conn.close()

    if not d:
        print("Doctor not found!")
        return

    print(f"Updating {d[1]}. Leave blank to keep current value.")
    name   = input(f"New Name [{d[1]}]: ")
    age    = input(f"New Age [{d[2]}]: ")
    gender = input(f"New Gender [{d[3]}]: ")
    spec   = input(f"New Specialization [{d[4]}]: ")
    avail  = input(f"New Availability [{d[5]}]: ")

    result = _update_doctor(did, name, age, gender, spec, avail)
    print(result["message"])


def delete_doctor():
    did = input("Enter Doctor ID: ")
    result = _delete_doctor(did)
    print(result["message"])


def search_doctor():
    keyword = input("Enter name or doctor ID: ")
    data = _search_doctor(keyword)
    if not data:
        print("No doctors found!")
        return
    for d in data:
        print(f"""
ID             : {d[0]}
Name           : {d[1]}
Age            : {d[2]}
Gender         : {d[3]}
Specialization : {d[4]}
Availability   : {d[5]}
----------------------------""")