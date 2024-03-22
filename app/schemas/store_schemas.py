import marshmallow as ma


class StoreSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    description = ma.fields.String()
    location = ma.fields.String()
    tags = ma.fields.List(ma.fields.Nested("TagSchema"))
    created_at = ma.fields.DateTime(dump_only=True)


class StoreCreateSchema(StoreSchema):
    name = ma.fields.String(required=True)
    description = ma.fields.String(required=True)
    location = ma.fields.String(required=True)


class StoreResponseSchema(StoreSchema):
    items = ma.fields.Nested(
        "ItemSchema", only=("id", "name", "unit_price"), many=True, exclude=("store",)
    )
