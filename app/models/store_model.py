from app.app import db
from app.models.association_models import store_tag_table


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    location = db.Column(db.String(120))
    items = db.relationship("Item", cascade="all, delete-orphan")
    tags = db.relationship(
        "Tag",
        secondary=store_tag_table,
        back_populates="stores",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __str__(self):
        return self.name
