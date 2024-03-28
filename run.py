from app.app import db, create_app
from app.services import decorators


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
