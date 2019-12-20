import json
from . import app, client, cache, create_token, db_reset

class TestRentCrud():
    # Test Case Post 1
    def test_rent_post_non_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": 5,
            "user_id": 80,
            "book_id": 1
        }

        res = client.post('/rent', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] == 5
        assert res_json['user_id'] == 80
        assert res_json['book_id'] == 1
    
    # Test Case Post 2
    def test_rent_post_non_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": "a",
            "user_id": 1,
            "book_id": 1
        }

        res = client.post('/rent', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # Test Case Post 3
    def test_rent_post_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 5,
            "user_id": 5,
            "book_id": 5
        }

        res = client.post('/rent', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'You are internal user, not permitted here'
    
    # Test Case Post 4
    def test_rent_post_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 5,
            "user_id": 5,
            "book_id": 5
        }

        res = client.post('/rent', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'You are internal user, not permitted here'
    
    # Test Case Get All 1
    def test_rent_get_all_non_internal_user_without_parameter(self, client):
        db_reset()
        token = create_token(False)

        res = client.get('/rent', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['id'] == 11
    
    # Test Case Get All 2
    def test_rent_get_all_non_internal_user_with_correct_parameter(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "p": 1,
            "rp": 25,
            "user_id": 80,
            "book_id": 1
        }

        res = client.get('/rent', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['id'] == 11

    # Test Case Get By ID 1
    def test_rent_get_by_id_non_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(False)

        res = client.get('/rent/11', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] == 11
        assert res_json['book_id'] == 1
        assert res_json['user_id'] == 81
    
    # Test Case Get By ID 2
    def test_rent_get_by_id_non_internal_user_non_matching_id(self, client):
        db_reset()
        token = create_token(False)

        res = client.get('/rent/77', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['message'] == 'It is not your transaction'