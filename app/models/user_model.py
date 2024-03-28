from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.association_models import user_role_table


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    roles = db.relationship(
        "Role",
        secondary=user_role_table,
        back_populates="users",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)

    @classmethod
    def create_user(
        cls,
        first_name=None,
        last_name=None,
        email=None,
        password=None,
    ):
        new_user = cls(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
            db.session.refresh(new_user)
            return new_user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("User with this email already exists")

    def __str__(self):
        return self.first_name
