import marshmallow as ma
from marshmallow import validates, ValidationError
from email_validator import validate_email, EmailNotValidError


class UserCreateSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    first_name = ma.fields.String(required=True)
    last_name = ma.fields.String(required=True)
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(dump_only=True)

    @validates("email")
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError("Please provide a valid email address")
        return value

    @validates("password")
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 8 characters long")
        elif len(value) > 30:
            raise ValidationError("Password must be less than 30 characters long")
        return value


class UserResponseSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    first_name = ma.fields.String()
    last_name = ma.fields.String()
    email = ma.fields.Email()
    created_at = ma.fields.DateTime(dump_only=True)


class UserLoginSchema(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True)

    @validates("email")
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError("Please provide a valid email address")
        return value

    @validates("password")
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 8 characters long")
        elif len(value) > 30:
            raise ValidationError("Password must be less than 30 characters long")
        return value
