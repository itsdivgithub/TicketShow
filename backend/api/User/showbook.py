from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import *
from app import cache_api
from api.Auth.LoginAPI import user_required


book_parser = reqparse.RequestParser()
book_parser.add_argument('seats_booked', type=int)

# API resource for booking a show
# Remove the total_seats_booked property from the Show model

# BookShowAPI class
class BookShowAPI(Resource):
    @jwt_required()
    @user_required
    def post(self, venue_id, show_id):
        args = book_parser.parse_args()
        seats_booked = args.get('seats_booked')

        # Retrieve the user ID from the current user session or authentication token
        user_id = get_jwt_identity()

        # Get the venue associated with the venue_id
        venue = cache_api.get_venue(venue_id)

        if not venue:
            return {'message': 'Venue not found'}, 404

        # Get the show associated with the show_id and venue_id
        show = cache_api.get_show_by_showvenue(venue_id, show_id)

        if not show:
            return {'message': 'Show not found'}, 404

        # Calculate the total seats already booked for the show
        total_seats_booked = show.total_seats_booked

        # Check if there are enough available seats for booking
        available_seats = venue.capacity - total_seats_booked
        if seats_booked > available_seats:
            return {'message': 'Not enough available seats for booking'}, 400

        # Calculate the booked_cost based on the number of seats booked and ticket price
        booked_cost = seats_booked * show.ticket_price

        # Create a booking record in the Bookings table
        booking = Bookings(user_id=user_id, show_id=show_id, seats_booked=seats_booked, booked_cost=booked_cost)
        db.session.add(booking)

        # Update the available seats for the show
        show.available_seats = available_seats - seats_booked

        # Commit the changes to the database
        db.session.commit()

        return {'message': 'Booking successful', 'available_seats': show.available_seats}, 200







