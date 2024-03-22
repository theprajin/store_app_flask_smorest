import marshmallow as ma
from app.schemas.store_schemas import StoreSchema
from app.schemas.item_schemas import ItemSchema


class TagSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    created_at = ma.fields.DateTime(dump_only=True)


class TagStoreSchema(TagSchema):
    stores = ma.fields.Nested(
        StoreSchema, only=("id",), dump_only=True, exclude=("tags",)
    )


class TagItemSchema(TagSchema):
    item = ma.fields.Nested(ItemSchema, only=("id",), dump_only=True, exclude=("tags",))
