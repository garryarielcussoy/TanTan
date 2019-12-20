# from unittest import mock
# from unittest.mock import patch
# import json
# from . import app, client, cache, create_token, db_reset

# class TestWeather():
#     # Mocking Function
#     def api_mock_weather(*args, **kwargs):
#         class MockResponse:
#             def __init__(self, json_data, status_code):
#                 self.json_data = json_data
#                 self.status_code = status_code
            
#             def json(self):
#                 return self.json_data
        
#         if len(args)>0:
#             if args[0] == 'https://api.weatherbit.io/v2.0/ip':
#                 return MockResponse({
#                     "latitude": "-6.21462",
#                     "longitude": "106.84513",
#                     "city": "Malang",
#                     "organization": "Alterra",
#                     "timezone": "Asia/Jakarta"
#                 }, 200)
#             elif args[0] == 'https://api.weatherbit.io/v2.0/current':
#                 return MockResponse({
#                     "data":[{"datetime": "50", "temp": "25"}]
#                 }, 200)
#         return MockResponse(None, 404)
    
#     # Get the Weather Test
#     @mock.patch('requests.get', side_effect=api_mock_weather)
#     def test_get_weather(self, test_weather_mock, client):
#         token = create_token(True)
#         data = {"ip":"12.34.56.78"}
#         res = client.get('/weather', query_string = data, headers={'Authorization': 'Bearer ' + token})
#         # res_json = json.loads(res.data)
#         assert res.status_code == 200
#         # assert res_json['city'] == 'Jakarta'
#         # assert res_json['weather'] == 32





#         # parser = reqparse.RequestParser()
#         # parser.add_argument('ip', location='args', default=None)
#         # args = parser.parse_args()
    
#         # # Step - 1 - Check lon lat from ip
#         # rq = requests.get(self.wio_host + '/ip', params={'ip': args['ip'], 'key': self.wio_apikey})
#         # geo = rq.json()
#         # lat = geo['latitude']
#         # lon = geo['longitude']

#         # # Step - 2 - Get current weather from lat lon
#         # rq = requests.get(self.wio_host + '/current', params={'lat': lat, 'lon':lon, 'key': self.wio_apikey})
#         # current = rq.json()

#         # return {
#         #     'city': geo['city'],
#         #     'organization': geo['organization'],
#         #     'timezone': geo['timezone'],
#         #     'current_weather': {
#         #         'date': current['data'][0]['datetime'],
#         #         'temp': current['data'][0]['temp']
#         #     }
#         # }