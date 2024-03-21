from app.app import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    location = db.Column(db.String(120))
    items = db.relationship("Item", cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
