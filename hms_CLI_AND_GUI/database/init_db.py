from connection import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        name TEXT,
        age INT,
        gender TEXT,
        disease TEXT,
        contact TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id TEXT PRIMARY KEY,
        name TEXT,
        age INT,
        gender TEXT,
        specialization TEXT,
        availability TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id TEXT PRIMARY KEY,
        patient_id TEXT,
        doctor_id TEXT,
        date TEXT,
        time TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id TEXT PRIMARY KEY,
        patient_id TEXT,
        amount FLOAT,
        status TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    init_db()