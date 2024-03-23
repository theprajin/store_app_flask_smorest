from app.app import db
from app.models.association_models import store_tag_table, item_tag_table


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    stores = db.relationship(
        "Store",
        secondary=store_tag_table,
        back_populates="tags",
        cascade="all, delete",
    )
    items = db.relationship(
        "Item",
        secondary=item_tag_table,
        back_populates="tags",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
