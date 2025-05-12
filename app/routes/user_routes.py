from flask import Blueprint, render_template, redirect, flash, request, session, url_for
from ..services.task_service import get_tasks_by_user, get_task_by_id, create_task, update_task, delete_task_by_id
from app.utils.auth_required import login_required
from app.config import get_db_connection
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route("/", methods=["GET"])
@login_required
def home():
    try:
        tasks = get_tasks_by_user(session['user_id'])
        return render_template("user/index.html", tasks=tasks)
    except Exception as e:
        flash(f"Failed to load tasks: {e}", "danger")
        return redirect(url_for('auth.login'))
    

@user_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        task_header = request.form.get("task_header")
        task_description = request.form.get("task_description")
        if not task_header or not task_description:
            flash("Task header and description are required.", "danger")
            return redirect(url_for("user.add_task"))
        try:
            create_task(task_header, task_description, session['user_id'])
            flash("Task added successfully.", "success")
            return redirect(url_for("user.home"))
        except Exception as e:
            flash(f"Failed to add task: {e}", "danger")
            return redirect(url_for("user.add_task"))
    return render_template("user/add_task.html")


@user_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    try:
        if request.method == "POST":
            task_header = request.form.get("task_header")
            task_description = request.form.get("task_description")
            is_complete = request.form.get("complete") == "on"
            if not task_header or not task_description:
                flash("Both fields are required.", "danger")
                return redirect(url_for("user.edit_task", task_id=task_id))
            update_task(task_id, session['user_id'], task_header, task_description, is_complete)
            flash("Task updated successfully.", "success")
            return redirect(url_for("user.home"))
        task = get_task_by_id(task_id, session['user_id'])
        if not task:
            flash("Task not found.", "danger")
            return redirect(url_for("user.home"))
        return render_template("user/edit_task.html", task=task)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for("user.home"))


@user_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    try:
        delete_task_by_id(task_id, session['user_id'])
        flash("Task deleted successfully.", "success")
    except Exception as e:
        flash(f"Failed to delete task: {e}", "danger")
    return redirect(url_for("user.home"))
