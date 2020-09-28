# Model, consist of all the model classes such as users and post-messages in db
from datetime import datetime
from application_files import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receiver = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    open_message = db.Column(db.Boolean, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.sender}', '{self.subject}', '{self.open_message},'{self.date_posted}')"






# class User(UserMixin, db.Model):
#     """ User model """
#
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(25), unique=True, nullable=False)
#     hashed_pswd = db.Column(db.String(), nullable=False)
#
# from application_files import db
#
#
# class Message(db.Model):
#     # ID = KEY of a point
#     id = db.Column(db.Integer, primary_key=True)
#     # The point coordinates,represented as a String of length 5, it has to be unique , and it can be null
#     text = db.Column(db.String(5), unique=True, nullable=False)
#     xCoord = db.Column(db.Integer, nullable=False)
#     yCoord = db.Column(db.Integer, nullable=False)
#     def __repr__(self):
#         return f"Point('{self.id}','{self.text}','{self.xCoord}',{self.yCoord}')"
