from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.app import URL_PREFIX, db
from app.models.tag_model import Tag
from app.models.store_model import Store
from app.models.item_model import Item
from app.schemas.tag_schemas import TagSchema, TagResponseSchema, TagCreateSchema


tag_blp = Blueprint(
    "tags", __name__, url_prefix=f"{URL_PREFIX}/", description="Operations on tags"
)


# Store Tag Routes


@tag_blp.route("/stores/<int:store_id>/tags")
class StoreTag(MethodView):
    @tag_blp.response(200, TagSchema)
    def get(self, store_id):
        """Get Store Tags"""
        pass

    @tag_blp.arguments(TagSchema)
    @tag_blp.response(200, TagResponseSchema)
    def post(self, new_data, store_id):
        """Create Store Tags"""
        try:
            store = Store.query.get(store_id)
            name = new_data.get("name")

            if store is None:
                return jsonify({"message": f"Store with id: {store_id} not found"}), 404

            tag = Tag(**new_data)
            print(tag.name)
            for i in store.tags:
                if i.name == tag.name:
                    return jsonify({"message": "Tag already exists"}), 400
            store.tags.append(tag)

            db.session.add(tag)
            db.session.commit()

            return tag
        except Exception as e:
            print(e)


@tag_blp.route("stores/<int:store_id>/tags/<int:tag_id>")
class StoreTagByID(MethodView):

    @tag_blp.response(200, TagResponseSchema)
    def delete(self, store_id, tag_id):
        """Remove Store Tags"""
        try:
            store = Store.query.get(store_id)
            if store is None:
                return jsonify({"message": f"Store with id: {store_id} not found"}), 404

            tag = Tag.query.get(tag_id)
            if tag is None:
                return jsonify({"message": f"Tag with id: {tag_id} not found"}), 404
            store.tags.remove(tag)

            db.session.commit()
            return tag
        except Exception as e:
            print(e)


# =====================================================================================================================


# Item Tag Routes
@tag_blp.route("/items/<int:item_id>/tags")
class ItemTag(MethodView):
    @tag_blp.response(200, TagSchema)
    def get(self, item_id):
        """Get Item Tags"""
        pass

    @tag_blp.arguments(TagSchema)
    @tag_blp.response(200, TagResponseSchema)
    def post(self, new_data, item_id):
        """Create Item Tags"""
        try:
            item = Item.query.get(item_id)
            name = new_data.get("name")

            if item is None:
                return jsonify({"message": f"Item with id: {item_id} not found"}), 404

            tag = Tag(**new_data)
            print(tag.name)
            for i in item.tags:
                if i.name == item.name:
                    return jsonify({"message": "Tag already exists"}), 400
            item.tags.append(tag)

            db.session.add(tag)
            db.session.commit()

            return tag
        except Exception as e:
            print(e)


@tag_blp.route("items/<int:item_id>/tags/<int:tag_id>")
class ItemTagByID(MethodView):

    @tag_blp.response(200, TagResponseSchema)
    def delete(self, item_id, tag_id):
        """Remove Item Tags"""
        try:
            item = Item.query.get(item_id)
            if item is None:
                return jsonify({"message": f"Store with id: {item_id} not found"}), 404

            tag = Tag.query.get(tag_id)
            if tag is None:
                return jsonify({"message": f"Tag with id: {tag_id} not found"}), 404

            item.tags.remove(tag)

            db.session.commit()
            return tag
        except Exception as e:
            print(e)
