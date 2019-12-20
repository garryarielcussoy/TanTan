import json
from . import app, client, cache, create_token, db_reset

class TestAuth():
    # Test Case Create Token 
    def test_get_token_valid(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "username": "test_token",
            "password": "test_pass"
        }

        res = client.get('/token', query_string = data)
        res_json = json.loads(res.data)

        assert res.status_code == 200
    
    # Test Case Post Token
    def test_post_token_valid(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "username": "test_token",
            "password": "test_pass"
        }

        res = client.post('/token', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200
        assert res_json['client_key'] == 'internal'

    def test_post_token_valid(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "username": None,
            "password": None
        }

        res = client.post('/token', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        
        assert res.status_code == 200
        assert res_json['client_key'] == 'internal'