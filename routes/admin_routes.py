from flask import Blueprint, render_template, redirect, flash, session, url_for, request
from functools import wraps
from config import get_db_connection
from datetime import datetime

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

@admin_bp.route("/admin_dashboard/edit_task/<int:task_id>", methods=['GET', 'POST'])
@admin_required
def edit_task(task_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        if request.method == 'POST':
            task_header = request.form.get('task_header')
            task_description = request.form.get('task_description')
            if not task_header or not task_description:
                flash("Task header and description cannot be empty.", "danger")
                return redirect(url_for('admin.display_tasks', task_id=task_id))
            complete = request.form.get('complete') == 'on'
            finish_time = datetime.now() if complete else None
            cursor.execute(
                """
                UPDATE tasks 
                SET task_header = %s, 
                    task_description = %s, 
                    finish_time = %s, 
                    complete = %s 
                WHERE task_id = %s 
                """,
                (task_header, task_description, finish_time, complete, task_id)
            )
            connection.commit()
            flash("Task updated successfully!", "success")
            return redirect(url_for('admin.display_tasks'))
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        task = cursor.fetchone()
        if not task:
            flash("Task not found.", "danger")
            return redirect(url_for('admin.admin_dashboard'))
        return render_template('admin_temp/admin_edit_task.html', task=task)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('admin.admin_dashboard'))
    finally:
        cursor.close()
        connection.close()

@admin_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@admin_required
def delete_task(task_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        connection.commit()
        flash("Task deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('admin.display_tasks'))

@admin_bp.route('/delete_users/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE  user_id = %s", (user_id,))
        connection.commit()
        flash(f"User has been deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    finally:
        pass
    return redirect(url_for('admin.manage_users'))