from app import db
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
    image_file = db.Column(db.String(20))
    price = db.Column(db.Float,nullable=False)
    rate = db.Column(db.Integer,nullable=True)
    favorite = db.Column(db.Boolean,nullable=True)
    address = db.Column(db.String(70),nullable=False)
    neighborhood = db.Column(db.String(40),nullable=False)
    city = db.Column(db.String(40),nullable=False)
    state = db.Column(db.String(40),nullable=False)
    # id do usuário que criou essa tabela, tem que ser igual da class User 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __init__(self, content, title,image_file,price,rate,favorite,address,neighborhood,city,state,author):
        self.content = content
        self.title = title
        #self.date_posted = date_posted
        self.image_file = image_file
        self.price = price
        self.rate = rate
        self.favorite = favorite
        self.address = address
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.user_id = author
        

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}','{self.image_file}')" 
    


