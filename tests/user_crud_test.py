import json
from . import app, client, cache, create_token, db_reset

class TestUserCrud():
    # Test Case Post 1
    def test_user_post_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 5,
            "client_id": 3,
            "name": "Joe",
            "age": 25,
            "sex": "male"
        }

        res = client.post('/user', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['client_id'] == 3
        assert res_json['id'] == 5
        assert res_json['name'] == "Joe"
    
    # Test Case Post 2
    def test_user_post_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 5,
            "client_id": "a",
            "name": "Joe",
            "age": 25,
            "sex": "male"
        }

        res = client.post('/user', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # Test Case Post 3
    def test_user_post_non_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": 5,
            "client_id": 3,
            "name": "Joe",
            "age": 25,
            "sex": "male"
        }

        res = client.post('/user', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'FORBIDDEN'
    
    # Test Case Post 4
    def test_user_post_non_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": 5,
            "client_id": 3,
            "name": "Joe",
            "age": 25,
            "sex": "male"
        }

        res = client.post('/user', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'FORBIDDEN'
    
    # Test Case Get All 1
    def test_user_get_all_internal_user_without_parameter(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/user', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['id'] == 1
        assert res_json[0]['client_id'] == 1
        assert res_json[0]['name'] == "Joe"
        assert res_json[0]['age'] == 25
        assert res_json[0]['sex'] == 'male'
    
    # Test Case Get All 2
    def test_user_get_all_internal_user_with_correct_parameter(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "p": 1,
            "rp": 25,
            "id": 1,
            "name": "Joe",
            "age": 25,
            "sex": "male"
        }

        res = client.get('/user', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['id'] == 1
        assert res_json[0]['client_id'] == 1
        assert res_json[0]['name'] == "Joe"
        assert res_json[0]['age'] == 25
        assert res_json[0]['sex'] == 'male'
    
    # Test Case Delete 1
    def test_user_delete_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.delete('/user/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json["status"] == "DELETED"
    
    # Test Case Delete 2
    def test_user_delete_internal_user_not_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.delete('/user/1111', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json["status"] == "NOT FOUND"
    
    # Test Case Delete 3
    def test_user_delete_non_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(False)

        res = client.delete('/user/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
    
    # Test Case Put 1
    def test_user_put_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 5,
            "client_id": 3,
            "name": "Joni",
            "age": 25,
            "sex": "male"
        }

        res = client.put('/user/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json["name"] == "Joni"
    
    # Test Case Put 2
    def test_user_put_internal_user_not_matching_id(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 5,
            "client_id": 3,
            "name": "Joni",
            "age": 25,
            "sex": "male"
        }

        res = client.put('/user/3000', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json["status"] == 'NOT FOUND'
    
    # Test Case Put 3
    def test_user_put_non_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": 5,
            "client_id": 3,
            "name": "Joni",
            "age": 25,
            "sex": "male"
        }

        res = client.put('/user/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
    
    # Test Case Get By ID 1
    def test_user_get_by_id_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/user/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['client_id'] == 1
        assert res_json['name'] == 'Joe'
        assert res_json['age'] == 25
    
    # Test Case Get By ID 2
    def test_user_get_by_id_internal_user_non_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/user/3', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json['status'] == 'NOT FOUND'