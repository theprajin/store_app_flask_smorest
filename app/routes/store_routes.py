from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models.store_model import Store
from app.schemas.store_schemas import (
    StoreSchema,
    StoreCreateSchema,
    StoreResponseSchema,
    StoreTagSchema,
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
    @store_blp.response(200, StoreSchema(many=True))
    def get(self):
        """Get Store List"""
        try:
            stores = Store.query.all()
            return stores
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
