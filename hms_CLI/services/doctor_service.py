from database.connection import get_connection
from utils.helpers import generate_id, validate_non_empty, validate_positive_number
from auth.session import get_user


def add_doctor():
    user = get_user()

    if user["role"] != "admin":
        print("Only admin can add doctor!")
        return

    name = input("Name: ")
    if not validate_non_empty(name, "name"):
        return

    age = input("Age: ")
    if not validate_positive_number(age, "age"):
        return

    gender = input("Gender: ")
    spec = input("Specialization: ")
    avail = input("Availability: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        # duplicate check
        cur.execute(
            "SELECT 1 FROM doctors WHERE name=%s",
            (name,)
        )
        if cur.fetchone():
            print("Doctor already exists!")
            return

        did = generate_id()

        cur.execute("""
            INSERT INTO doctors (id, name, age, gender, specialization, availability)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (did, name, int(age), gender, spec, avail))

        conn.commit()
        print("Doctor added successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def view_doctors():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM doctors")
        data = cur.fetchall()

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

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def update_doctor():
    user = get_user()

    if user["role"] != "admin":
        print("Only admin can update doctor!")
        return

    did = input("Enter Doctor ID to update: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM doctors WHERE id=%s", (did,))
        d = cur.fetchone()

        if not d:
            print("Doctor not found!")
            return

        print(f"Updating {d[1]}. Leave blank to keep current value.")

        new_name  = input(f"New Name [{d[1]}]: ")           or d[1]
        new_age   = input(f"New Age [{d[2]}]: ")            or d[2]
        new_gender = input(f"New Gender [{d[3]}]: ")        or d[3]
        new_spec  = input(f"New Specialization [{d[4]}]: ") or d[4]
        new_avail = input(f"New Availability [{d[5]}]: ")   or d[5]

        cur.execute("""
            UPDATE doctors
            SET name=%s, age=%s, gender=%s, specialization=%s, availability=%s
            WHERE id=%s
        """, (new_name, int(new_age), new_gender, new_spec, new_avail, did))

        conn.commit()
        print("Doctor updated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def delete_doctor():
    user = get_user()

    if user["role"] != "admin":
        print("Only admin can delete doctor!")
        return

    did = input("Enter Doctor ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT 1 FROM doctors WHERE id=%s", (did,))
        if not cur.fetchone():
            print("Doctor not found!")
            return

        cur.execute("DELETE FROM doctors WHERE id=%s", (did,))
        conn.commit()
        print("Doctor deleted successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


def search_doctor():
    keyword = input("Enter name or doctor ID: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM doctors WHERE name ILIKE %s OR id=%s",
            (f"%{keyword}%", keyword)
        )
        data = cur.fetchall()

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

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()