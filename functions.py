import re
import random
import boto3

from flask import request, redirect, url_for, Response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity, jwt_optional, get_jwt
from config.models import User, Post, Comoditie, User_has_Post_as_favorite
from config import db, jwt

from json import dumps
from http import HTTPStatus
from http.client import HTTPException
from datetime import datetime, timedelta

from werkzeug.utils import secure_filename

#db.create_all()

# ""Creating error cases JWT""
@jwt.expired_token_loader
def my_expired_token_callback():
    return Response(dumps([{"message": "Token has expired"}]), status=401, mimetype="application/json")

@jwt.invalid_token_loader
def invalid_token_callback(self):
    return Response(dumps([{"message": "Invalid JWT"}]), status=401, mimetype="application/json")

@jwt.unauthorized_loader
def unauthorized_token_callback(self):
    return Response(dumps([{"message": "Missing JWT"}]), status=403, mimetype="application/json")

@jwt.jwt_data_loader
def add_claims_to_access_token(identity):
    # exp -> now + 12 hours
    now = datetime.utcnow()
    hours = timedelta(hours=12)

    user = User.query.filter_by(id=identity).first()

    return {
        'exp': now + hours,
        'iat': now,
        'nbf': now,
        'sub': identity,
        'name': user.name,
        'img': user.image_file, 
        'description': user.description
    }

#""Flask Functions""
class Views(object):


    def home(self):
        return Response(dumps([{"message": "SUCCESS"}]), status=200, mimetype="application/json")
    

    def register(self):
        """Register a user in the database."""
        if request.method == 'POST':
            try:
                name = request.form["nome"]
                email = request.form["email"]
                pwd = request.form["password"]
                img = request.form["userImg"]
                telPhone = request.form["cell"]
                aboutMe = request.form["aboutMe"]

                existing_user = User.query.filter_by(email=email).first()

                if existing_user:
                    return Response(dumps({"message": "USER ALREADY EXISTS"}), status=422, mimetype="application/json")

                user = User(name, pwd, email, img, telPhone, aboutMe)
                db.session.add(user)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=201, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
        
        return Response(dumps({"message": "NOT AVAILABLE"}), status=403, mimetype="application/json")


    @jwt_required
    def create_post(self):
        """Register a Post in the database."""
        if request.method == 'POST':
            try:
                
                # descricao
                title = request.form["title"]
                content = request.form.get("content")
                #image = request.form["image_file"]
                price = request.form["price"]
                address = request.form["address"]
                bairro = request.form["bairro"]
                cep = request.form["cep"]
                city = request.form["city"]
                state = request.form["state"]
                image = request.form["imgs"]

                # inicio
                n_casa = request.form["n_casa"]
                referencia = request.form["referencia"]
                mora_local = bool(int(request.form["mora_local"]))
                restricao_sexo  = request.form["restricao_sexo"]
                pessoas_no_local = request.form["pessoas_no_local"]
                mobiliado = bool(int(request.form["mobiliado"]))
                
                # comodidades
                wifi = bool(int(request.form["wifi"]))
                maquina_lavar = bool(int(request.form["maquina_lavar"]))
                vaga_carro = bool(int(request.form["vaga_carro"]))
                refeicao = bool(int(request.form["refeicao"]))
                suite = bool(int(request.form["suite"]))
                mesa = bool(int(request.form["mesa"]))
                ar_condicionado = bool(int(request.form["ar_condicionado"]))
                tv = bool(int(request.form["tv"]))

                # user_id do criador
                user_id = get_jwt_identity()

                #jwt_data = get_jwt()  # ->pegar todos os dados do jwt 
                
                current_post = Post(title, content, price, address, bairro, cep, city, state, image, n_casa, referencia, mora_local, restricao_sexo, pessoas_no_local, mobiliado, user_id)
                              
                db.session.add(current_post)
                db.session.commit()

                postID = current_post.id  

                current_comoditie = Comoditie(wifi, maquina_lavar, vaga_carro, refeicao, suite, mesa, ar_condicionado, tv, postID)

                db.session.add(current_comoditie)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=201, mimetype="application/json")

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
                    return Response(dumps({"message": "NOT FOUND"}), status=422, mimetype="application/json")
                
                if not user.verify_password(pwd):
                    return Response(dumps({"message": "NOT FOUND"}), status=422, mimetype="application/json")
               
                return Response(dumps({"message": "SUCCESS", "jwt": create_jwt(identity=user.id)}), status=200, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
            
        return Response(dumps({"message": "NOT AVAILABLE"}), status=403, mimetype="application/json")

    @jwt_optional
    def rooms_list(self):
        """List the rooms from database."""
        try:
            posts = db.session.query(Post).all()
            all_post = []

            # quando tiver implementado rate alterar:
            rateNumb = random.randint(2,5)

            isLogged = get_jwt_identity()
            
            for post in posts:
                comoditie = Comoditie.query.filter_by(post_id=post.id).first()
                favorite = False

                if isLogged:
                    favorite = User_has_Post_as_favorite.query.filter_by(user_id=isLogged, post_id=post.id).first()
                    favorite = bool(favorite)
                
                all_post.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.content,
                    'image': post.image,
                    'price': post.price,
                    'rate': rateNumb,
                    'distance': post.content,
                    'favorite': favorite,
                    'attributesColumn1': [
                        {
                            'label': 'Wifi', 
                            'available': bool(comoditie.wifi)
                        },
                        {
                            'label': 'Estacionamento', 
                            'available': bool(comoditie.vaga_carro)
                        },
                    ],
                    'attributesColumn2': [
                        {
                            'label': 'Refeições', 
                            'available': bool(comoditie.refeicao)
                        }, 
                        {
                            'label': 'Suite', 
                            'available': bool(comoditie.suite)
                        }
                    ]
                })
            
            return Response(dumps(all_post), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

    @jwt_optional
    def rooms_detail(self, id):
        """List the rooms from database."""
        try:
            post = Post.query.filter_by(id=id).first()

            if not post:
                return Response(dumps({"message": "POST NOT FOUND"}), status=404, mimetype="application/json")

            comoditie = Comoditie.query.filter_by(post_id=id).first()
            
            # quando tiver implementado rate alterar:
            rateNumb = random.randint(2,5)
           
            isLogged = get_jwt_identity()
            favorite = None

            if isLogged:
                favorite = User_has_Post_as_favorite.query.filter_by(user_id=isLogged, post_id=id).first()
                favorite = bool(favorite)

            detail = [{
                'rate': rateNumb,
                'favorite': favorite,
                'post_id': id,
                'title': post.title,
                'text': post.content,
                'image': post.image,
                'price': post.price,
                'address': post.address, 
                'bairro': post.bairro, 
                'cep': post.cep, 
                'city': post.city,
                'state': post.state,
                'n_casa': post.n_casa,  
                'mora_local': bool(int(post.mora_local)),
                'referencia': post.referencia,
                'restricao_sexo': post.restricao_sexo,
                'pessoas_no_local': post.pessoas_no_local,
                'mobiliado': bool(int(post.mobiliado)),
                'attributes': [
                    {
                        'label': 'wifi', 
                        'available': bool(int(comoditie.wifi))
                    },
                    {
                        'label': 'maquina_lavar', 
                        'available': bool(int(comoditie.maquina_lavar))
                    },
                    {
                        'label': 'vaga_carro', 
                        'available': bool(int(comoditie.vaga_carro))
                    },
                    {
                        'label': 'refeições', 
                        'available': bool(int(comoditie.refeicao))
                    },
                    {
                        'label': 'suite', 
                        'available': bool(int(comoditie.suite))
                    },
                    {
                        'label': 'mesa', 
                        'available': bool(int(comoditie.mesa))
                    },
                    {
                        'label': 'ar_condicionado', 
                        'available': bool(int(comoditie.ar_condicionado))
                    },
                    {
                        'label': 'tv', 
                        'available': bool(int(comoditie.tv))
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
                userID = get_jwt_identity()
                
                already = User_has_Post_as_favorite.query.filter_by(user_id=userID, post_id=id_post).first()
                
                if already:
                     return Response(dumps({"message": "ALREADY FAVORITE"}), status=422, mimetype="application/json")

                favorite = User_has_Post_as_favorite(userID, id_post)

                db.session.add(favorite)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

        return Response(dumps({"message": "NOT POST"}), status=403, mimetype="application/json")

    @jwt_required
    def remove_favorite(self):  
        """Remove a relationship between Post and User as Favorite in the database."""
        if request.method == 'POST':
            try:
                id_post = request.form.get("post_id")
                userID = get_jwt_identity()
                
                favorite = User_has_Post_as_favorite.query.filter_by(user_id=userID, post_id=id_post).first()

                if not favorite:
                    return Response(dumps({"message": "IT IS NOT FAVORITE"}), status=422, mimetype="application/json")
                    
                db.session.delete(favorite)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

        return Response(dumps({"message": "NOT POST"}), status=403, mimetype="application/json")

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


    def post_author(self, id):
        try:
            post = Post.query.filter_by(id=id).first()
        
            user_id = post.user_id
            user = User.query.filter_by(id=user_id).first()

            author = [{
                'name': user.name,
                'email': user.email,
                'tel': user.tel, 
                'description': user.description,
                'img': user.image_file
            }]
            return Response(dumps(author), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")


    def upload_photo(self, paste='room'):
        """Upload Photos Service"""
        if request.method == 'POST':
            try:    
                img_file = request.files.getlist('userImg')

                if not img_file or img_file[0].filename == '':
                    return Response(dumps({"message": 'NOT UPLOADED'}), status=422, mimetype="application/json")

                image_list = []
                qtt_images = len(img_file)
                now = now = datetime.utcnow()
                bucket = paste + '-room4you-photos' 
                base_url = 'https://room4you-photos.s3-sa-east-1.amazonaws.com/'
                is_public = 'public-read'

                client = boto3.client('s3',
                                    region_name = 'sa-east-1',
                                    endpoint_url = base_url,
                                    aws_access_key_id = 'AKIA24MFWIT23R3GFMY7',
                                    aws_secret_access_key = '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')
            
                for img in img_file:    
                    if (img.content_type != 'image/png') and (img.content_type != 'image/jpeg'):
                        return Response(dumps({"message": 'ITS NOT IMAGE'}), status=422, mimetype="application/json")

                    filename = paste + '-' + secure_filename(img.filename) + '-' + str(now)  
                    content_type = img.content_type
                    
                    resp = client.put_object(Body=img,
                                    ACL=is_public,
                                    Bucket=bucket,
                                    Key=filename,
                                    ContentType=content_type
                                    )
                
                    image_list.append(base_url + bucket + '/' + filename)

                return Response(dumps({'link': image_list}), status=201, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

        return Response(dumps({"message": "NOT POST"}), status=403, mimetype="application/json")
        
        
        
        
        
       
        