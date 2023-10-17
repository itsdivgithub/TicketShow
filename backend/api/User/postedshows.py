from flask import jsonify
from flask_restful import Resource
from app.models import Show  # Assuming you have a model named "Show" for your shows
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import cache_api
from api.Auth.LoginAPI import user_required

class PostedShowsAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, venue_id):
        
        # Query the database to get all shows for the given venue_id
        shows = cache_api.get_shows_by_venue(venue_id)

        shows_data = [
            {
                'id': show.id,
                'name': show.name,
                'rating': show.rating,
                'tags': show.tags,
            }
            for show in shows
        ]

        return jsonify(shows_data)
