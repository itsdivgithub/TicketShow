import jwt
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from app.validation import *
from app.models import *
from app.security import user_datastore
from api.Auth.AdminLogin import admin_required
from app import cache_api
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity




show_parser = reqparse.RequestParser()
show_parser.add_argument('name', type=str, required=True)
show_parser.add_argument('rating', type=int, required=True)
show_parser.add_argument('tags', type=str, required=True)
show_parser.add_argument('timings', type=str, required=True)
show_parser.add_argument('ticket_price', type=int, required=True)

class AdminAddShowAPI(Resource):
    @jwt_required()
    @admin_required
    def post(self, venue_id):
        args = show_parser.parse_args()

        
        name = args['name']
        rating = args['rating']
        tags = args['tags']
        timings = args['timings']
        ticket_price = args['ticket_price']

        new_show = Show(
            name=name,
            rating=rating,
            tags=tags,
            timings=timings,
            ticket_price=ticket_price,
            venue_id=venue_id
        )

       
        db.session.add(new_show)
        db.session.commit()

       
        return {'message': 'Show created successfully', 'show_id': new_show.id}, 201

   

class AdminGetShowAPI(Resource):
    @jwt_required()
    @admin_required
    def get(self, venue_id):
        shows = cache_api.get_shows_by_venue(venue_id)

        show_list = []
        for show in shows:
            show_data = {
                'id': show.id,
                'name': show.name,
                'rating': show.rating,
                'tags': show.tags,
                'timings': show.timings,
                'ticket_price': show.ticket_price,
                'venue_id': show.venue_id
            }
            show_list.append(show_data)

        return {'shows': show_list}
