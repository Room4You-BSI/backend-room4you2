import os.path

from flask import Flask
from flask_jwt_simple import JWTManager
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dataBase.db')
app.config['JWT_SECRET_KEY'] = 'dKorz3YmAdJpiMfM7_9b8kOYd7NhVslSZ4DoSwXkHYb9i0xSA7NC0WTYfQTULJZcYGY8qQ4I4OFbw7Z0nL3Y9JCv74SI9urpxdwpsfrJIonEO1cVcnlxpt1NW1QmwD6FY4b-jgGDdDYjIFF1sFBogj-kDeIbx-TW77oatX44PsQOH_mmCTxpKRRQdKIo7ER2o5r94X_OBqnwJTZziJRu6cdB887-DKDp1ItSFWFN4TLx8YTm22nDSmugyjB-K_IF9PARVlZrfUmj4IWnU-nQsQdrDeHx63PGs7dEHPx9qhOqr8dUVnrrVwVCF6vPJtySB0Ehq6qw'

jwt = JWTManager(app)
db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    header['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response
