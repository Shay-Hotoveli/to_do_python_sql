from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from ..services.user_service import get_user_by_username, create_user, check_valid_register_info


auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = get_user_by_username(username)
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['user_id']
                session['user_name'] = user['user_name']
                session['role'] = user['role']
                if 'user_id' in session and session['role'] == 'admin':
                    flash('Hello Admin', 'Success')
                    return redirect(url_for('admin.admin_dashboard'))
                flash("Login successful!", "success")
                flash(f"Hello {user['user_name']}.")
                return redirect(url_for('user.home'))
            else:
                flash("Invalid username or password.", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        valid, message = check_valid_register_info(username, email)
        if not valid:
            flash(message, 'danger')
            return redirect(url_for('auth.register'))       
        password_hash = generate_password_hash(password)
        create_user(username, password_hash, email, gender)
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


