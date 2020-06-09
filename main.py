from flask import request, redirect, url_for, Response, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User

from json import dumps
from http import HTTPStatus
from http.client import HTTPException


@app.route("/add_user", methods=["GET", "POST"])
def register():
    
    if request.method == 'POST':
        try:
            name = request.form["name"]
            email = request.form["email"]
            pwd = request.form["password"]

            user = User(name, pwd, email)
            db.session.add(user)
            db.session.commit()

            return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")
        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
        
    return Response(dumps({"message": "NOT AVAILABLE"}), status=403, mimetype="application/json")

@app.route("/get_profile", methods=["GET", "POST"])
def login():
    
    if request.method == 'POST':
        try:
            email = request.form["email"]
            pwd = request.form["password"]

            user = User.query.filter_by(email=email).first()
            
            if not user or not user.verify_password(pwd):
                return redirect(url_for("login"))

            login_user(user)
            
            return Response(dumps([{"message": "SUCCESS"}]), status=200, mimetype="application/json")
        except HTTPException as e:
            return Response(dumps([{"message": str(e)}]), status=500, mimetype="application/json")

    return Response(dumps([{"message": "NOT AVAILABLE"}]), status=403, mimetype="application/json")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return Response(dumps([{"message": "SUCCESS"}]), status=200, mimetype="application/json")

@app.route('/home', methods=["GET"])
@app.route('/', methods=["GET"])
def home():
    return Response(dumps([{"message": "SUCCESS"}]), status=200, mimetype="application/json")

# informações sobre os posts
posts = [
    { 
        'title': 'Quarto São Carlos',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': '',
        'price': 10,
        'rate': 50,
        'distance': '4,0 km do centro',
        'favorite': False,
        'attributesColumn1': 'OfferCardColumnItemModel[]',
        'attributesColumn2': 'OfferCardColumnItemModel[]'
    },
    {
        'title': 'Quarto Rodoviária',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': '',
        'price': 10,
        'rate': 50,
        'distance': '4,0 km do centro',
        'favorite': False,
        'attributesColumn1': 'OfferCardColumnItemModel[]',
        'attributesColumn2': 'OfferCardColumnItemModel[]'
    },
    {
        'title': 'Quarto Embaré',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': '',
        'price': 10,
        'rate': 50,
        'distance': '4,0 km do centro',
        'favorite': False,
        'attributesColumn1': 'OfferCardColumnItemModel[]',
        'attributesColumn2': 'OfferCardColumnItemModel[]'
    }
]

@app.route('/posts', methods=["GET"])
def rooms():
    return Response(dumps(posts), status=200, mimetype="application/json")

app.run(debug=True)
