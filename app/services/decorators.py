from flask import current_app, g
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user_model import User
from app.services.exceptions import UnauthorizedAccessException


def load_user_from_request(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        user_identity = get_jwt_identity().get("id")
        print("user id from jwt", user_identity)

        user = User.query.get(user_identity)
        print("user from jwt: ", user)

        g.current_user = user

        return fn(*args, **kwargs)

    return wrapper


def superuser_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = g.get("current_user")

        if user is None:
            raise UnauthorizedAccessException("Unauthorized Access")
        for role in user.roles:
            if role.is_super:
                return fn(*args, **kwargs)
        else:
            raise UnauthorizedAccessException("Unauthorized Access")

    return wrapper


def permission_required(*permissions):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            user = g.get("current_user")
            if user is None:
                raise UnauthorizedAccessException("Unauthorized Access")

            # Check permissions
            for role in user.roles:
                # superuser has all permissions
                if role.is_super:
                    return fn(*args, **kwargs)

                # check permissions for other users
                for permission in role.permissions:
                    if permission.system_name in permissions:
                        return fn(*args, **kwargs)
            else:
                raise UnauthorizedAccessException("Unauthorized Access")

        return wrapped

    return wrapper
