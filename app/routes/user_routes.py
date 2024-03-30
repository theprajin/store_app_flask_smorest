from flask import jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.models.user_model import User
from app.models.role_model import Role
from app.schemas.user_schemas import UserResponseSchema
from app.schemas.user_role_schemas import UserRoleSchema

from app.services.decorators import load_user_from_request, superuser_required

from app.app import URL_PREFIX
from app.extensions import db


user_blp = Blueprint(
    "users",
    __name__,
    url_prefix=f"{URL_PREFIX}/users",
    description="Operations on users",
)


@user_blp.route("/")
class Users(MethodView):

    @user_blp.response(200, UserRoleSchema(many=True))
    @superuser_required
    def get(self):
        """Get User List"""
        return User.query.all()


@user_blp.route("/<int:user_id>")
class UserById(MethodView):

    @user_blp.response(200, UserRoleSchema)
    @superuser_required
    @load_user_from_request
    def get(self, user_id):
        """Get User"""
        try:
            user = User.query.get(user_id)

            if user is None:
                return jsonify({"message": f"User with id: {user_id} not found"}), 404

            return user
        except Exception as e:
            print(e)


@user_blp.route("/me")
class UserProfile(MethodView):

    @user_blp.response(200, UserResponseSchema)
    @load_user_from_request
    def get(self):
        """Get Own User Profile"""

        try:
            user = g.current_user

            return user
        except Exception as e:
            print(e)


@user_blp.route("/<int:user_id>/roles/<int:role_id>")
class UserRoles(MethodView):

    @user_blp.response(201, UserRoleSchema)
    @superuser_required
    @load_user_from_request
    def post(self, user_id, role_id):
        """Assign Role to User"""

        try:

            user = User.query.get(user_id)
            role = Role.query.get(role_id)

            if user is not None and role is not None:
                for user_role in user.roles:
                    if user_role.id == role.id:
                        return jsonify({"message": "Role already assigned"}), 400

                user.roles.append(role)
                db.session.commit()

                return user

            else:
                return jsonify({"message": f"User or Role does not exist"}), 404

        except Exception as e:
            print(e)

    @user_blp.response(204, UserRoleSchema)
    @superuser_required
    @load_user_from_request
    def delete(self, user_id, role_id):
        """Remove Role from User"""

        try:

            user = User.query.get(user_id)
            role = Role.query.get(role_id)

            if user is not None and role is not None:
                for user_role in user.roles:
                    if user_role.id == role.id:
                        user.roles.remove(role)
                        db.session.commit()

                        return user

                return jsonify({"message": "Role not found"}), 404

            else:
                return jsonify({"message": f"User or Role does not exist"}), 404

        except Exception as e:
            print(e)
