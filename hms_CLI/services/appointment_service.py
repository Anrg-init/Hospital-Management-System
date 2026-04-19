from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty
from auth.session import get_user


def add_appointment():
    user = get_user()

    if user["role"] not in ["admin", "receptionist"]:
        print("Access denied!")
        return

    pid = input("Patient ID: ")
    if not validate_non_empty(pid, "patient id"):
        return

    did = input("Doctor ID: ")
    if not validate_non_empty(did, "doctor id"):
        return

    date = input("Date (YYYY-MM-DD): ")
    if not validate_non_empty(date, "date"):
        return

    time = input("Time (HH:MM): ")
    if not validate_non_empty(time, "time"):
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        # validate patient exists
        cur.execute("SELECT 1 FROM patients WHERE id=%s", (pid,))
        if not cur.fetchone():
            print("Invalid patient!")
            return

        # validate doctor exists
        cur.execute("SELECT 1 FROM doctors WHERE id=%s", (did,))
        if not cur.fetchone():
            print("Invalid doctor!")
            return

        # prevent double booking
        cur.execute("""
            SELECT 1 FROM appointments
            WHERE doctor_id=%s AND date=%s AND time=%s
        """, (did, date, time))
        if cur.fetchone():
            print("Doctor already booked at this time!")
            return

        aid = generate_id()

        cur.execute("""
            INSERT INTO appointments (id, patient_id, doctor_id, date, time)
            VALUES (%s,%s,%s,%s,%s)
        """, (aid, pid, did, date, time))

        conn.commit()
        print("Appointment created successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def view_appointments():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM appointments")
        data = cur.fetchall()

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

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def delete_appointment():
    user = get_user()

    if user["role"] not in ["admin", "receptionist"]:
        print("Access denied!")
        return

    aid = input("Enter Appointment ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT 1 FROM appointments WHERE id=%s", (aid,))
        if not cur.fetchone():
            print("Appointment not found!")
            return

        cur.execute("DELETE FROM appointments WHERE id=%s", (aid,))
        conn.commit()
        print("Appointment deleted successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def search_appointment():
    keyword = input("Enter Patient ID or Doctor ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT * FROM appointments
            WHERE patient_id=%s OR doctor_id=%s
        """, (keyword, keyword))

        data = cur.fetchall()

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

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()