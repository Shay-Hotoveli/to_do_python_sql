from flask import Blueprint, render_template, redirect, flash, url_for, request
from app.services import admin_service
from ..utils.auth_required import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    try:
        counts = admin_service.get_dashboard_counts()
        return render_template('admin/admin_dashboard.html',
            task_count=counts['task_count'],
            user_count=counts['user_count'])
    except Exception as e:
        flash(f"Failed to load dashboard: {e}", "danger")
        return render_template('admin/admin_dashboard.html', task_count=0, user_count=0)

@admin_bp.route('/admin_dashboard/manage_users')
@admin_required
def manage_users():
    try:
        users = admin_service.fetch_all_users()
    except Exception as e:
        flash(f"Error loading users: {e}", "danger")
        users = []
    return render_template('admin/users.html', users=users)


@admin_bp.route('/user-overview')
@admin_required
def user_overview():
    try:
        users = admin_service.fetch_user_overview()
    except Exception as e:
        flash(f"Failed to load user overview: {e}", "danger")
        users = []
    return render_template('admin/user_overview.html', users=users)


@admin_bp.route('/delete_users/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    try:
        admin_service.delete_user_by_id(user_id)
        flash("User has been deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting user: {e}", "danger")
    return redirect(url_for('admin.manage_users'))
