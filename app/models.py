from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import db, login, app
from hashlib import md5
import jwt
from time import time

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now)
    posts = db.relationship("Post", backref='author', lazy='dynamic')

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm="HS256")
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id=jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256']) ['reset_password']
            
            
        except:
            return
        return User.query.get(id)
    def __repr__ (self):
        return f'User {self.username}'
    
    def avatar(self,size):
       digest= md5(self.email.lower().encode('utf-8')).hexdigest()
       return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    #Password hashing

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(360))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__ (self):
        return f'Post {self.body}'
    

    