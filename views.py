import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app,jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
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

#Alumni

@views_bp.route('/alumni', methods = ['GET', 'POST'])
@login_required
def alumni_dash():
    if current_user.role != 'alumni':
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        mentor_id = current_user.id 
        new_session = Session(title = title, description = description, mentor_id = mentor_id)
        new_session.is_approved = True #by default sessions will be approved

        db.session.add(new_session)
        db.session.commit()
        flash("Session created successfully", 'success')
        return redirect(url_for('views.alumni_dash'))
    
    my_sessions = Session.query.filter_by(mentor_id = current_user.id).all()
    return render_template('alumni_dash.html', my_sessions = my_sessions)

@views_bp.route('/update_app/<int:app_id>/<string:action>')
@login_required
def update_app(app_id, action):
    if current_user.role != 'alumni':
        return redirect(url_for('views.dashboard'))
    
    application = Application.query.get_or_404(app_id)
    if application.session.mentor_id == current_user.id:
        if action == 'accept':
            application.status = 'Accepted'
        else:
            application.status = 'Rejected'
        db.session.commit()
    return redirect(url_for('views.alumni_dash'))    


   


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



@views_bp.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'student':
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        file = request.files.get('resume')
        if file and file.filename.endswith(('.pdf','.docx')):
            filename = secure_filename(f"user_{current_user.id}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            current_user.resume_file = filename
            db.session.commit()
            flash('Resume uploaded', 'succcess')
    return render_template('profile.html')    