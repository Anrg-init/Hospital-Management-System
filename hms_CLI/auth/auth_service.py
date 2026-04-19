from database.connection import get_connection
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role (admin/receptionist): ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hash_password(password), role)
        )
        conn.commit()
        print("User registered!")
    except:
        print("Username already exists!")

    cur.close()
    conn.close()


def login():
    username = input("Username: ")
    password = input("Password: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=%s AND password=%s",
        (username, hash_password(password))
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        print("Login successful!")
        return {"username": username, "role": result[0]}
    else:
        print("Invalid credentials!")
        return None