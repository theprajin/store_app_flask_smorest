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
    migrate.init_app(app, db)

    from app.routes.store_routes import store_blp
    from app.routes.item_routes import item_blp

    api = Api(app)
    api.register_blueprint(store_blp)
    api.register_blueprint(item_blp)

    return app
