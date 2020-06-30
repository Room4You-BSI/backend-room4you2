import re

from flask import request, redirect, url_for, Response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from config.models import User, Post, Image, Comoditie, User_has_Post_as_favorite
from config import db, jwt

from json import dumps
from http import HTTPStatus
from http.client import HTTPException


# ""Creating error cases JWT""
@jwt.expired_token_loader
def my_expired_token_callback():
    return Response(dumps([{"message": "Token has expired"}]), status=401, mimetype="application/json")

@jwt.invalid_token_loader
def invalid_token_callback(self):
    return Response(dumps([{"message": "Invalid JWT"}]), status=401, mimetype="application/json")

@jwt.unauthorized_loader
def unauthorized_token_callback(self):
    return Response(dumps([{"message": "Missing Authorization Header"}]), status=403, mimetype="application/json")


# ""Flask Functions""

class Views(object):


    def home(self):
        return Response(dumps([{"message": "SUCCESS"}]), status=200, mimetype="application/json")
    

    def register(self):
        """Register a user in the database."""
        if request.method == 'POST':
            try:
                name = request.form["name"]
                email = request.form["email"]
                pwd = request.form["password"]
                img = request.form["img"]

                existing_user = User.query.filter_by(email=email).first()

                if existing_user:
                    return Response(dumps({"message": "USER ALREADY EXISTS"}), status=422, mimetype="application/json")

                user = User(name, pwd, email, img)
                db.session.add(user)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
        
        return Response(dumps({"message": "NOT AVAILABLE"}), status=403, mimetype="application/json")


    @jwt_required
    def create_post(self):
        """Register a Post in the database."""
        if request.method == 'POST':
            try:
                content = request.form.get("content")
                title = request.form["title"]
                #date_posted = request.form["date_posted"]
                #image = request.form["image_file"]
                price = request.form["price"]
                rate = request.form["rate"]
                #favorite = not not request.form["favorite"]
                address = request.form["address"]
                neighborhood = request.form["neighborhood"]
                cep = request.form["cep"]
                city = request.form["city"]
                state = request.form["state"]
                
                email = get_jwt_identity()
                current_user = User.query.filter_by(email=email).first()
                
                #current_post = Post(content, title, image, price, rate, favorite, address, neighborhood, city, state, current_user.id)
                current_post = Post(content, title, price, rate, address, neighborhood, cep, city, state, current_user.id)
                                   
                db.session.add(current_post)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

        return Response(dumps({"message": "NOT POST"}), status=403, mimetype="application/json")


    def login(self):
        """Find a User in the database."""
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


    def rooms_list(self):
        """List the rooms from database."""
        try:
            posts = db.session.query(Post).all()
            all_post = []

            for post in posts:
                all_post.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.content,
                    'image': 'https://q-cf.bstatic.com/images/hotel/max1024x768/200/200710933.jpg',
                    'price': post.price,
                    'rate': post.rate,
                    'distance': '3,0 km do centro',
                    'favorite': False,
                    'attributesColumn1': [
                        {
                            'label': 'Garagem', 
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
                })
            
            return Response(dumps(all_post), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")


    def rooms_detail(self, id):
        """List the rooms from database."""
        try:
            post = Post.query.filter_by(id=id).first()

            detail = [{
                'post_id': post.id,
                'title': post.title,
                'text': post.content,
                'image': ['https://q-cf.bstatic.com/images/hotel/max1024x768/200/200710933.jpg', 'https://q-cf.bstatic.com/images/hotel/max1024x768/200/200710933.jpg', 'https://q-cf.bstatic.com/images/hotel/max1024x768/200/200710933.jpg'],
                'price': post.price,
                'rate': 4,
                'referencia': '',
                'favorite': False,
                'mora_local': '',
                'rua': '', 
                'bairro': '',
                'n_casa': '', 
                'cidade': '',
                'estado': '',  
                'restricao_sexo': '',
                'pessoas_no_local': '',
                'mobiliado': '',
                'mora_local': '',
                'attributes': [
                    {
                        'label': 'wifi', 
                        'available': True
                    },
                    {
                        'label': 'vaga_carro', 
                        'available': True
                    },
                    {
                        'label': 'mesa', 
                        'available': True
                    },
                    {
                        'label': 'refeicoes', 
                        'available': True
                    },
                    {
                        'label': 'ar_condicionado', 
                        'available': True
                    },
                    {
                        'label': 'maquina_lavar', 
                        'available': True
                    },
                    {
                        'label': 'suite', 
                        'available': True
                    },
                    {
                        'label': 'tv', 
                        'available': True
                    }
                ]
            }]
        
            return Response(dumps(detail), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")


    @jwt_required
    def add_as_favorite(self):
        """Add a relationship between Post and User as Favorite in the database."""
        if request.method == 'POST':
            try:
                id_post = request.form.get("post_id")
                email = get_jwt_identity()
                current_user = User.query.filter_by(email=email).first()
                
                favorite = User_has_Post_as_favorite(current_user.id, id_post)

                db.session.add(favorite)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

        return Response(dumps({"message": "NOT POST"}), status=403, mimetype="application/json")

    @jwt_required
    def remove_favorite(self):
        pass     

    def filter(self):
        """filter data from database."""
        try:
            #http://127.0.0.1:5000/filter?city=araraquara
            # pega a query -> request.args
            # pega uma chave especifica "request.args.get('city')"
            # print(request.args.gets("title"))
        
            info = request.args['title']
            search = "%{}%".format(info)
            
            posts = db.session.query(Post).filter(Post.title.ilike(search)).all()
           
            if posts:
                print(posts)
                return Response(dumps({"message": 'SUCCESS'}), status=200, mimetype="application/json")
            else:
                return Response(dumps({"message": 'NO RESULTS'}), status=404, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")


    def post_author(self):
        try:
            post_id = request.form["post_id"]

            post = Post.query.filter_by(id=post_id).first()
        
            user_id = post.user_id

            user = User.query.filter_by(id=user_id).first()

            author = [{
                'name': user.name,
                'email': user.email,
                'tel': '16994151878', 
                'description': 'Andar de bicicleta, Astrologia, leitura de cartas, Caminhada, Ler, Música, shows, festivais.',
                'img': 'https://assets.b9.com.br/wp-content/uploads/2018/03/544be8a36059997d-1280x720.jpg'
            }]
            return Response(dumps(author), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
