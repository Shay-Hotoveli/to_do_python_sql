from flask import Blueprint, render_template, redirect, flash, session, url_for
from functools import wraps
from config import get_db_connection

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None or session.get('role') != 'admin':
            flash("Access denied! Admins only.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS task_count FROM tasks")
    task_count = cursor.fetchone()['task_count']
    cursor.execute("SELECT COUNT(*) AS user_count FROM users")
    user_count = cursor.fetchone()['user_count']
    cursor.close()
    connection.close()
    return render_template('admin_temp/admin_dashboard.html', task_count=task_count, user_count=user_count)

@admin_bp.route('/admin_dashboard/manage_users')
@admin_required
def manage_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        users = []
    finally:
        cursor.close()
        connection.close()
    return render_template('admin_temp/users.html', users=users)

@admin_bp.route('/admin_dashboard/tasks')
@admin_required
def display_tasks():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        tasks = []
    finally:
        cursor.close()
        connection.close()
    return render_template('admin_temp/tasks.html', tasks=tasks)