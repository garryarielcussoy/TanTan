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
        # policy setup
        policy = PasswordPolicy.from_names(
            length = 8
        )
        # validasi id gak ngaco
        if int(id) > 0:
            client = Client.query.get(id)
            if client:
                parser = reqparse.RequestParser()
                parser.add_argument('name', location='args', required=True)
                parser.add_argument('username', location='args', required=True)
                parser.add_argument('password', location='args', required=True)
                args = parser.parse_args()
                client = marshal(client, Client.client_fields)

                validation = policy.test(args['password'])
                password_digest = hashlib.md5(args['password'].encode()).hexdigest()

                if validation == []:
                    # Updated the object
                    client['name'] = args['name']
                    client['username'] = args['username']
                    client['password'] = password_digest
                    db.session.commit()
                    app.logger.debug('DEBUG : %s', client)
                    return client, 200, {'Content-Type':'application/json'}
                return {'status' : 'invalid username or password'}, 401, {'Content-Type':'application/json'}
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
        qry = Client.query.all()
        filter_result = []
        for query in qry:
            filter_result.append(marshal(query, Client.client_fields))
        return filter_result
    
    # Post
    @jwt_required
    @internal_required
    def post(self):
        # Setup the policy
        # later add min username length
        policy = PasswordPolicy.from_names(
            length = 8
        )

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='args', required=True)
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        # Validating the password policy
        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()
            # Creating object
            client = Client(args['name'], args['username'], password_digest)
            db.session.add(client)
            db.session.commit()

            app.logger.debug('DEBUG : %s', client)

            return marshal(client, Client.client_fields), 200, {'Content-Type':'application/json'}
        return {'status': 'invalid username or password'}

api.add_resource(ClientList, '')
api.add_resource(ClientResource, '/<id>')