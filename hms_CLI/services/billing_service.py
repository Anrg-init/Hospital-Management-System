from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty, validate_positive_number
from auth.session import get_user


def create_bill():
    user = get_user()

    if user["role"] not in ["admin", "receptionist"]:
        print("Access denied!")
        return

    patient_id = input("Patient ID: ")
    if not validate_non_empty(patient_id, "patient id"):
        return

    amount = input("Amount: ")
    if not validate_positive_number(amount, "amount"):
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        # check patient exists
        cur.execute("SELECT 1 FROM patients WHERE id=%s", (patient_id,))
        if not cur.fetchone():
            print("Patient not found!")
            return

        bid = generate_id()

        cur.execute("""
            INSERT INTO bills (id, patient_id, amount, status)
            VALUES (%s,%s,%s,%s)
        """, (bid, patient_id, float(amount), "unpaid"))

        conn.commit()
        print("Bill created successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def view_bills():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM bills")
        data = cur.fetchall()

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

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def mark_paid():
    user = get_user()

    if user["role"] not in ["admin", "receptionist"]:
        print("Access denied!")
        return

    bid = input("Enter Bill ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT 1 FROM bills WHERE id=%s", (bid,))
        if not cur.fetchone():
            print("Bill not found!")
            return

        cur.execute("""
            UPDATE bills SET status=%s WHERE id=%s
        """, ("paid", bid))

        conn.commit()
        print("Bill marked as paid!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def delete_bill():
    user = get_user()

    if user["role"] != "admin":
        print("Only admin can delete bill!")
        return

    bid = input("Enter Bill ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT 1 FROM bills WHERE id=%s", (bid,))
        if not cur.fetchone():
            print("Bill not found!")
            return

        cur.execute("DELETE FROM bills WHERE id=%s", (bid,))
        conn.commit()
        print("Bill deleted successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def search_bill():
    patient_id = input("Enter Patient ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM bills WHERE patient_id=%s",
            (patient_id,)
        )
        data = cur.fetchall()

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

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()