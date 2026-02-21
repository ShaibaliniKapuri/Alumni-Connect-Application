from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app,jsonify
from flask_login import login_required, current_user
from models import db, User, Session, Application
from sqlalchemy import or_

views_bp = Blueprint('views', __name__)

#Dashboard

@views_bp.route('/')
@login_required
def dashboard():
    if current_user.role == 'admin' :
        return redirect(url_for('views.admin_dash'))
    if current_user.role == 'alumni' :
        return redirect(url_for('views.alumni_dash'))
    if current_user.role == 'student' :
        return redirect(url_for('views.student_dash'))
    

#Admin

@views_bp.route('/admin', methods = ['GET'])
@login_required
def admin_dash():
    if current_user.role != 'admin':
        return redirect(url_for('views.dashboard'))
    
    search_query = request.args.get('q', '')
    if search_query:
        users = User.query.filter(or_(User.username.ilike(f'%{search_query}%'), User.role.ilike(f'%{search_query}%'))).all()
    else:
        users = User.query.all()

    students = [u for u in users if u.role == 'student']
    alumni = [u for u in users if u.role == 'alumni']
    pending_alumni = [u for u in users if not u.is_approved]

    sessions = Session.query.all()
    return render_template('admin_dash.html',search_query = search_query, student_users = students, alumni_users = alumni, pending_alumni = pending_alumni, sessions = sessions)

@views_bp.route('/admin/<int:id>')
@login_required
def approve_alumni(id):
    if current_user.role != 'admin':
        return redirect(url_for('views.dashboard'))
    
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()
    flash('Approved!', 'success')
    return redirect(url_for('views.admin_dash'))



#Student

@views_bp.route('/student')
@login_required
def student_dash():
    if current_user.role != 'student':
        return redirect(url_for('views.dashboard'))
    
    sessions = Session.query.all()
    my_apps = Application.query.filter_by(student_id = current_user.id).all()
    return render_template('student_dash.html', available_sessions= sessions, my_applications = my_apps)

@views_bp.route('/apply/<int:session_id>', methods = ['POST'])
@login_required
def apply_session(session_id):
    if current_user.role != 'student':
        return redirect(url_for('views.dashboard'))
    if not Application.query.filter_by(student_id = current_user.id, session_id = session_id).first():
        db.session.add(Application(student_id = current_user.id, session_id = session_id))
        db.session.commit()
        flash("Applied Successfully" , 'success')
    return redirect(url_for('views.student_dash'))
