from app import db

from flask import current_app

import redis
import rq


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128))
    md5 = db.Column(db.String(128))
    complete = db.Column(db.Boolean, default=False)

    @staticmethod
    def launch_task(name, url, email=None):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, url, email)
        task = Task(id=rq_job.get_id(), url=url, email=email)
        db.session.add(task)

        return task

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except redis.exceptions.RedisError:
            return None
        return rq_job

    def get_status(self):
        job = self.get_rq_job()
        return job.meta.get('status', 0) if job else 'not exist'
