# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from datetime import datetime
from sqlalchemy import desc
from .model import User
from blueprints import db, app
import json

# Import Authentication
from flask_jwt_extended import jwt_required
from blueprints import internal_required

# Creating blueprint
bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):
    # Get By ID
    @jwt_required
    @internal_required
    def get(self, id=None):
        qry = User.query.get(id)
        if qry:
            return marshal(qry, User.user_fields), 200
        return {'status': 'NOT FOUND'}, 404

    # Put
    @jwt_required
    @internal_required
    def put(self, id=None):
        user = User.query.filter_by(id=id).first()

        if user is not None:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int, location='json', required=True)
            parser.add_argument('client_id', type=int, location='json', required=True)
            parser.add_argument('name', location='json', required=True)
            parser.add_argument('age', type=int, location='json', required=True)
            parser.add_argument('sex', location='json', required=True)
            args = parser.parse_args()

            # Updated the object
            user = marshal(user, User.user_fields)
            user['id'] = args['id']
            user['client_id'] = args['client_id']
            user['name'] = args['name']
            user['age'] = args['age']
            user['sex'] = args['sex']
            user['updated_at'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            db.session.commit()
            app.logger.debug('DEBUG : %s', user)

            return user, 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT FOUND'}, 404, {'Content-Type':'application/json'}

    # Delete
    @jwt_required
    @internal_required
    def delete(self, id=None):
        user = User.query.filter_by(id=id).first()
        if user is not None:
            # Hard Delete
            db.session.delete(user)
            db.session.commit()
            return {'status': 'DELETED'}, 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT FOUND'}, 404, {'Content-Type':'application/json'}

class UserList(Resource):
    # Get All
    @jwt_required
    @internal_required
    def get(self):
        # Parsing some parameters
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('name', location = 'args')
        parser.add_argument('age', location = 'args')
        parser.add_argument('sex', location = 'args')
        args = parser.parse_args()

        # Pagination
        offset = args['rp'] * (args['p'] - 1)

        # Querying all rows of Client Table
        qry = User.query

        # Name Parameter
        if args['name'] is not None:
            qry = qry.filter_by(name = args['name'])
        
        # Age Parameter
        if args['age'] is not None:
            qry = qry.filter_by(age = args['age'])

        # Sex Parameter
        if args['sex'] is not None:
            qry = qry.filter_by(sex = args['sex'])

        # ID Parameter
        if args['id'] is not None:
            qry = qry.filter_by(id = args['id'])
        
        # Store the result in a list and return
        filter_result = []
        for query in qry:
            filter_result.append(marshal(query, User.user_fields))
        return filter_result
    
    # Post
    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=True)
        parser.add_argument('client_id', type=int, location='json', required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', type=int, location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        args = parser.parse_args()

        # Creating object
        user = User(args['id'], args['client_id'], args['name'], args['age'], args['sex'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, User.user_fields), 200, {'Content-Type':'application/json'}

api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, '/<id>')