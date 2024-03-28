from flask.views import MethodView
from flask_smorest import Blueprint, abort


from app.app import URL_PREFIX


user_blp = Blueprint(
    "users",
    __name__,
    url_prefix=f"{URL_PREFIX}/users",
    description="Operations on users",
)


@user_blp.route("/")
class Users(MethodView):
    pass
