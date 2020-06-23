from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable = false)
    password = db.Column(db.String,nullable=false)
    email = db.Column(db.String, unique=True)
    image_file = db.Column(db.String(20))
    posts = db.relationship('Post',backref='Author',lazy = true)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    def __init__(self, name, password, email):
        self.name = name
        self.password = generate_password_hash(password)
        self.email = email

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    title = db.Column(db.Text,nullable=false)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    image_file = db.Column(db.String(20))
    price = db.Column(db.Float,nullable=false)
    rate = db.Column(db.Integer,nullable=true)
    favorite = db.Column(db.Boolean,nullable=true)
    address = db.Column(db.String(70),nullable=false)
    neighborhood = db.Column(db.String(40),nullable=false)
    city = db.Column(db.String(40),nullable=false)
    state = db.Column(db.String(40),nullable=false)
    # id do usuário que criou essa tabela, tem que ser igual da class User 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=false)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}','{self.image_file}')" 
    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id


