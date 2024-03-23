import marshmallow as ma


class StoreSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    description = ma.fields.String()
    location = ma.fields.String()
    created_at = ma.fields.DateTime(dump_only=True)


class StoreTagSchema(StoreSchema):
    tags = ma.fields.List(ma.fields.Nested("TagSchema"), dump_only=True)


class StoreCreateSchema(StoreSchema):
    name = ma.fields.String(required=True)
    description = ma.fields.String(required=True)
    location = ma.fields.String(required=True)


class StoreQuerySchema(ma.Schema):
    name = ma.fields.String(required=False)
    location = ma.fields.String(required=False)
    page = ma.fields.Int(required=False)
    per_page = ma.fields.Int(required=False)
    sortField = ma.fields.String(required=False)
    sortDirection = ma.fields.String(required=False, default="asc")
