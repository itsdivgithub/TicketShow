from flask import jsonify, request
from flask_restful import Resource
from app.models import Venue  
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import cache_api
from api.Auth.LoginAPI import user_required

class VenueDetailAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, venue_id):
        venue = cache_api.get_venue(venue_id)
        if venue:
            venue_data = {
                'id': venue.id,
                'name': venue.name,
                'place': venue.place,
                'location': venue.location,
                'capacity': venue.capacity
            }
            return venue_data, 200
        return jsonify({'message': 'Venue not found'}), 404
