import marshmallow as ma

from app.schemas.role_schemas import RoleSchema


class RolePermissionSchema(RoleSchema):
    permissions = ma.fields.List(ma.fields.Nested("PermissionSchema"), dump_only=True)


class PermissionResponseSchema:
    pass
