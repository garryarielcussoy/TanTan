import pytest, json, logging
from flask import Flask, request

from blueprints import app, db
from blueprints.client.model import Client
from blueprints.user.model import User
from blueprints.book.model import Book
from blueprints.rent.model import Rent
from app import cache

# Password Encription
from password_strength import PasswordPolicy
import hashlib

def db_reset():
    db.drop_all()
    db.create_all()

    password_1 = hashlib.md5("SECRET_01".encode()).hexdigest()
    password_2 = hashlib.md5("'th1s1s1nt3n4lcl13nt'".encode()).hexdigest()
    password_3 = hashlib.md5("SECRET_03".encode()).hexdigest()
    client = Client(1, "CLIENT01", password_1, True)
    db.session.add(client)
    db.session.commit()
    client2 = Client(2, "internal", password_2, True)
    db.session.add(client2)
    db.session.commit()
    client3 = Client(3, "CLIENT03", password_3, True)
    db.session.add(client3)
    db.session.commit()
    user1 = User(1, 1, "Joe", 25, "male")
    user2 = User(2, 2, "Boni", 24, "female")
    user80 = User(80, 2, "Jono", 20, "male")
    user81 = User(81, 1, "Banu", 40, "male")
    db.session.add(user1)
    db.session.commit()
    db.session.add(user2)
    db.session.commit()
    db.session.add(user80)
    db.session.commit()
    db.session.add(user81)
    db.session.commit()
    book1 = Book(1, "Integral Cauchy", "111-111", "Cauchy")
    book2 = Book(2, "Integral Cauchy Jilid 2", "222-222", "Cauchy")
    book5 = Book(5, "Integral Cauchy Jilid 3", "333-333", "Cauchy")
    db.session.add(book1)
    db.session.commit()
    db.session.add(book2)
    db.session.commit()
    db.session.add(book5)
    db.session.commit()
    rent1 = Rent(80, 1, 1)
    rent2 = Rent(81, 1, 11)
    db.session.add(rent1)
    db.session.commit()
    db.session.add(rent2)
    db.session.commit()

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
            'client_key': 'internal',
            'client_secret': 'th1s1s1nt3n4lcl13nt'
        }
    else:
        cachename = "test-non-internal-token"
        data = {
            'client_key': 'CLIENT01',
            'client_secret': 'SECRET01'
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