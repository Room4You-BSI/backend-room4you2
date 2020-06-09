import os.path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='templates')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dataBase.db')
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager()
login_manager.init_app(app) 
db = SQLAlchemy(app)


