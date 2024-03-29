import marshmallow as ma


class RoleSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String(default="user")
    is_super = ma.fields.Boolean(default=False)
    is_admin = ma.fields.Boolean(default=False)
    created_at = ma.fields.DateTime(dump_only=True)
