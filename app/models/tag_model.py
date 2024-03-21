from app.app import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
