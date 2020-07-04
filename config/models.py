from config import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String,nullable = False)
    email = db.Column(db.String,unique=True,nullable = False)
    contactEmail = db.Column(db.String,unique=True,nullable = False)
    image_file = db.Column(db.Text)
    description = db.Column(db.Text, nullable = True, default='')
    tel = db.Column(db.String(15), default='')

    posts = db.relationship('Post', backref='Author', lazy=True)
    favorites = db.relationship('User_has_Post_as_favorite', backref='Author', lazy=True)
    
    def __init__(self, name, password, email, contactEmail, image_file, cell, aboutMe):
        self.name = name
        self.password = generate_password_hash(password)
        self.email = email
        self.contactEmail = contactEmail
        self.image_file = image_file
        self.tel = cell
        self.description = aboutMe

    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.image_file}')"

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text,nullable=False)
    content = db.Column(db.Text)
    price = db.Column(db.Float,nullable=False)
    address = db.Column(db.String(70),nullable=False)
    bairro = db.Column(db.String(40),nullable=False)
    cep = db.Column(db.String(9),nullable=False)
    city = db.Column(db.String(40),nullable=False)
    state = db.Column(db.String(40),nullable=False)
    image = db.Column(db.Text, nullable = False,default=False)
    n_casa  = db.Column(db.String(7),nullable=False)
    referencia = db.Column(db.String(40),nullable=False)
    mora_local = db.Column(db.Boolean, nullable = False,default=False)
    restricao_sexo  = db.Column(db.String(1),nullable=False)
    pessoas_no_local = db.Column(db.Integer,nullable=False)
    mobiliado = db.Column(db.Boolean, nullable = False,default=False)
    comoditie = db.relationship('Comoditie',backref='Post',lazy = True,uselist=False)
    favorite = db.relationship('User_has_Post_as_favorite',backref='Post',lazy = True)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    title_filter = db.Column(db.Text,nullable=False,default='quarto')

    # id do usuário que criou essa tabela, tem que ser igual da class User 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    def __init__(self, title, content, price, address, bairro, cep, city, state, image, n_casa, referencia, mora_local, restricao_sexo, pessoas_no_local, mobiliado, title_filter, author):
        self.title = title
        self.content = content 
        self.price = price
        self.address = address
        self.bairro = bairro
        self.cep = cep
        self.city = city
        self.state = state
        self.image = image
        self.n_casa= n_casa
        self.referencia = referencia
        self.mora_local = mora_local
        self.restricao_sexo = restricao_sexo
        self.pessoas_no_local = pessoas_no_local
        self.mobiliado = mobiliado
        self.title_filter = title_filter
        self.user_id = author
        
    def __repr__(self):
        return f"Post('{self.id}','{self.title}')" 

class Comoditie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wifi = db.Column(db.Boolean, nullable = False,default=False)
    maquina_lavar = db.Column(db.Boolean, nullable = False,default=False)
    vaga_carro = db.Column(db.Boolean, nullable = False,default=False)
    refeicao = db.Column(db.Boolean, nullable = False,default=False)
    suite = db.Column(db.Boolean, nullable = False,default=False)
    mesa = db.Column(db.Boolean, nullable = False,default=False)
    ar_condicionado = db.Column(db.Boolean, nullable = False,default=False)
    tv = db.Column(db.Boolean, nullable = False,default=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)

    def __init__(self, wifi, maquina_lavar, vaga_carro, refeicao, suite, mesa, ar_condicionado, tv, postID):
        self.wifi = wifi
        self.maquina_lavar = maquina_lavar
        self.vaga_carro = vaga_carro
        self.refeicao = refeicao
        self.suite = suite
        self.mesa = mesa
        self.ar_condicionado = ar_condicionado
        self.tv = tv
        self.post_id = postID
        
    def __repr__(self):
        return f"Post('{self.post_id}')" 
    
class User_has_Post_as_favorite(db.Model):
    __tablename__ = "user_has_Post_as_favorite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)

    def __init__(self, user_id,post_id):
        self.user_id = user_id
        self.post_id = post_id
        