import json
from . import app, client, cache, create_token, db_reset

class TestBookCrud():
    # Test Case Post 1
    def test_book_post_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 3,
            "title": "Buku Olimpiade",
            "isbn": "123-456",
            "writer": "Garry",
        }

        res = client.post('/book', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] == 3
        assert res_json['title'] == "Buku Olimpiade"
        assert res_json['writer'] == "Garry"
    
    # Test Case Post 2
    def test_book_post_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": "a",
            "title": "Buku Olimpiade",
            "isbn": "123-456",
            "writer": "Garry",
        }

        res = client.post('/book', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # Test Case Post 3
    def test_book_post_non_internal_user_valid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": 3,
            "title": "Buku Olimpiade",
            "isbn": "123-456",
            "writer": "Garry",
        }

        res = client.post('/book', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'FORBIDDEN'
    
    # Test Case Post 4
    def test_book_post_non_internal_user_invalid_body(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": 3,
            "title": "Buku Olimpiade",
            "isbn": "123-456",
            "writer": "Garry",
        }

        res = client.post('/book', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json['status'] == 'FORBIDDEN'
    
    # Test Case Get All 1
    def test_book_get_all_internal_user_without_parameter(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/book', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['id'] == 1
        assert res_json[0]['title'] == "Integral Cauchy"
        assert res_json[0]['isbn'] == "111-111"
        assert res_json[0]['writer'] == "Cauchy"
    
    # Test Case Get All 2
    def test_book_get_all_internal_user_with_correct_parameter(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "p": 1,
            "rp": 25,
            "title": "Integral Cauchy",
            "isbn": "111-111"
        }

        res = client.get('/book', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['id'] == 1
        assert res_json[0]['title'] == "Integral Cauchy"
        assert res_json[0]['isbn'] == "111-111"
        assert res_json[0]['writer'] == "Cauchy"
    
    # Test Case Delete 1
    def test_book_delete_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.delete('/book/2', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json["status"] == "DELETED"
    
    # Test Case Delete 2
    def test_book_delete_internal_user_not_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.delete('/book/1111', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json["status"] == "NOT FOUND"
    
    # Test Case Delete 3
    def test_book_delete_non_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(False)

        res = client.delete('/book/2', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
    
    # Test Case Put 1
    def test_book_put_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 1,
            "title": "Integral Cauchy",
            "isbn": "111-111",
            "writer": "Einstein",
        }

        res = client.put('/book/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res_json['id'] == 1
        assert res_json['title'] == "Integral Cauchy"
        assert res_json['isbn'] == "111-111"
        assert res_json['writer'] == "Einstein"
    
    # Test Case Put 2
    def test_book_put_internal_user_not_matching_id(self, client):
        db_reset()
        token = create_token(True)

        data = {
            "id": 1,
            "title": "Integral Cauchy",
            "isbn": "111-111",
            "writer": "Einstein",
        }

        res = client.put('/book/3000', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json["status"] == 'NOT FOUND'
    
    # Test Case Put 3
    def test_book_put_non_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(False)

        data = {
            "id": 1,
            "title": "Integral Cauchy",
            "isbn": "111-111",
            "writer": "Einstein",
        }

        res = client.put('/book/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
    
    # Test Case Get By ID 1
    def test_book_get_by_id_internal_user_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/book/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] == 1
        assert res_json['isbn'] == '111-111'
        assert res_json['title'] == 'Integral Cauchy'
        assert res_json['writer'] == 'Cauchy'
    
    # Test Case Get By ID 2
    def test_book_get_by_id_internal_user_non_matching_id(self, client):
        db_reset()
        token = create_token(True)

        res = client.get('/book/3', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        assert res_json['status'] == 'NOT FOUND'