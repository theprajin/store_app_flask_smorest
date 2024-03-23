import marshmallow as ma
from app.schemas.store_schemas import StoreSchema


class ItemSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    description = ma.fields.String()
    unit_price = ma.fields.Float()
    store_id = ma.fields.Int(load_only=True)
    store = ma.fields.Nested(StoreSchema, only=("id",), dump_only=True)
    tags = ma.fields.List(ma.fields.Nested("TagSchema"))
    created_at = ma.fields.DateTime(dump_only=True)


class ItemCreateResponseSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    description = ma.fields.String()
    unit_price = ma.fields.Float()
    store_id = ma.fields.Int(load_only=True)
    store = ma.fields.Nested(StoreSchema, only=("id",), dump_only=True)
    # tags = ma.fields.List(ma.fields.Nested("TagSchema"))
    created_at = ma.fields.DateTime(dump_only=True)


class ItemCreateSchema(ItemCreateResponseSchema):
    name = ma.fields.String(required=True)
    description = ma.fields.String(required=True)
    unit_price = ma.fields.Float(required=True)
    store_id = ma.fields.Int(required=True)


class ItemTagSchema(ItemSchema):
    tags = ma.fields.List(ma.fields.Nested("TagSchema"), dump_only=True)


class ItemQuerySchema(ma.Schema):
    name = ma.fields.String(required=False)
    unit_price = ma.fields.Float(required=False)
    page = ma.fields.Int(required=False)
    per_page = ma.fields.Int(required=False)
    sortField = ma.fields.String(required=False)
    sortDirection = ma.fields.String(required=False, default="asc")
