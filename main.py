from flask import request, redirect, url_for, Response, abort
from app import app, db
from app.models import User, Post
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity

from json import dumps
from http import HTTPStatus
from http.client import HTTPException

@app.route("/add_user", methods=["GET", "POST"])
def register():
    """Register a user in the database."""
    if request.method == 'POST':
        try:
            name = request.form["nome"]
            email = request.form["email"]
            pwd = request.form["password"]

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                return Response(dumps({"message": "USER ALREADY EXISTS"}), status=422, mimetype="application/json")

            user = User(name, pwd, email)
            db.session.add(user)
            db.session.commit()

            return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
    
    return Response(dumps({"message": "NOT AVAILABLE"}), status=403, mimetype="application/json")

@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    """Register a Post in the database."""
    if request.method == 'POST':
        try:
            #print(request.form.items)
            content = request.form.get("content")
            print(content)
            # title = request.form["title"]
            # date_posted = request.form["date_posted"]
            # image = request.form["image_file"]
            # price = request.form["price"]
            # rate = request.form["rate"]
            # favorite = request.form["favorite"]
            # address = request.form["address"]
            # neighborhood = request.form["neighborhood"]
            # city = request.form["city"]
            # state = request.form["state"]
            
            # email = request.form["email"]
            #current_user = User.query.filter_by(email=email).first()
            
            #post1 = Post(content,title,date_posted,image,price,rate,favorite,address,neighborhood,city,state,current_user.id)
            
            #print(post1)
            #db.session.add(Post)
            #db.session.commit()

            return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
    return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")


@app.route("/get_profile", methods=["GET", "POST"])
def login():
    
    if request.method == 'POST':
        try:
            email = request.form["email"]
            pwd = request.form["password"]

            user = User.query.filter_by(email=email).first()
            
            if not user:
                return Response(dumps({"message": "USER NOT FOUND"}), status=404, mimetype="application/json")
            
            if not user.verify_password(pwd):
                return Response(dumps({"message": "WRONG PASSWORD"}), status=422, mimetype="application/json")

            return Response(dumps({"message": "SUCCESS", "jwt": create_jwt(identity=email)}), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
        
    return Response(dumps({"message": "NOT AVAILABLE"}), status=403, mimetype="application/json")

@app.route('/adduser2', methods=["GET"])
def adduser2():
    user1 = User(name="Cassio",password="123485",email="ccas@g.com",image_file="000.jpg")
    db.session.add(user1)
    db.session.commit()
    return Response(dumps([{"message": "SUCCESS"}]), status=200, mimetype="application/json")

@app.route('/addpost', methods=["GET"])
def addpost():
    post1 = Post(content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
     title = "Titulo 1",image_file = "123.jpg",price = 250.00,rate = 50,favorite = True,address = "Rua leao de macaquinhos",neighborhood = "Bairdro dos alemaes",city = "Maracanja",state = "MA",user_id = 1)
    db.session.add(post1)
    db.session.commit()
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
        'image': 'https://media.gazetadopovo.com.br/haus/2018/10/quarto-infantil-dia-da-crianca-decoracao-design-arquitetura-dicas-karina-korn-5-768x521-baa14530.jpg',
        'price': 720.5,
        'rate': 5,
        'distance': '4,0 km do centro',
        'favorite': False,
        'attributesColumn1': [
            {
                'label': 'Vaga', 
                'available': True
            },
            {
                'label': 'Wi-fi', 
                'available': True
            },
        ],
        'attributesColumn2': [
            {
                'label': 'Suite', 
                'available': False
            }
        ]
    },
    {
        'title': 'Quarto Rodoviária',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': 'https://q-cf.bstatic.com/images/hotel/max1024x768/200/200710933.jpg',
        'price': 380.7,
        'rate': 3,
        'distance': '2,8 km do centro',
        'favorite': False,
        'attributesColumn1': [
            {
                'label': 'Vaga', 
                'available': True
            },
            {
                'label': 'Wi-fi', 
                'available': True
            },
        ],
        'attributesColumn2': [
            {
                'label': 'Suite', 
                'available': True
            }
        ]
    },
    {
        'title': 'Quarto Embaré',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': 'https://images.madeiramadeira.com.br/product/images/75801354-quarto-de-solteiro-completo-com-guarda-roupa-closet-painel-cabeceira-e-nicho-mov-siena-moveis-1_zoom-1500x1500.jpg',
        'price': 450.5,
        'rate': 5,
        'distance': '3,8 km do centro',
        'favorite': False,
        'attributesColumn1': [
            {
                'label': 'Vaga', 
                'available': True
            },
            {
                'label': 'Wi-fi', 
                'available': True
            },
        ],
        'attributesColumn2': [
            {
                'label': 'Suite', 
                'available': True
            }
        ]
    }
]

@app.route('/posts', methods=["GET"])
def rooms():
    return Response(dumps(posts), status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True)