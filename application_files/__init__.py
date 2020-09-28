import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create/initialization of the application
app = Flask(__name__)
app.secret_key = '97ef6723e4cad5ec0d157570dbdca787'
# upload the configuration values from file config.py

# app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from application_files import routes

