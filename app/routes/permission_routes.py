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
from app.services.decorators import user_is_super, load_user_from_request
from app.models.user_model import User
from app.extensions import db, app


perm_blp = Blueprint(
    "permissions",
    __name__,
    url_prefix=f"{URL_PREFIX}/permissions",
    description="Operations on permissions",
)


@perm_blp.route("/")
class Permissions(MethodView):

    @perm_blp.response(200, PermissionSchema(many=True))
    def get(self):
        """Get Permission List"""
        return Permission.query.all()

    @perm_blp.arguments(PermissionSchema)
    @perm_blp.response(201, PermissionSchema)
    @jwt_required()
    def post(self, new_data):
        """Create Permission"""
        try:
            user_id = get_jwt_identity().get("id")
            user = User.query.filter_by(id=user_id).first()

            @user_is_super(user)
            def create_permission():
                permission = Permission(**new_data)
                db.session.add(permission)
                db.session.commit()

                return permission

            permission = create_permission()
            return permission

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 401


class PermissionById(MethodView):

    @perm_blp.response(200, PermissionSchema)
    @jwt_required()
    def get(self, permission_id):
        """Get Permission"""
        return Permission.query.get_or_404(permission_id)

    @perm_blp.arguments(PermissionSchema)
    @perm_blp.response(200, PermissionSchema)
    @jwt_required()
    def patch(self, new_data, permission_id):
        """Update Permission"""
        permission = Permission.query.get_or_404(permission_id)
        permission.update_permission(**new_data)
        db.session.commit()
        return permission

    @perm_blp.response(204)
    @jwt_required()
    def delete(self, permission_id):
        """Delete Permission"""
        permission = Permission.query.get_or_404(permission_id)
        db.session.delete(permission)
        db.session.commit()
        return "", 204
