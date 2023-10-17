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


class AdminDeleteVenueAPI(Resource):
    @jwt_required()
    @admin_required
    def delete(self, venue_id):
        venue = cache_api.get_venue(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404

        show_ids = [show.id for show in venue.shows]

        db.session.query(Bookings).filter(Bookings.show_id.in_(show_ids)).delete(synchronize_session=False)

        db.session.query(Show).filter(Show.venue_id == venue_id).delete()

        db.session.delete(venue)
        db.session.commit()

        return {'message': 'Venue, associated shows, and bookings deleted'}, 200









