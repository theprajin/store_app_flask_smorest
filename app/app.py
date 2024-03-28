from flask import Flask, g, jsonify
from flask.views import MethodView


from flask_smorest import Api
from flask_jwt_extended import jwt_required, get_jwt_identity


from app import configuration
from app.extensions import db, migrate, jwt, cors
from app.models.user_model import User
from app.services.exceptions import UnauthorizedAccessException

from app.services.unauthorized_error import custom_unauthorized_response


URL_PREFIX = "/api/v1"


def create_app():
    app = Flask(__name__)

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

    @app.before_request
    @jwt_required(optional=True)
    def load_user_into_g():
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = user_identity.get("id")
            if user_id:
                user = User.query.get(user_id)
                g.current_user = user
            else:
                g.current_user = None

    @app.errorhandler(UnauthorizedAccessException)
    def handle_unauthorized_access(error):
        """Handle UnauthorizedAccessException exceptions globally."""
        return jsonify({"error": "Unauthorized Access"}), 403

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
