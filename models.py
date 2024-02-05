"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

class Post(db.Model):
    __tablename__ = 'posts'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable = False)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    user = db.relationship('User', backref = 'posts')

    def __repr__(self):
        return f'<Post {self.title} by User {self.user_id}>'
