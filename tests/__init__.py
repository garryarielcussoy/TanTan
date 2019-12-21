import pytest, json, logging
from flask import Flask, request

from blueprints import app, db
from blueprints.client.model import Client
from app import cache

# Password Encription
from password_strength import PasswordPolicy
import hashlib

def db_reset():
    db.drop_all()
    db.create_all()

    password_1 = hashlib.md5("password1".encode()).hexdigest()
    client = Client('name1', 'username1', password_1)
    db.session.add(client)

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(isInternal):
    # Checking whether internal or not and prepare the data
    if isInternal:
        cachename = "test-internal-token"
        data = {
            'username': 'internal',
            'password': 'tantan'
        }
    else:
        cachename = "test-non-internal-token"
        data = {
            'username': 'client1',
            'password': 'password1'
        }

    token = cache.get(cachename)
    if token is None:
        # Do Request
        req = call_client(request)
        res = req.get('/token', query_string = data, content_type='application/json')

        # Store Response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # Assertion
        assert res.status_code == 200

        # Save token into cache
        cache.set(cachename, res_json['token'], timeout = 60)

        # Return, because it is useful for other test
        return res_json['token']
    else:
        return token