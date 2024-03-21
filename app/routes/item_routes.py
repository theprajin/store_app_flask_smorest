from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models.item_model import Item
from app.models.store_model import Store
from app.schemas.item_schemas import ItemSchema, ItemCreateSchema
from app.app import db, URL_PREFIX

item_blp = Blueprint(
    "items",
    "items",
    url_prefix=f"{URL_PREFIX}/items",
    description="Operations on items",
)


@item_blp.route("/")
class Items(MethodView):
    @item_blp.response(200, ItemSchema(many=True))
    def get(self):
        """Get Item List"""
        try:
            items = Item.query.all()
            return items
        except Exception as e:
            print(e)
            return jsonify({"message": "Something went wrong"}), 400

    @item_blp.arguments(ItemCreateSchema)
    @item_blp.response(201, ItemSchema)
    def post(self, new_data):
        """Create Item"""
        try:
            name = new_data.get("name")
            store_id = new_data.get("store_id")

            # check if store exists
            store = Store.query.get(store_id)
            if store is None:
                return jsonify({"message": f"Store with id: {store_id} not found"}), 404

            # check for duplicate name of item
            item = Item.query.filter_by(name=name).first()

            if item:
                return jsonify({"message": "Item already exists"}), 400

            else:
                item = Item(**new_data)
                db.session.add(item)
                db.session.commit()
            return item
        except Exception as e:
            print(e)


@item_blp.route("/<int:item_id>")
class ItemByID(MethodView):

    @item_blp.response(200, ItemSchema)
    def get(self, item_id):
        """Get Item By ID"""
        try:
            item = Item.query.get(item_id)

            if item is None:
                return jsonify({"message": f"Item with id: {item_id} not found"}), 404
            return item
        except Exception as e:
            print(e)

    @item_blp.arguments(ItemSchema)
    @item_blp.response(200, ItemSchema)
    def patch(self, new_data, item_id):
        """Update Item By ID"""
        try:
            item: Item = Item.query.get(item_id)

            if item is None:
                return jsonify({"message": f"Item with id: {item_id} not found"}), 404

            item.name = new_data.get("name") or item.name
            item.description = new_data.get("description") or item.description
            item.unit_price = new_data.get("unit_price") or item.unit_price
            item.store_id = new_data.get("store_id") or item.store_id
            db.session.commit()
            return item
        except Exception as e:
            print(e)

    @item_blp.response(204, ItemSchema)
    def delete(self, item_id):
        """Delete Item By ID"""
        try:
            item = Item.query.get(item_id)

            if item is None:
                return jsonify({"message": f"Item with id: {item_id} not found"}), 404

            db.session.delete(item)
            db.session.commit()
            return item
        except Exception as e:
            print(e)
