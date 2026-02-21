from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(username = username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username = username, email = email, password = password, role = role)
        if role == 'student' : new_user.is_approved = True #student do not need admin approval

        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            if user.role == 'alumni' and not user.is_approved:
                flash("Account needs to be approved")
                return redirect(url_for('auth.login'))
            
            login_user(user)
            return redirect(url_for('views.dashboard'))
        
        flash("Invalid Credentials",'danger')    

    return render_template("login.html")


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))