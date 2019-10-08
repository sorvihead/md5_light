from app import db

from flask import current_app

import redis
import rq


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except redis.exceptions.RedisError:
            return None
        return rq_job

    def get_status(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job else 100
