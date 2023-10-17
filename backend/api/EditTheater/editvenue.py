import jwt
from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_security import login_user
from app.validation import *
from app.models import User,Venue, db
from app.security import user_datastore
from app import cache_api
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


edittheatre_parser = reqparse.RequestParser()
edittheatre_parser.add_argument('name')
edittheatre_parser.add_argument('location')

class AdminEditTheatreAPI(Resource):
    @jwt_required()
    def put(self, venue_id):
        
        args = edittheatre_parser.parse_args()
        name = args.get("name")
        location = args.get('location')

        venue = cache_api.get_venue(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404

        venue.name = name
        venue.location = location

        db.session.commit()

        return {'message': 'Venue updated successfully'}, 200



