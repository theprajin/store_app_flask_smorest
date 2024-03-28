from flask import g
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user_model import User


# checks if the user is super admin
def user_is_super(user: User = None):
    def wrapper(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            for role in user.roles:
                if role.is_super:
                    return func(*args, **kwargs)
            else:
                raise ValueError("Unauthorized Access")

        return wrapped_function

    return wrapper


def load_user_from_request(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        user_identity = get_jwt_identity().get("id")

        user = User.query.get(user_identity)

        g.current_user = user

        return fn(*args, **kwargs)

    return wrapper
