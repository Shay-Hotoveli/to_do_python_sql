from app.config import get_db_connection
from datetime import datetime

def get_tasks_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def get_task_by_id(task_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s AND user_id = %s", (task_id, user_id))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    return task

def create_task(task_header, task_description, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (task_header, task_description, user_id) VALUES (%s, %s, %s)",
        (task_header, task_description, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_task(task_id, user_id, task_header, task_description, is_complete):
    finish_time = datetime.now() if is_complete else None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks 
        SET task_header = %s, task_description = %s, finish_time = %s, complete = %s
        WHERE task_id = %s AND user_id = %s
    """, (task_header, task_description, finish_time, is_complete, task_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_task_by_id(task_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id = %s AND user_id = %s", (task_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
