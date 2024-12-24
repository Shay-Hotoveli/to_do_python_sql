from flask import Blueprint, render_template, redirect, flash, request, session, url_for
from functools import wraps
from config import get_db_connection
from datetime import datetime


user_bp = Blueprint('user', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args , **kwargs):
        if 'user_id' not in session:
            flash("Access denied! Please log in.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@user_bp.route("/", methods=["GET"])
@login_required
def home():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (session['user_id'],))
        tasks = cursor.fetchall()
        return render_template("user_temp/index.html", tasks=tasks)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('auth.login'))
    finally:
        cursor.close()
        connection.close()


@user_bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        task_header = request.form.get('task_header')
        task_description = request.form.get('task_description')
        if not task_header or not task_description:
            flash("Task header and description cannot be empty.", "danger")
            return redirect(url_for('user.add_task'))
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO tasks (task_header, task_description, user_id) VALUES (%s, %s, %s)",
                (task_header, task_description, session['user_id'])
            )
            connection.commit()
            flash("Task added successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('user.home'))
    return render_template('user_temp/add_task.html')


@user_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id = %s AND user_id = %s", (task_id, session['user_id']))
        connection.commit()
        flash("Task deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('user.home'))


@user_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        if request.method == 'POST':
            task_header = request.form.get('task_header')
            task_description = request.form.get('task_description')
            if not task_header or not task_description:
                flash("Task header and description cannot be empty.", "danger")
                return redirect(url_for('user.edit_task', task_id=task_id))
            complete = request.form.get('complete') == 'on'
            finish_time = datetime.now() if complete else None
            cursor.execute(
                """
                UPDATE tasks 
                SET task_header = %s, 
                    task_description = %s, 
                    finish_time = %s, 
                    complete = %s 
                WHERE task_id = %s AND user_id = %s
                """,
                (task_header, task_description, finish_time, complete, task_id, session['user_id'])
            )
            connection.commit()
            flash("Task updated successfully!", "success")
            return redirect(url_for('user.home'))
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s AND user_id = %s", (task_id, session['user_id']))
        task = cursor.fetchone()
        if not task:
            flash("Task not found.", "danger")
            return redirect(url_for('user.home'))
        return render_template('user_temp/edit_task.html', task=task)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('user.home'))
    finally:
        cursor.close()
        connection.close()

