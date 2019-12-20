# Import
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from ..client.model import Client

# Password Encription
from password_strength import PasswordPolicy
import hashlib

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

# Resource
class CreateTokenResource(Resource):
    def get(self):
        # Create Token
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        args = parser.parse_args()

        qry = Client.query.filter_by(client_key = args['client_key']).filter_by(client_secret = args['client_secret'])

        clientData = qry.first()
        clientData = marshal(clientData, Client.jwt_claim_fields)

        # Encript the secret
        secret_key = hashlib.md5('th1s1s1nt3n4lcl13nt'.encode()).hexdigest()

        # Internal Client
        if clientData['client_key'] == 'internal' and clientData['client_secret'] == secret_key:
            token = create_access_token(identity = args['client_key'], user_claims={'client_key': args['client_key']})
        # Non-Interval Client
        else:
            if clientData is not None:
                token = create_access_token(identity = args['client_key'], user_claims={'client_key': args['client_key']})
                return {'token': token}, 200
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

    # Show the payload
    @jwt_required
    def post(self):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        claims = marshal(claims, Client.jwt_claim_fields)
        return claims, 200
        
api.add_resource(CreateTokenResource, '', '/refresh')