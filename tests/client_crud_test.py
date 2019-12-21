# import json
# from . import app, client, cache, create_token, db_reset

# class TestClientCrud():

#     # Test Case Post 
#     def test_client_post_valid(self, client):
#         db_reset()
#         token = create_token(True)

#         data = {
#             'name': 'user 01',
#             'username': 'user01',
#             'password': 'passuser01'
#         }

#         res = client.post('/client', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)

#         assert res.status_code == 200
#         assert res_json['client_id'] > 0

#     # Test Case Put 
#     def test_client_put_valid(self, client):
        
#         token = create_token(True)

#         data = {
#             'name': 'user satu',
#             'username': 'usersatu',
#             'password': 'passusersatu'
#         }

#         res = client.put('/client', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)

#         assert res.status_code == 200
#         assert res_json['client_id'] > 0
    
#     # Test Case Get All 
#     def test_client_get_all_valid(self, client):
        
#         token = create_token(True)

#         data = {
#             'p':1,
#             'rp':2
#         }

#         res = client.post('/client', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)

#         assert res.status_code == 200
#         assert res_json['client_id'] > 0
    
#     # Test Case Get by ID 
#     def test_client_get_by_id_valid(self, client):
        
#         token = create_token(True)

#         data = {
#             'p':1,
#             'rp':2
#         }

#         res = client.get('/client/<client_id>', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)

#         assert res.status_code == 200
#         assert res_json['client_id'] > 0
    
#     # Test Case Delete
#     def test_client_delete_by_id_valid(self, client):
        
#         token = create_token(True)

#         data = {
#             'client_id':1
#         }

#         res = client.delete('/client/<client_id>', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)

#         assert res.status_code == 200
#         assert res_json['client_id'] > 0

