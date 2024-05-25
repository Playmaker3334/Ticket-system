from . import db
from flask_login import UserMixin

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    assigned_to = db.Column(db.String(100), nullable=True)  # Nueva columna para el nombre del usuario

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

