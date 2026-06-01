from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.services.recommendation_service import RecommendationService

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations')
@login_required
def view_recommendations():
    if current_user.role != 'student':
        flash('Recommendations are only available for student profiles.', 'warning')
        return redirect(url_for('auth.dashboard'))
        
    recommendations = RecommendationService.get_recommendations(current_user)
    return render_template('recommendations.html', recommendations=recommendations)
