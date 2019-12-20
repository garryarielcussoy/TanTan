# Import
from blueprints import db
from flask_restful import fields

#Others
from datetime import datetime

# Create Model
class Client(db.Model):
    __tablename__ = 'client'
    created_at = db.Column(db.DateTime, server_default = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    updated_at = db.Column(db.DateTime, server_onupdate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    deleted_at = db.Column(db.Boolean, default = False)
    client_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    client_key = db.Column(db.String(255), unique = True, nullable = False)
    client_secret = db.Column(db.String(255), nullable = False)
    status = db.Column(db.Boolean, nullable = False)

    client_fields = {
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'deleted_at': fields.Boolean,
        'client_id': fields.Integer,
        'client_key': fields.String,
        'client_secret': fields.String,
        'status':fields.Boolean
    }

    jwt_claim_fields = {
        'client_key': fields.String,
    }

    def __init__(self, client_id, client_key, client_secret, status):
        self.created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.deleted_at = False
        self.client_id = client_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.status = status

    def __repr__(self):
        return '<Client %r>' % self.client_id