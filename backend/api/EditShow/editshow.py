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

class AdminEditShowAPI(Resource):
    @jwt_required()
    @admin_required
    def put(self, venue_id, show_id):
        args = show_parser.parse_args()

        show = cache_api.get_show_by_showvenue(venue_id, show_id)
        if not show:
            return {'message': 'Show not found'}, 404

        show.name = args['name']

        db.session.commit()

        return {'message': 'Show updated successfully'}, 200
