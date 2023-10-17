from flask import jsonify, request
from flask_restful import Resource
from app.models import * 
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import func
from api.Auth.LoginAPI import user_required


class SearchVenuesAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        place = request.args.get('place')

        if not place:
            return jsonify({'message': 'Place parameter is missing'}), 400

        # Perform the full-text search on the 'place' field using the 'LIKE' operator
        venues = Venue.query.filter(Venue.place.like(f'%{place}%')).all()

        if not venues:
            return jsonify({'message': 'No venues found'}), 404

        venue_list = []
        for venue in venues:
            venue_data = {
                'id': venue.id,
                'name': venue.name,
                'place': venue.place,
                'location': venue.location,
                'capacity': venue.capacity,
            }
            venue_list.append(venue_data)

        return venue_list, 200