from app.app import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)
    store = db.relationship("Store", back_populates="items")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
