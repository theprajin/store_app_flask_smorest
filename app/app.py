from flask import Flask
from flask.views import MethodView

from flask_smorest import Api


from app import configuration
from app.extensions import app, db, migrate, jwt, cors

from app.services.unauthorized_error import custom_unauthorized_response


URL_PREFIX = "/api/v1"


def create_app():

    app.config.from_object(configuration.DevelopmentConfig)

    cors.init_app(app)

    db.init_app(app)

    from app.models.association_models import (
        store_tag_table,
        item_tag_table,
        role_permission_table,
        user_role_table,
    )
    from app.models.store_model import Store
    from app.models.item_model import Item
    from app.models.tag_model import Tag
    from app.models.role_model import Role
    from app.models.permission_model import Permission

    migrate.init_app(app, db)

    jwt.init_app(app)

    from app.routes.store_routes import store_blp
    from app.routes.item_routes import item_blp
    from app.routes.tag_routes import tag_blp
    from app.routes.auth_routes import auth_blp
    from app.routes.permission_routes import perm_blp

    api = Api(app)
    api.register_blueprint(auth_blp)
    api.register_blueprint(store_blp)
    api.register_blueprint(item_blp)
    api.register_blueprint(tag_blp)
    api.register_blueprint(perm_blp)

    return app
