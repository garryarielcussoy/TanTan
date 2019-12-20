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
#     # Get By ID
#     @jwt_required
#     @internal_required
#     def get(self, id=None):
#         qry = Client.query.get(id)
#         if qry:
#             return marshal(qry, Client.client_fields), 200
#         return {'status': 'NOT FOUND'}, 404

#     # Put
#     @jwt_required
#     @internal_required
#     def put(self, id=None):
#         client = Client.query.get(id)
#         client = marshal(client, Client.client_fields)

#         if client['client_id'] != 0:
#             parser = reqparse.RequestParser()
#             parser.add_argument('client_id', type=int, location='json', required=True)
#             parser.add_argument('client_key', location='json', required=True)
#             parser.add_argument('client_secret', location='json', required=True)
#             parser.add_argument('status', location='json',type=inputs.boolean, required=True)
#             args = parser.parse_args()

#             # Updated the object
#             client['client_id'] = args['client_id']
#             client['client_key'] = args['client_key']
#             client['client_secret'] = args['client_secret']
#             client['status'] = args['status']
#             client['updated_at'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#             db.session.commit()
#             app.logger.debug('DEBUG : %s', client)

#             return client, 200, {'Content-Type':'application/json'}
#         return {'status' : 'NOT FOUND'}, 404, {'Content-Type':'application/json'}

#     # Delete
#     @jwt_required
#     @internal_required
#     def delete(self, id=None):
#         client = Client.query.get(id)

#         if client is not None:
#             # Hard Delete
#             db.session.delete(client)
#             db.session.commit()
#             return {'status': 'DELETED'}, 200, {'Content-Type':'application/json'}
#         return {'status' : 'NOT FOUND'}, 404, {'Content-Type':'application/json'}

class ClientList(Resource):
    # Get All
    @jwt_required
    @internal_required
    def get(self):
        # Parsing some parameters
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('client_id', type=int, location='args')
        parser.add_argument('status', location = 'args', help ='invalid status', choices = ('true', 'false', 'True', 'False'))
        args = parser.parse_args()

        # Pagination
        offset = args['rp'] * (args['p'] - 1)

        # Querying all rows of Client Table
        qry = Client.query

        # Status Parameter
        if args['status'] is not None:
            qry = qry.filter_by(status = args['status'])
        
        # Status Client_ID
        if args['client_id'] is not None:
            qry = qry.filter_by(client_id = args['client_id'])
        
        # Store the result in a list and return
        filter_result = []
        for query in qry:
            filter_result.append(marshal(query, Client.client_fields))
        return filter_result
    
#     # Post
#     @jwt_required
#     @internal_required
#     def post(self):
#         # Setup the policy
#         policy = PasswordPolicy.from_names(
#             length = 8
#         )

#         parser = reqparse.RequestParser()
#         parser.add_argument('client_id', type=int, location='json', required=True)
#         parser.add_argument('client_key', location='json', required=True)
#         parser.add_argument('client_secret', location='json', required=True)
#         parser.add_argument('status', location='json',type=inputs.boolean, required=True)
#         args = parser.parse_args()

#         # Validating the password policy
#         validation = policy.test(args['client_secret'])

#         if validation == []:
#             password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()
#             # Creating object
#             client = Client(args['client_id'], args['client_key'], password_digest, args['status'])
#             db.session.add(client)
#             db.session.commit()

#             app.logger.debug('DEBUG : %s', client)

#             return marshal(client, Client.client_fields), 200, {'Content-Type':'application/json'}
#         return {'status': 'Failed'}

api.add_resource(ClientList, '', '/list')
api.add_resource(ClientResource, '/<id>')