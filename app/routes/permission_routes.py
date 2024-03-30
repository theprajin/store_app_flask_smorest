from flask import g, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from app.app import URL_PREFIX
from app.models.permission_model import Permission
from app.schemas.permission_schemas import PermissionSchema
from app.services.decorators import superuser_required, load_user_from_request

from app.models.user_model import User
from app.extensions import db


perm_blp = Blueprint(
    "permissions",
    __name__,
    url_prefix=f"{URL_PREFIX}/permissions",
    description="Operations on permissions",
)


@perm_blp.route("/")
class Permissions(MethodView):

    @perm_blp.response(200, PermissionSchema(many=True))
    @superuser_required
    @load_user_from_request
    def get(self):
        """Get Permission List"""
        return Permission.query.all()

    @perm_blp.arguments(PermissionSchema)
    @perm_blp.response(201, PermissionSchema)
    @superuser_required
    @load_user_from_request
    def post(self, new_data):
        """Create Permission"""
        try:

            permission = Permission(**new_data)
            db.session.add(permission)
            db.session.commit()

            return permission

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 401


@perm_blp.route("/<int:permission_id>")
class PermissionById(MethodView):

    @perm_blp.response(200, PermissionSchema)
    @superuser_required
    @load_user_from_request
    def get(self, permission_id):
        """Get Permission"""
        try:
            permission = Permission.query.get(permission_id)
            return permission
        except Exception as e:
            print(e)

    @perm_blp.arguments(PermissionSchema)
    @perm_blp.response(200, PermissionSchema)
    @superuser_required
    @load_user_from_request
    def patch(self, new_data, permission_id):
        """Update Permission"""
        try:

            permission = Permission.query.get(permission_id)

            if permission is None:
                return (
                    jsonify(
                        {"message": f"Permission with id: {permission_id} not found"}
                    ),
                    404,
                )

            permission.system_name = new_data.get("name") or permission.system_name
            permission.display_name = (
                new_data.get("display_name") or permission.display_name
            )
            db.session.commit()

            return permission
        except Exception as e:
            print(e)

    @perm_blp.response(204)
    @superuser_required
    @load_user_from_request
    def delete(self, permission_id):
        """Delete Permission"""
        permission = Permission.query.get_or_404(permission_id)
        db.session.delete(permission)
        db.session.commit()
        return "", 204
