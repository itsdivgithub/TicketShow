from flask import jsonify, request
from flask_restful import Resource
from app.models import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.Auth.LoginAPI import user_required

def get_booked_seats(show_id):
    booked_seats = db.session.query(db.func.sum(Bookings.seats_booked)).filter_by(show_id=show_id).scalar()
    return booked_seats if booked_seats else 0

class GetSeatsAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, show_id, venue_id):
        show = Show.query.get(show_id)
        if not show:
            return jsonify({'error': 'Show not found'}), 404

        venue = Venue.query.get(show.venue_id)
        if not venue:
            return jsonify({'error': 'Venue not found'}), 404

        booked_seats = get_booked_seats(show_id)
        available_seats = venue.capacity - booked_seats

        return jsonify({'available_seats': available_seats})