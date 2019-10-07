from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.secure_api import bp as secure
    app.register_blueprint(secure)

    return app
