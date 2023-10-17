from flask import jsonify, request
from flask_restful import Resource
from app.models import Venue , Show 
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import cache_api
from api.Auth.LoginAPI import user_required

class ShowDetailAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, venue_id, show_id):
        show = cache_api.get_show_by_showvenue(venue_id, show_id)
        if show:
            show_data = {
                'id': show.id,
                'name': show.name,
                'rating': show.rating,
                'tags': show.tags,
                'timings': show.timings,
                'ticket_price': show.ticket_price,
                'venue_id': show.venue_id
            }
            return show_data, 200
        return jsonify({'message': 'Show not found'}), 404