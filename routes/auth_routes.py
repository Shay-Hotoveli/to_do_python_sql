from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from config import get_db_connection
import re


auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
            user = cursor.fetchone()
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
        finally:
            cursor.close()
            connection.close()
    return render_template('login.html')


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
        result = check_valid_register_info(username, email)
        if 'Valid' not in result:
            flash(result, 'danger')
            return redirect(url_for('auth.register'))       
        password_hash = generate_password_hash(password)
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (user_name, password, email, gender)
                VALUES (%s, %s, %s, %s)
            """, (username, password_hash, email, gender))
            connection.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
    return render_template('register.html')

def check_valid_register_info(username, email):
    if not username or not email:
        return "Username and email are required."
    if not username.isalnum() or not (3 <= len(username) <= 20):
        return "Invalid username. Must be alphanumeric and 3-20 characters long."
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format."    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT user_name, email FROM USERS 
            WHERE LOWER(user_name) = LOWER(%s) OR LOWER(email) = LOWER(%s)
        """
        cursor.execute(query, (username, email))
        result = cursor.fetchone()
        if result:
            return "Username or email already exists."
        return "Valid inputs. Proceed with registration."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
