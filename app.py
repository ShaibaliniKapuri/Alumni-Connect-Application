from flask import Flask, render_template, request,flash,redirect, session
from models import db, User, Session, Application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SECRET_KEY'] = 'bootcamp_secret_key'

db.init_app(app)

#creating admin
with app.app_context():
    db.create_all()
    if not User.query.filter_by(role = 'admin').first():
        admin = User(username = 'admin',email = 'admin@email.com', password = 'admin123', role = 'admin', is_approved = True)
        db.session.add(admin)
        db.session.commit()



#Define Routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        new_user = User(username = username, email = email, password = password, role = role)
        if role == 'student' : new_user.is_approved = True #student do not need admin approval

        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful')
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            if user.role == 'alumni' and not user.is_approved:
                flash("Account needs to be approved")
                return redirect('/')
            session['user_id'] = user.id
            session['role'] = user.role

            if user.role == 'admin' : return render_template("admin.html") #redirect('/admin')
            if user.role == 'alumni' : return render_template("alumni.html") #redirect('/alumni')
            if user.role == 'student' : return render_template("student.html") #redirect('/student')

        flash("Invalid Credentials")
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug = True)

