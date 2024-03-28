from app.models.user_model import User


def create_token_user(user: User):

    return {
        "id": user.id,
        "email": user.email,
    }
