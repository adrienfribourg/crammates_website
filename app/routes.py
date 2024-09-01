from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, login_user  # Added login_user
from werkzeug.security import check_password_hash, generate_password_hash  # Added check_password_hash
from app.models import StudySession, User
from app import db

# Create a Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/calendar')
def calendar():
    return render_template('calendar.html')

@bp.route('/about')
def about():
    return render_template('about.html')

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
            return render_template('login.html')  # Render the login page with the flash message
    return render_template('login.html')

@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/profile')
@login_required  # Ensures the user is logged in to access this page
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                courses = data.get('courses')  # Changed from `course` to `courses`
            else:
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                courses = request.form.get('courses')  # Changed from `course` to `courses`

            if not password:
                flash('Password is required.', 'danger')
                return redirect(url_for('main.signup'))

            if User.query.filter_by(email=email).first():
                flash('User with this email already exists.', 'danger')
                return redirect(url_for('main.signup'))

            new_user = User(username=username, email=email,
                            password_hash=generate_password_hash(password),
                            courses=courses)  # Ensure `courses` is used
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f"Error during registration: {e}")  # Print the error to the console
            flash('An error occurred. Please try again later.', 'danger')
            return redirect(url_for('main.signup'))

    return render_template('signup.html')