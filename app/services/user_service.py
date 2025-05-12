from app.config import get_db_connection
import re

def get_user_by_username(username):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def create_user(username, password_hash, email, gender):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (user_name, password, email, gender)
            VALUES (%s, %s, %s, %s)
        """, (username, password_hash, email, gender))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def user_exists(username, email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT user_name, email FROM users 
            WHERE LOWER(user_name) = LOWER(%s) OR LOWER(email) = LOWER(%s)
        """
        cursor.execute(query, (username, email))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def check_valid_register_info(username, email):
    if not username or not email:
        return False, "Username and email are required."
    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        return False, "Invalid username. Must be alphanumeric (or underscore) and 3-20 characters long."
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format." 
    if user_exists(username, email):
        return False, "Username or email already exists."
    return True, "Valid inputs. Proceed with registration."
