import marshmallow as ma


class PermissionSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    system_name = ma.fields.String(required=True)
    display_name = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
