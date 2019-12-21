import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required

bp_tembak = Blueprint('tembak', __name__)
api = Api(bp_tembak)

class GetMateToEat(Resource):
    geo_location = 'https://api.ipgeolocation.io'
    geo_location_api_key = '49794d165c0541438235dd9544a7922a'
    zomato_host = 'https://developers.zomato.com/api/v2.1/search'
    zomato_api_key = '652b214e65c6d08ddcd5246fd4f8fd2d'
    meetup_host = 'https://api.meetup.com/find/locations'

    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()
    
        # Step - 1 - Check lon lat from ip
        rq = requests.get(self.geo_location + '/ipgeo', params={'ip': args['ip'], 'apiKey': self.geo_location_api_key})
        rq_json = rq.json()
        lat = rq_json['latitude']
        lon = rq_json['longitude']
        print(lat," halo ", lon)

        # Step - 2 - Get nearby restaurant
        rq = requests.get(self.zomato_host, headers={'user-key': self.zomato_api_key}, params={'lat': lat, 'lon':lon, 'radius': 100000, 'count': 5})
        rq_json = rq.json()

        restaurant_list = []
        for restaurant in rq_json['restaurants']:
            detail_info = {
                "Nama Restaurant": restaurant['restaurant']['name'],
                "Lokasi": restaurant['restaurant']['location']['address'],
                "Pilihan Menu": restaurant['restaurant']['cuisines'],
                "Jam Buka": restaurant['restaurant']['timings'],
                "Rating": restaurant['restaurant']['user_rating']['aggregate_rating']
            }
            restaurant_list.append(detail_info)

        # Step - 3 - Finding nearby friends
        nearby_friends = requests.get(self.meetup_host, params={"lat": lat, "lon": lon})
        nearby_friends = nearby_friends.json()

        if len(nearby_friends) >= 3:
            n = 3
        else:
            n = len(nearby_friends)

        return {
            "Daftar Restaurant Terdekat:" : restaurant_list,
            "Daftar Teman yang Bisa Diajak" : nearby_friends[0:n]
        }, 200

api.add_resource(GetMateToEat, '')