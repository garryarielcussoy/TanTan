import json
from . import app, client, cache, create_token, db_reset

class TestClientCrud():
    # Test Case Post 1
    def test_client_post_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "client_id": 2021,
            "client_key": "CLIENT2021",
            "client_secret": "SECRET2021",
            "status": True
        }

        res = client.post('/client', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['client_id'] > 0
    
    # Test Case Post 2
    def test_client_post_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "client_id": 2019,
            "client_key": 2019,
            "client_secret": "SECRET2019",
            "status": 2
        }

        res = client.post('/client', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # Test Case Post 3
    def test_client_post_non_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "client_id": 2020,
            "client_key": "CLIENT2020",
            "client_secret": "SECRET2020",
            "status": True
        }

        res = client.post('/client', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'FORBIDDEN'
    
    # Test Case Post 4
    def test_client_post_non_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "client_id": 2019,
            "client_key": 2019,
            "client_secret": "SECRET2019",
            "status": 2
        }

        res = client.post('/client', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'FORBIDDEN'
    
    # Test Case Get All 1
    def test_client_get_all_internal_user_without_parameter(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/client', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['client_id'] == 1
        assert res_json[0]['client_key'] == 'CLIENT01'
        assert res_json[0]['status'] == True
    
    # Test Case Get All 2
    def test_client_get_all_internal_user_with_correct_parameter(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "p": 1,
            "rp": 25,
            "client_id": 1,
            "status": True
        }

        res = client.get('/client', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['client_id'] == 1
        assert res_json[0]['client_key'] == 'CLIENT01'
        assert res_json[0]['status'] == True
    
    # Test Case Delete 1
    def test_client_delete_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.delete('/client/3', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json["status"] == "DELETED"
    
    # Test Case Delete 2
    def test_client_delete_internal_user_not_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.delete('/client/1111', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json["status"] == "NOT FOUND"
    
    # Test Case Delete 3
    def test_client_delete_non_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(False)

        res = client.delete('/client/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
    
    # Test Case Put 1
    def test_client_put_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "client_id": 1,
            "client_key": "CLIENT47",
            "client_secret": "SECRET47",
            "status": True
        }

        res = client.put('/client/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json["client_key"] == "CLIENT47"
        assert res_json["client_secret"] == "SECRET47"
    
    # Test Case Put 2
    def test_client_put_internal_user_not_matching_id(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "client_id": 1,
            "client_key": "CLIENT47",
            "client_secret": "SECRET47",
            "status": True
        }

        res = client.put('/client/100', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json["status"] == 'NOT FOUND'
    
    # Test Case Put 3
    def test_client_put_non_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "client_id": 1,
            "client_key": "CLIENT47",
            "client_secret": "SECRET47",
            "status": True
        }

        res = client.put('/client/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
    
    # Test Case Get By ID 1
    def test_client_get_by_id_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/client/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['client_id'] == 1
        assert res_json['client_key'] == 'CLIENT01'
        assert res_json['status'] == True
    
    # Test Case Get By ID 2
    def test_client_get_by_id_internal_user_non_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/client/100', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json['status'] == 'NOT FOUND'