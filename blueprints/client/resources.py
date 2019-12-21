# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from datetime import datetime
from sqlalchemy import desc
from .model import Client
from blueprints import db, app
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required
from blueprints import internal_required

# Password Encription
from password_strength import PasswordPolicy
import hashlib

# Creating blueprint
bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):
    # Get By ID
    @jwt_required
    @internal_required
    def get(self, id):
        qry = Client.query.get(id)
        if qry:
            return marshal(qry, Client.client_fields), 200
        return {'status': 'NOT FOUND'}, 404

    # Put
    @jwt_required
    @internal_required
    def put(self, id):
        if id > 0:
            client = Client.query.get(id)
            if client:
                client = marshal(client, Client.client_fields)

                parser = reqparse.RequestParser()
                parser.add_argument('id', type=int, location='json', required=True)
                parser.add_argument('name', location='json', required=True)
                parser.add_argument('username', location='json', required=True)
                parser.add_argument('password', location='json', required=True)
                args = parser.parse_args()

                # Updated the object
                client['id'] = args['id']
                client['name'] = args['name']
                client['username'] = args['username']
                client['password'] = args['password']
                db.session.commit()
                app.logger.debug('DEBUG : %s', client)

                return client, 200, {'Content-Type':'application/json'}

            return {'status' : 'NOT FOUND'}, 404, {'Content-Type':'application/json'}
        return {'status' : 'BAD REQUEST'}, 400, {'Content-Type':'application/json'}

    # Delete
    @jwt_required
    @internal_required
    def delete(self, id):
        client = Client.query.get(id)

        if client is not None:
            # Hard Delete
            db.session.delete(client)
            db.session.commit()
            return {'status': 'DELETED'}, 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT FOUND'}, 404, {'Content-Type':'application/json'}

class ClientList(Resource):
    # Get All
    @jwt_required
    @internal_required
    def get(self):
        # Parsing some parameters
        # Pagination
        # offset = args['rp'] * (args['p'] - 1)

        # Querying all rows of Client Table
        qry = Client.query.all()

        # Status Parameter
        # if args['status'] is not None:
        #     qry = qry.filter_by(status = args['status'])
        
        # Status Client_ID
        # if args['id'] is not None:
        #     qry = qry.filter_by(id = args['id'])
        
        # Store the result in a list and return
        filter_result = []
        for query in qry:
            filter_result.append(marshal(query, Client.client_fields))
        return filter_result
    
    # Post
    @jwt_required
    @internal_required
    def post(self):
        # Setup the policy
        # policy = PasswordPolicy.from_names(
        #     length = 8
        # )

        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        # Validating the password policy
        # validation = policy.test(args['client_secret'])

        # if validation == []:
        password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()
        # Creating object
        client = Client(args['id'], args['client_key'], password_digest, args['status'])
        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)

        return marshal(client, Client.client_fields), 200, {'Content-Type':'application/json'}
        # return {'status': 'Failed'}

api.add_resource(ClientList, '')
api.add_resource(ClientResource, '/<id>')