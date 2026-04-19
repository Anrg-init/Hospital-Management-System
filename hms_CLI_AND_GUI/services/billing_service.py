from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty, validate_positive_number
from auth.session import get_user


# ─── CORE FUNCTIONS (GUI calls these) ────────────────────────────────

def _create_bill(patient_id, amount):
    user = get_user()
    if user["role"] not in ["admin", "receptionist"]:
        return {"success": False, "message": "Access denied"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM patients WHERE id=%s", (patient_id,))
        if not cur.fetchone():
            return {"success": False, "message": "Patient not found"}

        bid = generate_id()
        cur.execute("""
            INSERT INTO bills (id, patient_id, amount, status)
            VALUES (%s,%s,%s,%s)
        """, (bid, patient_id, float(amount), "unpaid"))
        conn.commit()
        return {"success": True, "message": "Bill created successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def get_all_bills():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM bills")
        data = cur.fetchall()
        return data if data else []
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()


def _mark_paid(bid):
    user = get_user()
    if user["role"] not in ["admin", "receptionist"]:
        return {"success": False, "message": "Access denied"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM bills WHERE id=%s", (bid,))
        if not cur.fetchone():
            return {"success": False, "message": "Bill not found"}

        cur.execute("UPDATE bills SET status=%s WHERE id=%s", ("paid", bid))
        conn.commit()
        return {"success": True, "message": "Bill marked as paid"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def _delete_bill(bid):
    user = get_user()
    if user["role"] != "admin":
        return {"success": False, "message": "Only admin can delete bill"}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM bills WHERE id=%s", (bid,))
        if not cur.fetchone():
            return {"success": False, "message": "Bill not found"}

        cur.execute("DELETE FROM bills WHERE id=%s", (bid,))
        conn.commit()
        return {"success": True, "message": "Bill deleted successfully"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cur.close()
        conn.close()


def _search_bill(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM bills WHERE patient_id=%s", (patient_id,))
        data = cur.fetchall()
        return data if data else []
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()


# ─── CLI WRAPPERS (menu.py calls these) ──────────────────────────────

def create_bill():
    patient_id = input("Patient ID: ")
    if not validate_non_empty(patient_id, "patient id"): return

    amount = input("Amount: ")
    if not validate_positive_number(amount, "amount"): return

    result = _create_bill(patient_id, amount)
    print(result["message"])


def view_bills():
    data = get_all_bills()
    if not data:
        print("No bills found!")
        return
    for b in data:
        print(f"""
ID         : {b[0]}
Patient ID : {b[1]}
Amount     : {b[2]}
Status     : {b[3]}
----------------------------""")


def mark_paid():
    bid = input("Enter Bill ID: ")
    result = _mark_paid(bid)
    print(result["message"])


def delete_bill():
    bid = input("Enter Bill ID: ")
    result = _delete_bill(bid)
    print(result["message"])


def search_bill():
    patient_id = input("Enter Patient ID: ")
    data = _search_bill(patient_id)
    if not data:
        print("No bills found!")
        return
    for b in data:
        print(f"""
ID         : {b[0]}
Patient ID : {b[1]}
Amount     : {b[2]}
Status     : {b[3]}
----------------------------""")