from app.config import get_db_connection
from datetime import datetime

def get_dashboard_counts():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS task_count FROM tasks")
        task_count = cursor.fetchone()['task_count']
        cursor.execute("SELECT COUNT(*) AS user_count FROM users")
        user_count = cursor.fetchone()['user_count']
        return {'task_count': task_count, 'user_count': user_count}
    finally:
        cursor.close()
        connection.close()

def fetch_all_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def fetch_user_overview():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                u.user_id, u.user_name, u.email,
                COUNT(t.task_id) AS total_tasks,
                SUM(t.complete = 1) AS completed_tasks,
                SUM(t.complete = 0) AS pending_tasks,
                MAX(GREATEST(
                    IFNULL(UNIX_TIMESTAMP(t.creation_time), 0),
                    IFNULL(UNIX_TIMESTAMP(t.finish_time), 0)
                )) AS last_activity_unix
            FROM users u
            LEFT JOIN tasks t ON u.user_id = t.user_id
            GROUP BY u.user_id
        """)
        users = cursor.fetchall()
        for user in users:
            user['last_activity'] = (
                datetime.fromtimestamp(user['last_activity_unix']).strftime('%Y-%m-%d %H:%M:%S')
                if user['last_activity_unix'] else None
            )
        return users
    finally:
        cursor.close()
        connection.close()


def delete_user_by_id(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()
