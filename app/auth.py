# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
import traceback

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                courses = data.get('courses')
                university = data.get('university')
            else:
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                courses = request.form.get('courses')
                university = request.form.get('university')

            if not password:
                flash('Password is required.', 'danger')
                return redirect(url_for('main.signup'))

            if User.query.filter_by(email=email).first():
                flash('User with this email already exists.', 'danger')
                return redirect(url_for('main.signup'))

            new_user = User(username=username, email=email,
                            password_hash=generate_password_hash(password),
                            courses=courses,
                            university=university)
            db.session.add(new_user)
            db.session.commit()

            # Automatically log in the user after successful registration
            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            error_message = f"Error during registration: {str(e)}"
            print(error_message)
            traceback.print_exc()
            return render_template('signup.html', error=error_message)

    return render_template('signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.profile'))  # Redirect to profile page on success
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))