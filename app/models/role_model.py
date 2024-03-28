import enum
from app.extensions import db
from sqlalchemy import Enum
from sqlalchemy.exc import IntegrityError
from app.models.association_models import role_permission_table, user_role_table


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    is_super = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(255), default="user")
    permissions = db.relationship(
        "Permission",
        secondary=role_permission_table,
        back_populates="roles",
        cascade="all, delete",
    )
    users = db.relationship(
        "User",
        secondary=user_role_table,
        back_populates="roles",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __str__(self):
        return self.name

    @classmethod
    def create_role(cls, name=None, is_super=False, is_admin=False):
        new_role = cls(name=name, is_super=is_super, is_admin=is_admin)
        db.session.add(new_role)
        try:
            db.session.commit()
            return new_role
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Role already exists")
