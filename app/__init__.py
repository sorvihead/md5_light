from config import Config

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from redis import Redis

import rq

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('tc-tasks', connection=app.redis)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.secure_api import bp as secure
    app.register_blueprint(secure)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.errors.errors import (not_found_error, internal_server_error, method_not_allowed,
                                   bad_request)
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(405, method_not_allowed)

    return app
