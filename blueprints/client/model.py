# Import
from blueprints import db
from flask_restful import fields

# Create Model
class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)

    client_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'username': fields.String,
        'password': fields.String
    }

    jwt_claim_fields = {
        'username': fields.String,
    }

    def __init__(self, id, name, username, password):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Client %r>' % self.id