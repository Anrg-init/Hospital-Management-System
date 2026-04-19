from database.connection import get_connection
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ─── CORE FUNCTIONS (GUI uses these directly) ───────────────────────

def register_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hash_password(password), role)
        )
        conn.commit()
        return {"success": True, "message": "User registered"}
    except:
        conn.rollback()
        return {"success": False, "message": "Username already exists"}
    finally:
        cur.close()
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, hash_password(password))
        )
        result = cur.fetchone()
        if result:
            return {"success": True, "user": {"username": username, "role": result[0]}}
        else:
            return {"success": False, "message": "Invalid credentials"}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close()
        conn.close()


# ─── CLI WRAPPERS (CLI uses these) ───────────────────────────────────

def register():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    role = input("Role (admin/receptionist): ").strip()

    result = register_user(username, password, role)
    print(result["message"])


def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    result = login_user(username, password)
    if result["success"]:
        print("Login successful!")
        return result["user"]
    else:
        print(result["message"])
        return None