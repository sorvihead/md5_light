from app import create_app
from app import db

from app.models import Task

from rq import get_current_job

app = create_app()
app.app_context().push()


def _set_task_status(status):
    job = get_current_job()
    if job:
        job.meta['status'] = status
        job.save_meta()
        task = Task.query.get(job.get_id())
        if status == 'complete':
            task.complete = True
        db.session.commit()
