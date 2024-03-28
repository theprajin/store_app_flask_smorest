from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.item_model import Item
from app.models.store_model import Store
from app.schemas.item_schemas import (
    ItemSchema,
    ItemCreateSchema,
    ItemQuerySchema,
    ItemTagSchema,
    ItemCreateResponseSchema,
)
from app.app import URL_PREFIX
from app.extensions import db

from app.services.decorators import load_user_from_request, user_is_super

item_blp = Blueprint(
    "items",
    __name__,
    url_prefix=f"{URL_PREFIX}/items",
    description="Operations on items",
)


@item_blp.route("/")
class Items(MethodView):

    @item_blp.arguments(ItemQuerySchema, location="query")
    @item_blp.response(200, ItemSchema(many=True))
    def get(self, queries):
        """Get Item List"""
        try:
            page = queries.pop("page", 1)
            per_page = queries.pop("per_page", 10)
            sortField = queries.pop("sortField", "")
            sortDirection = queries.pop("sortDirection", "asc")

            query = Item.query

            if "name" in queries:
                query = query.filter(Item.name.ilike(f"%{queries['name']}%"))

            if "price" in queries:
                query = query.filter(Item.unit_price == float(queries["price"]))

            if sortField == "name":
                if sortDirection == "desc":
                    query = query.desc(Item.name)
                else:
                    query = query.order_by(Item.name)

            if sortField == "price":
                if sortDirection == "desc":
                    query = query.order_by(desc(Item.unit_price))
                else:
                    query = query.order_by(Item.unit_price)

            items = query.paginate(per_page=per_page, page=page, error_out=False)

            if not items.items and page != 1:
                abort(404, message="Page not found")

            return items.items
        except Exception as e:
            print(e)

    @item_blp.arguments(ItemCreateSchema)
    @item_blp.response(201, ItemCreateResponseSchema)
    @user_is_super
    @load_user_from_request
    def post(self, new_data):
        """Create Item"""
        try:

            name = new_data.get("name")

            store_id = new_data.get("store_id")

            # check if store exists
            store = Store.query.get(store_id)
            if store is None:
                return (
                    jsonify({"message": f"Store with id: {store_id} not found"}),
                    404,
                )

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

    @item_blp.response(200, ItemTagSchema)
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
    @user_is_super
    @load_user_from_request
    def patch(self, new_data, item_id):
        """Update Item By ID"""
        try:

            item: Item = Item.query.get(item_id)

            if item is None:
                return (
                    jsonify({"message": f"Item with id: {item_id} not found"}),
                    404,
                )

            item.name = new_data.get("name") or item.name
            item.description = new_data.get("description") or item.description
            item.unit_price = new_data.get("unit_price") or item.unit_price
            item.store_id = new_data.get("store_id") or item.store_id
            db.session.commit()

            return item

        except Exception as e:
            print(e)

    @item_blp.response(204, ItemSchema)
    @user_is_super
    @load_user_from_request
    def delete(self, item_id):
        """Delete Item By ID"""
        try:

            item = Item.query.get(item_id)

            if item is None:
                return (
                    jsonify({"message": f"Item with id: {item_id} not found"}),
                    404,
                )

            db.session.delete(item)
            db.session.commit()

            return item

        except Exception as e:
            print(e)
