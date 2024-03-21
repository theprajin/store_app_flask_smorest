import marshmallow as ma
from app.schemas.store_schemas import StoreSchema


class ItemSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    description = ma.fields.String()
    unit_price = ma.fields.Float()
    store_id = ma.fields.Int(load_only=True)
    store = ma.fields.Nested(StoreSchema, only=("id",), dump_only=True)
    created_at = ma.fields.DateTime(dump_only=True)


class ItemCreateSchema(ItemSchema):
    name = ma.fields.String(required=True)
    description = ma.fields.String(required=True)
    unit_price = ma.fields.Float(required=True)
    store_id = ma.fields.Int(required=True)
