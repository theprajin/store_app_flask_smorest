import marshmallow as ma
from app.schemas.store_schemas import StoreSchema, StoreTagSchema
from app.schemas.item_schemas import ItemSchema


class TagSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    created_at = ma.fields.DateTime(dump_only=True)


class TagResponseSchema(TagSchema):
    stores = ma.fields.Nested(
        StoreTagSchema, only=("id",), many=True, exclude=("tags",), required=False
    )
    items = ma.fields.Nested(
        ItemSchema, only=("id",), many=True, exclude=("tags",), required=False
    )
