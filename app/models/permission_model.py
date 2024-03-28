import enum
from app.extensions import db
from sqlalchemy import Enum
from app.models.association_models import role_permission_table


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    roles = db.relationship(
        "Role",
        secondary=role_permission_table,
        back_populates="permissions",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __str__(self):
        return self.name
