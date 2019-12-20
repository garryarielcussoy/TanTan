# Import
from blueprints import db
from flask_restful import fields

#Others
from datetime import datetime

# Create Model
class User(db.Model):
    __tablename__ = 'user'
    created_at = db.Column(db.DateTime, server_default = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    updated_at = db.Column(db.DateTime, server_onupdate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    deleted_at = db.Column(db.Boolean, default = False)
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    name = db.Column(db.String(255), nullable = False)
    age = db.Column(db.Integer, default = 0)
    sex = db.Column(db.String(10), nullable = False)

    user_fields = {
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'deleted_at': fields.Boolean,
        'id': fields.Integer,
        'client_id': fields.Integer,
        'name': fields.String,
        'age': fields.Integer,
        'sex':fields.String
    }

    def __init__(self, id, client_id, name, age, sex):
        self.id = id
        self.created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.deleted_at = False
        self.client_id = client_id
        self.name = name
        self.age = age
        self.sex = sex

    def __repr__(self):
        return '<User %r>' % self.id