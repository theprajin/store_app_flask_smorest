from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from app.models.user_model import User, UserRole
from app.schemas.user_schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserLoginSchema,
)
from app.services.token_user import create_token_user

from app.app import URL_PREFIX, db


auth_blp = Blueprint(
    "auth", __name__, url_prefix=f"{URL_PREFIX}/auth", description="Operations on auth"
)


@auth_blp.route("/register")
class Register(MethodView):

    @auth_blp.arguments(UserCreateSchema)
    @auth_blp.response(200, UserResponseSchema)
    def post(self, new_data):
        """Register User"""
        try:
            first_name = new_data.get("first_name")
            last_name = new_data.get("last_name")
            email = new_data.get("email")
            password = new_data.get("password")
            role = new_data.get("role")

            total_user = db.session.query(User).count()

            role = UserRole.ADMIN if total_user <= 0 else UserRole.USER

            user = User.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                role=role,
            )

            return jsonify({"message": "user registration successful"}), 201
        except ValueError:
            return jsonify({"error": "User with this email already exists"}), 400


@auth_blp.route("/login")
class Login(MethodView):
    @auth_blp.arguments(UserLoginSchema)
    @auth_blp.response(200, UserResponseSchema)
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
