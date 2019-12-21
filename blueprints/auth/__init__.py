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
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        # Internal Client
        if args['username'] == 'internal' and args['password'] == 'tantan':
            token = create_access_token(identity = args['username'], user_claims={'username': args['username']})
            return {'token': token}, 200

        else:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()
            qry = Client.query.filter_by(username = args['username']).filter_by(password = password_digest)
            clientData = qry.first()
        # Non-Interval Client
            if clientData is not None:
                clientData = marshal(clientData, Client.jwt_claim_fields)
                token = create_access_token(identity = args['username'], user_claims=clientData)
                return {'token': token}, 200
            return {'status': 'BAD REQUEST', 'message': 'invalid username or password'}, 400

    # Show the payload
    @jwt_required
    def post(self):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        claims = marshal(claims, Client.jwt_claim_fields)
        return claims, 200
        
api.add_resource(CreateTokenResource, '')