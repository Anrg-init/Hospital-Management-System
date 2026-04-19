from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty
from auth.session import get_user


# ─── CORE FUNCTIONS (GUI calls these) ────────────────────────────────

def _add_appointment(pid, did, date, time):
    user = get_user()
    if user["role"] not in ["admin", "receptionist"]:
        return {"success": False, "message": "Access denied"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM patients WHERE id=%s", (pid,))
        if not cur.fetchone():
            return {"success": False, "message": "Invalid patient"}

        cur.execute("SELECT 1 FROM doctors WHERE id=%s", (did,))
        if not cur.fetchone():
            return {"success": False, "message": "Invalid doctor"}

        cur.execute("""
            SELECT 1 FROM appointments
            WHERE doctor_id=%s AND date=%s AND time=%s
        """, (did, date, time))
        if cur.fetchone():
            return {"success": False, "message": "Doctor already booked at this time"}

        aid = generate_id()
        cur.execute("""
            INSERT INTO appointments (id, patient_id, doctor_id, date, time)
            VALUES (%s,%s,%s,%s,%s)
        """, (aid, pid, did, date, time))
        conn.commit()
        return {"success": True, "message": "Appointment created successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def get_all_appointments():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM appointments")
        data = cur.fetchall()
        return data if data else []
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()


def _delete_appointment(aid):
    user = get_user()
    if user["role"] not in ["admin", "receptionist"]:
        return {"success": False, "message": "Access denied"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM appointments WHERE id=%s", (aid,))
        if not cur.fetchone():
            return {"success": False, "message": "Appointment not found"}

        cur.execute("DELETE FROM appointments WHERE id=%s", (aid,))
        conn.commit()
        return {"success": True, "message": "Appointment deleted successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def _search_appointment(keyword):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT * FROM appointments
            WHERE patient_id=%s OR doctor_id=%s
        """, (keyword, keyword))
        data = cur.fetchall()
        return data if data else []
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()


# ─── CLI WRAPPERS (menu.py calls these) ──────────────────────────────

def add_appointment():
    pid = input("Patient ID: ")
    if not validate_non_empty(pid, "patient id"): return

    did = input("Doctor ID: ")
    if not validate_non_empty(did, "doctor id"): return

    date = input("Date (YYYY-MM-DD): ")
    if not validate_non_empty(date, "date"): return

    time = input("Time (HH:MM): ")
    if not validate_non_empty(time, "time"): return

    result = _add_appointment(pid, did, date, time)
    print(result["message"])


def view_appointments():
    data = get_all_appointments()
    if not data:
        print("No appointments found!")
        return
    for a in data:
        print(f"""
ID         : {a[0]}
Patient ID : {a[1]}
Doctor ID  : {a[2]}
Date       : {a[3]}
Time       : {a[4]}
----------------------------""")


def delete_appointment():
    aid = input("Enter Appointment ID: ")
    result = _delete_appointment(aid)
    print(result["message"])


def search_appointment():
    keyword = input("Enter Patient ID or Doctor ID: ")
    data = _search_appointment(keyword)
    if not data:
        print("No appointments found!")
        return
    for a in data:
        print(f"""
ID         : {a[0]}
Patient ID : {a[1]}
Doctor ID  : {a[2]}
Date       : {a[3]}
Time       : {a[4]}
----------------------------""")