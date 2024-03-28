from flask import jsonify
from app.extensions import jwt
from app.services.exceptions import UnauthorizedAccessException


@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return (
        jsonify(
            {
                "message": "Missing or invalid token. Please log in or provide a valid token.",
            }
        ),
        401,
    )
