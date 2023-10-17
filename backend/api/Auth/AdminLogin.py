import jwt
from functools import wraps
from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from app.validation import *
from app.models import User, db
from app.security import user_datastore
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request

admin_parser = reqparse.RequestParser()
admin_parser.add_argument('username')
admin_parser.add_argument('password')

class AdminLoginAPI(Resource):
    def post(self):
        args = admin_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        admin = None
        if '@' in username:
            admin = db.session.query(User).filter(User.email == username, User.is_admin==True).first()
        else:
            admin = db.session.query(User).filter(User.username == username, User.is_admin==True).first()

        if admin:
            if verify_password(password, admin.password):
                access_token = create_access_token(identity=admin.id, expires_delta=timedelta(seconds=1200))
                login_user(admin)
                return jsonify({'status': 'success','message': 'Admin login Successful!', 'access_token': access_token, "username": username})
            else:
                return jsonify({'status': 'error', 'message': 'Incorrect password!'}), 401
        else:
            # return 401 Unauthorized error
            raise BusinessValidationError(status_code=404, error_code="BE101", error_message="Admin not found! Only for Admins")







def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Verify JWT token in the request

        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        user = User.query.get(user_id)  # Fetch the user object from the database

        if not user or not user.is_admin:
            return jsonify(message="Admin permissions required"), 403

        return func(*args, **kwargs)

    return decorated_function