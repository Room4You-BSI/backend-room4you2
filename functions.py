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
from unidecode import unidecode

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
        'img': user.image_file
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
                email_cont = request.form["email"]
                pwd = request.form["password"]
                img = request.form["userImg"]
                telPhone = request.form["cell"]
                aboutMe = request.form["aboutMe"]

                existing_user = User.query.filter_by(email=email).first()

                if existing_user:
                    return Response(dumps({"message": "USER ALREADY EXISTS"}), status=422, mimetype="application/json")

                user = User(name, pwd, email, email_cont, img, telPhone, aboutMe)
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
                infos = request.json
                # descricao
                title = infos["title"]
                content = infos["description"]
                price = infos["price"]
                address = infos["rua"]
                bairro = infos["bairro"]
                cep = infos["cep"]
                city = infos["cidade"]
                state = infos["estado"]
                image = str(infos["imgs"])
                
                # inicio
                n_casa = infos["n_casa"]
                referencia = infos["referencia"]
                mora_local = infos["mora_local"] 
                restricao_sexo  = infos["restricao_sexo"]
                pessoas_no_local = infos["pessoas_no_local"]
                mobiliado = infos["mobiliado"] 
                
                # comodidades
                wifi = infos["wifi"] 
                maquina_lavar = infos["maquina_lavar"] 
                vaga_carro = infos["vaga_carro"] 
                refeicao = infos["meals"] 
                suite = infos["suite"] 
                mesa = infos["mesa"]
                ar_condicionado = infos["ar_condicionado"] 
                tv = infos["tv"] 
                
                # user_id do criador
                user_id = get_jwt_identity()

                #jwt_data = get_jwt()  # ->pegar todos os dados do jwt 
                
                titleFilter = unidecode(title.lower() + ' ' + content.lower() + ' ' + address.lower() + ' ' + bairro.lower() + ' ' + city.lower())
                current_post = Post(title, content, price, address, bairro, cep, city, state, image, n_casa, referencia, mora_local, restricao_sexo, pessoas_no_local, mobiliado, titleFilter, user_id)
                
                db.session.add(current_post)
                db.session.commit()

                postID = current_post.id  

                current_comoditie = Comoditie(wifi, maquina_lavar, vaga_carro, refeicao, suite, mesa, ar_condicionado, tv, postID)
              
                db.session.add(current_comoditie)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS", 'post_id': postID}), status=201, mimetype="application/json")

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

            if not posts:
                return Response(dumps({"message": "NO RESULTS"}), status=404, mimetype="application/json")
            
            all_post = []

            isLogged = get_jwt_identity()
            all_fav = []
            if isLogged:
                    favorites = User_has_Post_as_favorite.query.filter_by(user_id=isLogged).all()
                    for favorite in favorites:
                        all_fav.append(favorite.post_id)

            for post in posts:
                comoditie = Comoditie.query.filter_by(post_id=post.id).first()
                
                favorite = False
                if (all_fav):
                    favorite = post.id in all_fav

                # quando tiver implementado rate alterar:
                rateNumb = random.randint(2,5)
                
                image = eval(post.image)
                if (len(image) > 1):
                    image = image[0]
                else:
                    if(len(image) == 0):
                        image = ''

                all_post.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.content,
                    'image': image,
                    'price': post.price,
                    'rate': rateNumb,
                    'distance': post.referencia,
                    'favorite': favorite,
                    'attributesColumn1': [
                        {
                            'label': 'Wifi', 
                            'available': comoditie.wifi
                        },
                        {
                            'label': 'Estacionamento', 
                            'available': comoditie.vaga_carro
                        },
                    ],
                    'attributesColumn2': [
                        {
                            'label': 'Refeições', 
                            'available': comoditie.refeicao
                        }, 
                        {
                            'label': 'Suite', 
                            'available': comoditie.suite
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

            detail = {
                'rate': rateNumb,
                'favorite': favorite,
                'post_id': id,
                'title': post.title,
                'text': post.content,
                'image': eval(post.image),
                'price': post.price,
                'address': post.address, 
                'bairro': post.bairro, 
                'cep': post.cep, 
                'city': post.city,
                'state': post.state,
                'n_casa': post.n_casa,  
                'mora_local': post.mora_local,
                'referencia': post.referencia,
                'restricao_sexo': post.restricao_sexo,
                'pessoas_no_local': post.pessoas_no_local,
                'mobiliado': post.mobiliado,
                'attributes': [
                    {
                        'label': 'wifi', 
                        'available': comoditie.wifi
                    },
                    {
                        'label': 'maquina_lavar', 
                        'available': comoditie.maquina_lavar
                    },
                    {
                        'label': 'vaga_carro', 
                        'available': comoditie.vaga_carro
                    },
                    {
                        'label': 'refeições', 
                        'available': comoditie.refeicao
                    },
                    {
                        'label': 'suite', 
                        'available': comoditie.suite
                    },
                    {
                        'label': 'mesa', 
                        'available': comoditie.mesa
                    },
                    {
                        'label': 'ar_condicionado', 
                        'available': comoditie.ar_condicionado
                    },
                    {
                        'label': 'tv', 
                        'available': comoditie.tv
                    }
                ]
            }
        
            return Response(dumps(detail), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")


    @jwt_required
    def add_as_favorite(self):
        """Add a relationship between Post and User as Favorite in the database."""
        if request.method == 'POST':
            try:
                userID = get_jwt_identity()
                info = request.json
                id_post = info["post_id"]

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
                userID = get_jwt_identity()
                info = request.json
                id_post = info["post_id"]

                favorite = User_has_Post_as_favorite.query.filter_by(user_id=userID, post_id=id_post).first()

                if not favorite:
                    return Response(dumps({"message": "IT IS NOT FAVORITE"}), status=422, mimetype="application/json")
                    
                db.session.delete(favorite)
                db.session.commit()

                return Response(dumps({"message": "SUCCESS"}), status=200, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

        return Response(dumps({"message": "NOT POST"}), status=403, mimetype="application/json")

    @jwt_optional
    def search(self):
        """filter data from database."""
        try:
            #http://127.0.0.1:5000/filter?city=araraquara
            # pega a query -> request.args
            # pega uma chave especifica "request.args.get('city')"
            # print(request.args.gets("title"))
            
            all_post = []

            text_s = request.args['text']
            text_s = "%{}%".format(text_s)
            text_s = unidecode(text_s.lower())
            
            posts = db.session.query(Post).filter(Post.title_filter.ilike(text_s)).all()

            if not posts:
                return Response(dumps({"message": 'NO RESULTS'}), status=404, mimetype="application/json")

            isLogged = get_jwt_identity()
            
            for post in posts:
                comoditie = Comoditie.query.filter_by(post_id=post.id).first()
                favorite = False

                if isLogged:
                    favorite = User_has_Post_as_favorite.query.filter_by(user_id=isLogged, post_id=post.id).first()
                    favorite = bool(favorite)
                
                # quando tiver implementado rate alterar:
                rateNumb = random.randint(2,5)

                image = eval(post.image)
                if (len(image) > 1):
                    image = image[0]
                else:
                    if(len(image) == 0):
                        image = ''

                all_post.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.content,
                    'image': image,
                    'price': post.price,
                    'rate': rateNumb,
                    'distance': post.referencia,
                    'favorite': favorite,
                    'attributesColumn1': [
                        {
                            'label': 'Wifi', 
                            'available': comoditie.wifi
                        },
                        {
                            'label': 'Estacionamento', 
                            'available': comoditie.vaga_carro
                        },
                    ],
                    'attributesColumn2': [
                        {
                            'label': 'Refeições', 
                            'available': comoditie.refeicao
                        }, 
                        {
                            'label': 'Suite', 
                            'available': comoditie.suite
                        }
                    ]
                })

            return Response(dumps(all_post), status=200, mimetype="application/json")    
            
        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")


    def post_author(self, id):
        try:
            post = Post.query.filter_by(id=id).first()
            
            user_id = post.user_id
            user = User.query.filter_by(id=user_id).first()

            author = {
                'name': user.name,
                'email': user.email,
                'email_contato': user.contactEmail, 
                'tel': user.tel, 
                'description': user.description,
                'img': user.image_file
            }
            return Response(dumps(author), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

    
    def upload_photo(self):
        """Upload Photos Service"""
        if request.method == 'POST':
            try:    
                img_file = request.files['images_file']
                
                if not img_file:
                    return Response(dumps({"message": 'NOT UPLOADED'}), status=422, mimetype="application/json")

                if (img_file.content_type != 'image/png') and (img_file.content_type != 'image/jpeg'):
                    return Response(dumps({"message": 'ITS NOT IMAGE'}), status=422, mimetype="application/json")

                now = datetime.timestamp(datetime.now())
                bucket = 'room4you-photos' 
                base_url = 'https://room4you-photos.s3-sa-east-1.amazonaws.com/'
                is_public = 'public-read'
                filename = secure_filename(img_file.filename) + '-' + str(now)  
                content_type = img_file.content_type

                client = boto3.client('s3',
                                    region_name = 'sa-east-1',
                                    endpoint_url = base_url,
                                    aws_access_key_id = 'AKIA24MFWIT23R3GFMY7',
                                    aws_secret_access_key = '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')
                
                resp = client.put_object(Body=img_file,
                                ACL=is_public,
                                Bucket=bucket,
                                Key=filename,
                                ContentType=content_type
                                )
                
                img_resp = base_url + bucket + '/' + filename

                return Response(dumps({'link': img_resp}), status=201, mimetype="application/json")

            except HTTPException as e:
                return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")

        return Response(dumps({"message": "NOT POST"}), status=403, mimetype="application/json")

    
    @jwt_required
    def favorite_list(self):
        """List the favorite rooms from database."""
        try:
            userID = get_jwt_identity()
            favorites = User_has_Post_as_favorite.query.filter_by(user_id=userID).all()

            if not favorites:
                return Response(dumps({"message": "WITHOUT FAVORITE"}), status=404, mimetype="application/json")

            all_post = []
            for favorite in favorites:
                post = Post.query.filter_by(id=favorite.post_id).first()
                comoditie = Comoditie.query.filter_by(post_id=post.id).first()
                
                # quando tiver implementado rate alterar:
                rateNumb = random.randint(2,5)

                image = eval(post.image)
                if (len(image) > 1):
                    image = image[0]
                else:
                    if(len(image) == 0):
                        image = ''

                all_post.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.content,
                    'image': image,
                    'price': post.price,
                    'rate': rateNumb,
                    'distance': post.referencia,
                    'favorite': True,
                    'attributesColumn1': [
                        {
                            'label': 'Wifi', 
                            'available': comoditie.wifi
                        },
                        {
                            'label': 'Estacionamento', 
                            'available': comoditie.vaga_carro
                        },
                    ],
                    'attributesColumn2': [
                        {
                            'label': 'Refeições', 
                            'available': comoditie.refeicao
                        }, 
                        {
                            'label': 'Suite', 
                            'available': comoditie.suite
                        }
                    ]
                })
            
            return Response(dumps(all_post), status=200, mimetype="application/json")
        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
        
        
    @jwt_required
    def my_posts_list(self):
        """List the favorite rooms from database."""
        try:
            userID = get_jwt_identity()
            posts = Post.query.filter_by(user_id=userID).all()

            if not posts:
                return Response(dumps({"message": "WITHOUT POSTS"}), status=404, mimetype="application/json")

            all_fav = []
            favorites = User_has_Post_as_favorite.query.filter_by(user_id=userID).all()
            for favorite in favorites:
                all_fav.append(favorite.post_id)

            all_post = []
            for post in posts:
                comoditie = Comoditie.query.filter_by(post_id=post.id).first()

                favorite = False
                if (all_fav):
                    favorite = post.id in all_fav
                
                # quando tiver implementado rate alterar:
                rateNumb = random.randint(2,5)

                image = eval(post.image)
                if (len(image) > 1):
                    image = image[0]
                else:
                    if(len(image) == 0):
                        image = ''

                all_post.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.content,
                    'image': image,
                    'price': post.price,
                    'rate': rateNumb,
                    'distance': post.referencia,
                    'favorite': favorite,
                    'attributesColumn1': [
                        {
                            'label': 'Wifi', 
                            'available': comoditie.wifi
                        },
                        {
                            'label': 'Estacionamento', 
                            'available': comoditie.vaga_carro
                        },
                    ],
                    'attributesColumn2': [
                        {
                            'label': 'Refeições', 
                            'available': comoditie.refeicao
                        }, 
                        {
                            'label': 'Suite', 
                            'available': comoditie.suite
                        }
                    ]
                })
            
            return Response(dumps(all_post), status=200, mimetype="application/json")
        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")
        
    def upload_photo_list(self):
        """Upload Photos List Service"""
        if request.method == 'POST':
            header['client_max_body_size'] = 0
            try:    
                img_file = request.files.getlist('images_file')

                if not img_file or img_file[0].filename == '':
                    return Response(dumps({"message": 'NOT UPLOADED'}), status=422, mimetype="application/json")

                image_list = []
                qtt_images = len(img_file)
                now = datetime.timestamp(datetime.now())
                bucket = 'room4you-photos'  
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

                    filename = secure_filename(img.filename) + '-' + str(now)  
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
       
    @jwt_optional
    def filter(self):
        """List the rooms from database."""
        try:
            arg = request.query_string
            len(arg.decode('ascii').split('&'))
            posts = db.session.query(Post).all()

            if not posts:
                return Response(dumps({"message": "NO RESULTS"}), status=404, mimetype="application/json")
            
            all_post = []

            isLogged = get_jwt_identity()
            all_fav = []
            if isLogged:
                    favorites = User_has_Post_as_favorite.query.filter_by(user_id=isLogged).all()
                    for favorite in favorites:
                        all_fav.append(favorite.post_id)

            for post in posts:
                comoditie = Comoditie.query.filter_by(post_id=post.id).first()
                
                favorite = False
                if (all_fav):
                    favorite = post.id in all_fav

                # quando tiver implementado rate alterar:
                rateNumb = random.randint(2,5)
                
                image = eval(post.image)
                if (len(image) > 1):
                    image = image[0]
                else:
                    if(len(image) == 0):
                        image = ''

                all_post.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.content,
                    'image': image,
                    'price': post.price,
                    'rate': rateNumb,
                    'distance': post.referencia,
                    'favorite': favorite,
                    'attributesColumn1': [
                        {
                            'label': 'Wifi', 
                            'available': comoditie.wifi
                        },
                        {
                            'label': 'Estacionamento', 
                            'available': comoditie.vaga_carro
                        },
                    ],
                    'attributesColumn2': [
                        {
                            'label': 'Refeições', 
                            'available': comoditie.refeicao
                        }, 
                        {
                            'label': 'Suite', 
                            'available': comoditie.suite
                        }
                    ]
                })
            
            return Response(dumps(all_post), status=200, mimetype="application/json")

        except HTTPException as e:
            return Response(dumps({"message": str(e)}), status=500, mimetype="application/json")