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
    # date_birth = db.Column(db.String(10), nullable = False)

    client_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'username': fields.String,
        'password': fields.String,
        # 'date_birth': fields.String
    }

    # translate_fields = {
    #     'text': fields.String
    # }

    jwt_claim_fields = {
        'id' : fields.String,
        'username': fields.String,
    }

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Client %r>' % self.id