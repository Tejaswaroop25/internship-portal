from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from backend.models import db
from backend.models.application import Application
from backend.models.internship import Internship

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/apply/<int:internship_id>', methods=['GET', 'POST'])
@login_required
def apply(internship_id):
    if current_user.role != 'student':
        flash('Only students can apply for internships.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    internship = Internship.query.get_or_404(internship_id)
    
    # Check if student already applied
    existing_app = Application.query.filter_by(
        internship_id=internship_id, 
        student_id=current_user.id
    ).first()
    
    if existing_app:
        flash('You have already applied for this internship.', 'warning')
        return redirect(url_for('auth.student_dashboard'))
        
    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter')
        
        new_app = Application(
            internship_id=internship_id,
            student_id=current_user.id,
            cover_letter=cover_letter
        )
        
        db.session.add(new_app)
        db.session.commit()
        
        flash('Your application has been submitted successfully!', 'success')
        return redirect(url_for('auth.student_dashboard'))
        
    return render_template('apply.html', internship=internship)

@applications_bp.route('/applications', methods=['GET'])
@login_required
def list_applications():
    if current_user.role == 'student':
        applications = Application.query.filter_by(student_id=current_user.id).order_by(Application.applied_at.desc()).all()
        return render_template('applications.html', applications=applications)
        
    elif current_user.role == 'company':
        # Get all internships posted by company
        company_internships = Internship.query.filter_by(company_id=current_user.id).all()
        internship_ids = [internship.id for internship in company_internships]
        
        if internship_ids:
            applications = Application.query.filter(Application.internship_id.in_(internship_ids)).order_by(Application.applied_at.desc()).all()
        else:
            applications = []
            
        return render_template('applications.html', applications=applications)
        
    elif current_user.role == 'admin':
        applications = Application.query.order_by(Application.applied_at.desc()).all()
        return render_template('applications.html', applications=applications)
        
    return redirect(url_for('auth.dashboard'))

@applications_bp.route('/applications/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    application = Application.query.get_or_404(id)
    
    # Verify current user is the company posting the internship
    internship = Internship.query.get(application.internship_id)
    if current_user.role != 'company' or internship.company_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    status = request.form.get('status')
    if status in ['Pending', 'Reviewed', 'Accepted', 'Rejected']:
        application.status = status
        db.session.commit()
        flash(f'Application status updated to {status}!', 'success')
    else:
        flash('Invalid status provided.', 'danger')
        
    return redirect(url_for('auth.company_dashboard'))
