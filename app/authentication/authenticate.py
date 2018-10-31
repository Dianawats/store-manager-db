from flask import jsonify, request, Blueprint
from flask.views import MethodView
from functools import wraps
from flask_jwt_extended import (create_access_token, 
                                get_jwt_identity, 
                                verify_jwt_in_request)
from app.validation import Validator 
from app.handlers.user_handler import UserHandler
import datetime


validate = Validator()
user_handler = UserHandler()
auth_blueprint = Blueprint("auth_blueprint", __name__)

class RegisterStoreAttendant(MethodView):
    """This class view registers store attendants"""
    
    def post(self):
        #registers a store attendant
        data = request.get_json()
        search_keys = ("username", "phone", "role", "password")
        if all(key in data.keys() for key in search_keys):
            username = data.get("username")
            phone = data.get("phone")
            role = data.get("role")
            password = data.get("password")
        
            invalid = validate.user_validator(username, phone, role, password)
            if invalid:
                return jsonify({"message": invalid}), 400
            username_exists = user_handler.check_whether_user_exists(username=username)
            if username_exists:
                return jsonify({"message": "username already exists"}), 409
            phone_exists = user_handler.check_whether_phone_exists(phone=phone)
            if phone_exists:
                return jsonify({"message": "phone already exists"}), 409
            new_user = user_handler.add_attendant(username=username,
                                                  phone=phone,
                                                  role=role, 
                                                  password=password)
            if new_user:
                return jsonify({"message": 
                                "Store Attendant account has been created"}), 201
            else:
                return jsonify({"message": "No Account created yet"}), 400
        return jsonify({"message": 
                        "You missed some key in your registration body"}), 400

class LoginView(MethodView):
    """
    This class-based view handles user login and access token generation.
    """
    def post(self):
        data = request.get_json()
        search_keys = ("username", "password")
        if all(key in data.keys() for key in search_keys):
            username = data.get("username")
            password = data.get("password")

            invalid = validate.login_validator(username, password)
            if invalid:
                return jsonify({"message": invalid}), 400

            user_token = {}
            expires = datetime.timedelta(days=2)
            given_access = user_handler.user_login(username=username, password=password)
            if given_access:
                access_token = create_access_token(identity= given_access["username"], 
                                                   expires_delta=expires)
                user_token["user logged in"]=username
                user_token["token"] = access_token
                return jsonify(user_token), 200
            return jsonify({"message": "user does not exist"}), 404
        return jsonify({"message": "You missed some key in the login body"}), 400

registration_view = RegisterStoreAttendant.as_view("registration_view")
auth_blueprint.add_url_rule("/api/auth/register",view_func=registration_view, methods=["POST"])

login_view = LoginView.as_view("login_view")
auth_blueprint.add_url_rule("/api/auth/login",view_func=login_view, methods=["POST"])

def requires_admin_permission(zy):
    """
    This is a decorator function to wrap and replace the normal jwt_required function
    """
    @wraps(zy)
    def decorated_function(*args, **kwargs):
        # check user role in token.
        verify_jwt_in_request()
        logged_user = get_jwt_identity()
        user_role = user_handler.get_user_role(username=logged_user)
        if user_role["role"] != 'admin':
            return jsonify({"message": "You need to get permission from admin to access this route"}), 403
        else:
            return zy(*args, **kwargs)
    return decorated_function

