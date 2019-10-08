from config import Config

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from redis import Redis

import rq

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('tc-tasks', connection=app.redis)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.secure_api import bp as secure
    app.register_blueprint(secure)

    return app
