import marshmallow as ma
from app.schemas.user_schemas import UserCreateSchema, UserResponseSchema
from app.schemas.role_schemas import RoleSchema


class UserRoleSchema(UserResponseSchema):

    roles = ma.fields.List(ma.fields.Nested("RoleSchema"), dump_only=True)


class RoleResponseSchema(RoleSchema):
    users = ma.fields.Nested(
        UserRoleSchema, only=("id",), many=True, exclude=("role",), required=False
    )
