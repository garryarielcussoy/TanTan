import json
from . import app, client, cache, create_token, db_reset

class TestAuth():
    # Test Case Create Token 
    def test_get_token_valid_secret_valid_key(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "username": "username1",
            "password": "password1"
        }

        res = client.get('/token', query_string = data)
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Test Case Post Token
    def test_post_token_valid(self, client):
        db_reset()
        token = create_token(True)

        res = client.post('/token', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['username'] == 'internal'