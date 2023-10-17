from flask import jsonify, request
from flask_restful import Resource
from app.models import Venue  
from app import cache_api
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.Auth.LoginAPI import user_required

class PostedVenuesAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        venues = cache_api.get_all_venues()

        venues_data = [
            {
                'id': venue.id,
                'name': venue.name,
                'location': venue.location,
            }
            for venue in venues
        ]

        return jsonify(venues_data)

