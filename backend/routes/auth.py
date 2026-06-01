from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from backend.models import db
from backend.models.user import User
from backend.models.application import Application
from backend.models.internship import Internship

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
            
        new_user = User(
            username=username,
            email=email,
            role=role
        )
        
        # Role-specific fields
        if role == 'student':
            new_user.skills = request.form.get('skills', '')
            new_user.experience = request.form.get('experience', '')
            new_user.resume_link = request.form.get('resume_link', '')
            new_user.bio = request.form.get('bio', '')
        elif role == 'company':
            new_user.company_name = request.form.get('company_name', '')
            new_user.company_website = request.form.get('company_website', '')
            new_user.bio = request.form.get('company_description', '')
            
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.dashboard'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
            
        flash('Invalid email or password.', 'danger')
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return redirect(url_for('auth.student_dashboard'))
    elif current_user.role == 'company':
        return redirect(url_for('auth.company_dashboard'))
    elif current_user.role == 'admin':
        return redirect(url_for('auth.users_admin'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    # Get student's applications
    applications = Application.query.filter_by(student_id=current_user.id).all()
    
    # Import recommendation engine to render matching internships on dashboard
    from backend.services.recommendation_service import RecommendationService
    recommendations = RecommendationService.get_recommendations(current_user)
    
    # Take top 3 for dashboard quick view
    top_recommendations = recommendations[:3]
    
    return render_template('student_dashboard.html', 
                           applications=applications, 
                           recommendations=top_recommendations)

@auth_bp.route('/company/dashboard')
@login_required
def company_dashboard():
    if current_user.role != 'company':
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    # Get internships posted by company
    internships = Internship.query.filter_by(company_id=current_user.id).all()
    
    # Get applications for these internships
    internship_ids = [internship.id for internship in internships]
    applications = Application.query.filter(Application.internship_id.in_(internship_ids)).order_by(Application.applied_at.desc()).all() if internship_ids else []
    
    return render_template('company_dashboard.html', 
                           internships=internships, 
                           applications=applications)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if current_user.role == 'student':
            current_user.skills = request.form.get('skills', '')
            current_user.experience = request.form.get('experience', '')
            current_user.resume_link = request.form.get('resume_link', '')
            current_user.bio = request.form.get('bio', '')
        elif current_user.role == 'company':
            current_user.company_name = request.form.get('company_name', '')
            current_user.company_website = request.form.get('company_website', '')
            current_user.bio = request.form.get('company_description', '')
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
        
    return render_template('profile.html')

@auth_bp.route('/users')
@login_required
def users_admin():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    users = User.query.all()
    return render_template('users.html', users=users)
