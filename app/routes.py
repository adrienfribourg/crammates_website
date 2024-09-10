from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
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
            return redirect(url_for('main.profile'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            courses = request.form.get('courses')

            if not password:
                flash('Password is required.', 'danger')
                return redirect(url_for('main.signup'))

            if User.query.filter_by(email=email).first():
                flash('User with this email already exists.', 'danger')
                return redirect(url_for('main.signup'))

            new_user = User(username=username, email=email,
                            password_hash=generate_password_hash(password),
                            courses=courses)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('main.login'))

        except Exception as e:
            print(f"Error during registration: {e}")
            flash('An error occurred. Please try again later.', 'danger')
            return redirect(url_for('main.signup'))

    return render_template('signup.html')

# Route to add a new study session
@bp.route('/add_session', methods=['POST'])
@login_required
def add_session():
    try:
        title = request.json.get('title')  # Match front-end data keys
        course = request.json.get('course')  # Match front-end data keys
        start = request.json.get('start')  # The start time from front-end
        end = request.json.get('end')  # The end time from front-end
        description = request.json.get('description')

        if not title or not course or not start or not end:
            return jsonify({'success': False, 'error': 'Missing required fields.'}), 400

        # Create a new StudySession object
        new_session = StudySession(
            title=title,
            course=course,
            date=start,  # Assume this is properly formatted
            description=description,
            creator_id=current_user.id
        )
        db.session.add(new_session)
        db.session.commit()

        return jsonify({'success': True}), 200

    except Exception as e:
        print(f"Error adding session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Route to fetch all study sessions for the current user
@bp.route('/get_sessions', methods=['GET'])
@login_required
def get_sessions():
    try:
        sessions = StudySession.query.filter_by(creator_id=current_user.id).all()
        session_list = [{
            'title': session.title,
            'course': session.course,
            'start': session.date.isoformat(),
            'description': session.description
        } for session in sessions]

        return jsonify(session_list)

    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return jsonify({'error': 'An error occurred while fetching sessions.'}), 500
