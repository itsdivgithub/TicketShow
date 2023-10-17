from flask import jsonify, request
from flask_restful import Resource
from app.models import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.Auth.LoginAPI import user_required

class BookDashAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        bookings = Bookings.query.filter_by(user_id=user_id).all()
        user_bookings = []

        for booking in bookings:
            show = Show.query.get(booking.show_id)
            venue = Venue.query.get(show.venue_id)
            
            user_booking = {
                'booking_id': booking.id,
                'show_name': show.name,
                'venue_name': venue.name,
                'show_time': show.timings,
                'seats_booked': booking.seats_booked,
                'booked_cost': booking.booked_cost,
            }
            user_bookings.append(user_booking)

        return user_bookings, 200
