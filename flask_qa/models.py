from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5000000))
    password = db.Column(db.String(100000))
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    questions_asked = db.relationship(
        'Question', 
        foreign_keys='Question.asked_by_id', 
        backref='asker', 
        lazy=True
    )

    answers_requested = db.relationship(
        'Question',
        foreign_keys='Question.expert_id',
        backref='expert',
        lazy=True
    )

   # @property
   # def unhashed_password(self):
    #    raise AttributeError('Cannot view unhasshed password!')

    #@unhashed_password.setter
   # def unhashed_password(self, unhashed_password):
    #    self.password = generate_password_hash(unhashed_password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    ans_filename = db.Column(db.String(50))
    ans_data = db.Column(db.LargeBinary)
    image_filename = db.Column(db.String(50))
    image_data = db.Column(db.LargeBinary)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'))