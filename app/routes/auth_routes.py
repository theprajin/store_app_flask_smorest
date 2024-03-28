from flask import jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from app.models.user_model import User
from app.models.role_model import Role
from app.schemas.user_schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserLoginSchema,
)
from app.services.token_user import create_token_user

from app.app import URL_PREFIX
from app.extensions import db

from app.services.decorators import load_user_from_request


auth_blp = Blueprint(
    "auth", __name__, url_prefix=f"{URL_PREFIX}/auth", description="Operations on auth"
)


@auth_blp.route("/register")
class Register(MethodView):

    @auth_blp.arguments(UserCreateSchema)
    @auth_blp.response(200, UserResponseSchema)
    def post(self, new_data):
        """Register User"""
        # prit(register)
        try:
            first_name = new_data.get("first_name")
            last_name = new_data.get("last_name")
            email = new_data.get("email")
            password = new_data.get("password")

            # Total number of users in the User table
            total_user = db.session.query(User).count()

            # Create a superadmin only if there are no users
            if total_user <= 0:
                role = Role.query.filter_by(is_super=True).first()
                if role is None:
                    role = Role.create_role(is_super=True, is_admin=True, name="super")

                user = User.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )

                user.roles.append(role)
                db.session.commit()
                g.current_user = user
                return

            # create a new user
            user = User.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            db.session.commit()

            return jsonify({"message": "user registration successful"}), 201
        except ValueError:
            return jsonify({"error": "User with this email already exists"}), 400


@auth_blp.route("/login")
class Login(MethodView):
    @auth_blp.arguments(UserLoginSchema)
    @auth_blp.response(200, UserResponseSchema)
    @jwt_required(optional=True)
    def post(self, new_data):
        """Login User"""
        try:
            email = new_data.get("email")
            password = new_data.get("password")

            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                return jsonify({"error": "Incorrect email or password"}), 401

            access_token = create_access_token(identity=create_token_user(user))
            refresh_token = create_refresh_token(identity=create_token_user(user))

            return jsonify(access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            print(e)


@auth_blp.route("/refresh")
class AccessTokenWithRefreshToken(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        """Create New Access Token With Refresh Token"""
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}, 200


# @auth_blp.route("/logout")
# class Logout(MethodView):
#     pass
