import jwt
from flask import jsonify
from api.Auth.AdminLogin import admin_required
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from app.validation import *
from app.models import User,Venue, db
from app.security import user_datastore
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import cache_api

addtheatre_parser = reqparse.RequestParser()
addtheatre_parser.add_argument('name')
addtheatre_parser.add_argument('place')
addtheatre_parser.add_argument('location')
addtheatre_parser.add_argument('capacity')

class AdminAddTheatreAPI(Resource): 
    @jwt_required()
    @admin_required
    def post(self):
        args = addtheatre_parser.parse_args()
        name = args.get("name", None)
        place = args.get("place", None)
        location = args.get("location", None)
        capacity = args.get("capacity", None)
        
        new_theatre = Venue(name=name, place=place, capacity=capacity,location=location)
        db.session.add(new_theatre)
        db.session.commit()

        return {'message': 'Theatre added successfully'}, 201

class AdminGetTheatreAPI(Resource):
    @jwt_required()
    @admin_required
    
    def get(self):
        
        venues = cache_api.get_all_venues()

        venues_data = []
        for venue in venues:
            venue_data = {
                "id": venue.id,
                "name": venue.name,
                "place": venue.place,
                "location": venue.location,
                "capacity": venue.capacity
            }
            venues_data.append(venue_data)

        return venues_data, 200
