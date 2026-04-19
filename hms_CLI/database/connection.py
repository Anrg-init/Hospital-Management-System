import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="hms_db",
            user="hms_user",
            password="123",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
        return None