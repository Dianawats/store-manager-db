from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.handlers.user_handler import UserHandler
user_handler = UserHandler()

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