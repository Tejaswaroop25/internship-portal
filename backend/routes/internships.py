from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from backend.models import db
from backend.models.internship import Internship

internships_bp = Blueprint('internships', __name__)

@internships_bp.route('/internships', methods=['GET'])
@login_required
def list_internships():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    
    query = Internship.query
    
    if search:
        query = query.filter(
            (Internship.title.like(f'%{search}%')) | 
            (Internship.requirements.like(f'%{search}%')) |
            (Internship.description.like(f'%{search}%'))
        )
    if location:
        query = query.filter(Internship.location.like(f'%{location}%'))
        
    internships = query.all()
    return render_template('internship_listing.html', 
                           internships=internships, 
                           search=search, 
                           location=location)

@internships_bp.route('/internships/<int:id>', methods=['GET'])
@login_required
def view_internship(id):
    internship = Internship.query.get_or_404(id)
    return render_template('internship_detail.html', internship=internship)

@internships_bp.route('/internships/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'company':
        flash('Only companies can post internships.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        location = request.form.get('location')
        stipend = request.form.get('stipend', 'Unpaid')
        duration = request.form.get('duration', '3 months')
        
        new_internship = Internship(
            title=title,
            description=description,
            requirements=requirements,
            location=location,
            stipend=stipend,
            duration=duration,
            company_id=current_user.id
        )
        
        db.session.add(new_internship)
        db.session.commit()
        flash('Internship posted successfully!', 'success')
        return redirect(url_for('auth.company_dashboard'))
        
    return render_template('create_internship.html')

@internships_bp.route('/internships/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    internship = Internship.query.get_or_404(id)
    
    if current_user.role != 'company' or internship.company_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    if request.method == 'POST':
        internship.title = request.form.get('title')
        internship.description = request.form.get('description')
        internship.requirements = request.form.get('requirements')
        internship.location = request.form.get('location')
        internship.stipend = request.form.get('stipend')
        internship.duration = request.form.get('duration')
        
        db.session.commit()
        flash('Internship updated successfully!', 'success')
        return redirect(url_for('auth.company_dashboard'))
        
    return render_template('edit_internship.html', internship=internship)

@internships_bp.route('/internships/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    internship = Internship.query.get_or_404(id)
    
    if current_user.role != 'company' or internship.company_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    db.session.delete(internship)
    db.session.commit()
    flash('Internship deleted successfully.', 'success')
    return redirect(url_for('auth.company_dashboard'))
