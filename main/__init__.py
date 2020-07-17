import os
import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

os.environ['EMAIL_USER'] = 'haanzee@gmail.com'
os.environ['EMAIL_PASS'] = 'Jas5454#@'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fb5fc397fa9767ca1db7646871b5c546'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from main.users.route import users
from main.posts.route import posts
from main.main.route import main
from main.errors.handlers import errors
from main.bhandler.route import bhandler


app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(bhandler)
