from config import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String,unique = True,nullable = False)
    image_file = db.Column(db.String(20))
    posts = db.relationship('Post',backref='Author',lazy = True)
    favorites = db.relationship('User_has_Post_as_favorite',backref='Author',lazy = True)
    
    def __init__(self, name, password, email,image_file):
        self.name = name
        self.password = generate_password_hash(password)
        self.email = email
        self.image_file = image_file
    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.image_file}')"

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    title = db.Column(db.Text,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    price = db.Column(db.Float,nullable=False)
    rate = db.Column(db.Integer,nullable=True)
    address = db.Column(db.String(70),nullable=False)
    neighborhood = db.Column(db.String(40),nullable=False)
    cep = db.Column(db.String(9),nullable=False)
    city = db.Column(db.String(40),nullable=False)
    n_casa  = db.Column(db.String(7),nullable=False)
    state = db.Column(db.String(40),nullable=False)
    referencia = db.Column(db.String(40),nullable=False)
    mora_local = db.Column(db.Boolean, nullable = False,default=False)
    restricao_sexo  = db.Column(db.String(1),nullable=False)
    pessoas_no_local = db.Column(db.Integer,nullable=False)
    mobiliado = db.Column(db.Boolean, nullable = False,default=False)
    comoditie = db.relationship('Comoditie',backref='Post',lazy = True,uselist=False)
    image = db.relationship('Image',backref='Post',lazy = True)
    favorite = db.relationship('User_has_Post_as_favorite',backref='Post',lazy = True)

    # id do usuário que criou essa tabela, tem que ser igual da class User 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
<<<<<<< HEAD

    def __init__(self, content, title,price,rate,address,neighborhood,cep,city,state,n_casa,referencia,mora_local,restricao_sexo,mobiliado,author):
=======
>>>>>>> b50783fafe27ae70a6c26755013068a7fb5397e2
        self.content = content
        self.title = title
        #self.date_posted = date_posted
        self.price = price
        self.rate = rate
        self.address = address
        self.neighborhood = neighborhood
        self.cep = cep
        self.city = city
        self.state = state
        self.n_casa= n_casa
        self.referencia = referencia
        self.mora_local = mora_local
        self.restricao_sexo = restricao_sexo
        self.mobiliado = mobiliado
        
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

    def __init__(self, content):
        self.content = content
        
        
    def __repr__(self):
        return f"Post('{self.content}')" 
    


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text,nullable = False)
    priority = db.Column(db.Integer,nullable=False)
    
    # id do usuário que criou essa tabela, tem que ser igual da class User 
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)

    def __init__(self, url, priority):
        self.url = url
        self.priority = priority
        
    def __repr__(self):
        return f"Post('{self.url}','{self.priority}','{self.image_file}')" 
    



# class User_has_rated_Post(db.Model):
#     __tablename__ = "post"
#     id = db.Column(db.Integer, primary_key=True)
    
#     # id do usuário que criou essa tabela, tem que ser igual da class User 
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

#     def __init__(self, content, title,image_file,price,rate,favorite,address,neighborhood,cep,city,state,author):
#         self.content = content
#         self.title = title
#         #self.date_posted = date_posted
        
            
#     def __repr__(self):
#         return f"Post('{self.title}','{self.date_posted}','{self.image_file}')" 
    

class User_has_Post_as_favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
    # id do usuário que criou essa tabela, tem que ser igual da class User 

    def __init__(self, user_id,post_id):
        self.user_id = user_id
        self.post_id = post_id
        #self.date_posted = date_posted
        

