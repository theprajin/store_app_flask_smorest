from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort


from app.models.role_model import Role
from app.models.permission_model import Permission

from app.schemas.role_schemas import RoleSchema
from app.schemas.permission_schemas import PermissionSchema
from app.schemas.role_permission_schemas import RolePermissionSchema
from app.services.decorators import superuser_required, load_user_from_request
from app.extensions import db
from app.app import URL_PREFIX

role_perm_blp = Blueprint(
    "role_permissions",
    __name__,
    url_prefix=f"{URL_PREFIX}/role_permissions",
)


@role_perm_blp.route("/<int:role_id>/permissions/<int:permission_id>")
class RolePermission(MethodView):

    @role_perm_blp.response(201, RolePermissionSchema)
    @superuser_required
    @load_user_from_request
    def post(self, role_id, permission_id):
        """Assign Role to User"""

        try:

            role = Role.query.get(role_id)
            permission = Permission.query.get(permission_id)

            if role is not None and permission is not None:
                for role_perm in role.permissions:
                    if role_perm.id == permission.id:
                        return jsonify({"message": "Permission already assigned"}), 400

                role.permissions.append(permission)
                db.session.commit()

                return role

            else:
                return jsonify({"message": f"Role or Permission does not exist"}), 404

        except Exception as e:
            print(e)

    @role_perm_blp.response(204, RolePermissionSchema)
    @superuser_required
    @load_user_from_request
    def delete(self, role_id, permission_id):
        """Remove Role from User"""

        try:

            role = User.query.get(role_id)
            permission = Role.query.get(permission_id)

            if role is not None and permission is not None:
                for role_perm in role.permissions:
                    if role_perm.id == permission.id:
                        role.permissions.remove(permission)
                        db.session.commit()

                        return role

                return jsonify({"message": "Role not found"}), 404

            else:
                return jsonify({"message": f"User or Role does not exist"}), 404

        except Exception as e:
            print(e)
