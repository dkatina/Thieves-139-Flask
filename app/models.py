from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

db = SQLAlchemy()

follower_followed = db.Table(
    'follower_followed',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='author')
    following = db.relationship('User',
                                secondary= follower_followed,
                                primaryjoin = (follower_followed.columns.follower_id == id),
                                secondaryjoin = (follower_followed.columns.followed_id == id),
                                backref= "followed_by",
                                lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, img_url, caption, user_id, location=''):
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id
        self.location = location

    def save(self):
        db.session.add(self)
        db.session.commit()




