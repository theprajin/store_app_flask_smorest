from app.extensions import db

store_tag_table = db.Table(
    "store_tag",
    db.Column("store_id", db.Integer, db.ForeignKey("store.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


item_tag_table = db.Table(
    "item_tag",
    db.Column("item_id", db.Integer, db.ForeignKey("item.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

role_permission_table = db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)

user_role_table = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)
