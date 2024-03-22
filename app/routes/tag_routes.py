from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models.tag_model import Tag
from app.app import URL_PREFIX, db
from app.models.tag_model import Tag
from app.schemas.tag_schemas import TagSchema

tag_blp = Blueprint(
    "tags", __name__, url_prefix=f"{URL_PREFIX}/tags", description="Operations on tags"
)


@tag_blp.route("/")
class Tags(MethodView):

    @tag_blp.response(200, TagSchema(many=True))
    def get(self):
        """List Tags"""

        try:
            tags = Tag.query.all()
            return tags
        except Exception as e:
            print(e)

    @tag_blp.arguments(TagSchema)
    @tag_blp.response(201, TagSchema)
    def post(self, new_data):
        """Create a new Tag"""

        try:
            tag = Tag(**new_data)
            db.session.add(tag)
            db.session.commit()

            return tag
        except Exception as e:
            print(e)


@tag_blp.route("/<int:tag_id>")
class TagById(MethodView):

    @tag_blp.response(200, TagSchema)
    def get(self, tag_id):
        """Get Tag by ID"""

        try:
            tag = Tag.query.get(tag_id)
            if not tag:
                abort(404, message="Tag not found.")

            return tag
        except Exception as e:
            print(e)

    @tag_blp.arguments(TagSchema)
    @tag_blp.response(200, TagSchema)
    def put(self, update_data, tag_id):
        """Update a Tag"""

        try:
            tag = Tag.query.get(tag_id)
            if not tag:
                abort(404, message="Tag not found.")
            for key, value in update_data.items():
                setattr(tag, key, value)
            db.session.commit()

            return tag
        except Exception as e:
            print(e)

    @tag_blp.response(204)
    def delete(self, tag_id):
        """Delete a Tag"""

        try:
            tag = Tag.query.get(tag_id)
            if not tag:
                abort(404, message="Tag not found.")
            db.session.delete(tag)
            db.session.commit()

            return tag
        except Exception as e:
            print(e)
