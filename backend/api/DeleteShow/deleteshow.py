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


class AdminDeleteShowAPI(Resource):
    @jwt_required()
    @admin_required
    def delete(self, venue_id, show_id):
        show = cache_api.get_show_by_showvenue(venue_id, show_id)
        if not show:
            return {'message': 'Show not found'}, 404
        
        db.session.query(Bookings).filter(Bookings.show_id == show_id).delete()

        db.session.delete(show)
        db.session.commit()

        return {'message': 'Show deleted successfully'}, 200