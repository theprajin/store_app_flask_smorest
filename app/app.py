from flask import Flask
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_migrate import Migrate

from app import configuration


URL_PREFIX = "/api/v1"

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(configuration.DevelopmentConfig)

    db.init_app(app)

    from app.models.association_models import store_tag_table, item_tag_table
    from app.models.store_model import Store
    from app.models.item_model import Item
    from app.models.tag_model import Tag

    migrate.init_app(app, db)

    from app.routes.store_routes import store_blp
    from app.routes.item_routes import item_blp
    from app.routes.tag_routes import tag_blp

    api = Api(app)
    api.register_blueprint(store_blp)
    api.register_blueprint(item_blp)
    api.register_blueprint(tag_blp)

    return app
