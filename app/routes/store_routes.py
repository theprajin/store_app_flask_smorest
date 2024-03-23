from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import desc

from app.models.store_model import Store
from app.schemas.store_schemas import (
    StoreSchema,
    StoreCreateSchema,
    StoreResponseSchema,
    StoreTagSchema,
    StoreQuerySchema,
)
from app.app import db, URL_PREFIX

store_blp = Blueprint(
    "stores",
    __name__,
    url_prefix=f"{URL_PREFIX}/stores",
    description="Operations on stores",
)


@store_blp.route("/")
class Stores(MethodView):

    @store_blp.arguments(StoreQuerySchema, location="query")
    @store_blp.response(200, StoreSchema(many=True))
    def get(self, queries):
        """Get Store List"""
        try:
            page = queries.pop("page", 1)
            per_page = queries.pop("per_page", 10)
            sortField = queries.pop("sortField", "")
            sortDirection = queries.pop("sortDirection", "asc")

            query = Store.query

            # Filetering queries
            if "name" in queries:
                query = query.filter(Store.location.ilike(f"%{queries['name']}%"))

            if "location" in queries:
                query = query.filter(Store.location.ilike(f"%{queries['location']}%"))

            # sorting queries
            if sortField == "name":
                if sortDirection == "desc":
                    query = query.desc(Store.name)
                else:
                    query = query.order_by(Store.name)

            if sortField == "location":
                if sortDirection == "desc":
                    query = query.order_by(desc(Store.location))
                else:
                    query = query.order_by(Store.location)

            stores = query.paginate(per_page=per_page, page=page, error_out=False)

            if not stores.items and page != 1:
                abort(404, message="Page not found")

            return stores.items
        except Exception as e:
            print(e)

    @store_blp.arguments(StoreCreateSchema)
    @store_blp.response(201, StoreSchema)
    def post(self, new_data):
        """Create Store"""
        try:
            name = new_data.get("name")
            store = Store.query.filter_by(name=name).first()

            if store:
                return jsonify({"message": "Store already exists"}), 400
            else:
                store = Store(**new_data)
                db.session.add(store)
                db.session.commit()
                return store
        except Exception as e:
            print(e)


@store_blp.route("/<int:store_id>")
class StoreByID(MethodView):

    @store_blp.response(200, StoreTagSchema)
    def get(self, store_id):
        """Get Store By ID"""
        try:
            store = Store.query.get(store_id)
            print(store)

            if store is None:
                return jsonify({"message": f"Store with id: {store_id} not found"}), 404

            return store
        except Exception as e:
            print(e)

    @store_blp.arguments(StoreSchema)
    @store_blp.response(200, StoreSchema)
    def patch(self, new_data, store_id):
        """Update Store By ID"""
        try:
            store = Store.query.get(store_id)

            if store is None:
                return jsonify({"message": f"Store with id: {store_id} not found"}), 404

            store.name = new_data.get("name") or store.name
            store.description = new_data.get("description") or store.description
            store.location = new_data.get("location") or store.location
            db.session.commit()

            return store
        except Exception as e:
            print(e)

    @store_blp.response(204, StoreSchema)
    def delete(self, store_id):
        """Delete Store By ID"""
        try:
            store = Store.query.get(store_id)

            if store is None:
                return jsonify({"message": f"Store with id: {store_id} not found"}), 404

            db.session.delete(store)
            db.session.commit()

            return store
        except Exception as e:
            print(e)
