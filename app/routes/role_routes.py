from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort


from app.app import URL_PREFIX
from app.models.role_model import Role
from app.schemas.role_schemas import RoleSchema
from app.extensions import db
from app.services.decorators import superuser_required, load_user_from_request


role_blp = Blueprint(
    "roles",
    __name__,
    url_prefix=f"{URL_PREFIX}/roles",
    description="Operations on roles",
)


@role_blp.route("/")
class Roles(MethodView):
    @role_blp.response(200, RoleSchema(many=True))
    @superuser_required
    @load_user_from_request
    def get(self):
        """Get Role List"""
        return Role.query.all()

    @role_blp.arguments(RoleSchema)
    @role_blp.response(201, RoleSchema)
    @superuser_required
    @load_user_from_request
    def post(self, new_data):
        """Create Role"""
        try:

            role = Role(**new_data)
            db.session.add(role)
            db.session.commit()

            return role

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 401


@role_blp.route("/<int:role_id>")
class RoleById(MethodView):

    @role_blp.response(200, RoleSchema)
    @superuser_required
    @load_user_from_request
    def get(self, role_id):
        """Get Role"""
        try:
            role = Role.query.get(role_id)

            if role is None:
                return jsonify({"message": f"Role with id: {role_id} not found"}), 404

            return role
        except Exception as e:
            print(e)

    @role_blp.arguments(RoleSchema)
    @role_blp.response(200, RoleSchema)
    @superuser_required
    @load_user_from_request
    def patch(self, new_data, role_id):
        """Update Role"""
        try:

            role = Role.query.get(role_id)

            if role is None:
                return jsonify({"message": f"Role with id: {role_id} not found"}), 404

            role.name = new_data.get("name") or role.name
            role.is_super = new_data.get("is_super") or role.is_super
            role.is_admin = new_data.get("is_admin") or role.is_admin
            db.session.commit()

            return role

        except Exception as e:
            print(e)

    @role_blp.arguments(RoleSchema)
    @role_blp.response(204)
    @superuser_required
    @load_user_from_request
    def delete(self, role_id):
        """Delete Role"""
        role = Role.query.get(role_id)
        if role is None:
            return jsonify({"message": f"Role with id: {role_id} not found"}), 404
        db.session.delete(role)
        db.session.commit()
