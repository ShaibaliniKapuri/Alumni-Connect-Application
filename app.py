import os
from flask import Flask, render_template, request,flash,redirect, session, url_for
from config import Config
from models import db, User, Session, Application
from flask_login import LoginManager

from auth import auth_bp
from views import views_bp

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok = True)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category ='warning'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)

#creating admin
with app.app_context():
    db.create_all()
    if not User.query.filter_by(role = 'admin').first():
        admin = User(username = 'admin',email = 'admin@email.com', password = 'admin123', role = 'admin', is_approved = True)
        db.session.add(admin)
        db.session.commit()






if __name__ == '__main__':
    app.run(debug = True)

