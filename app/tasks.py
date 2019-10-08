from app import create_app
from app import db

from app.email import send_email
from app.models import Task

from flask import render_template

from rq import get_current_job

import json
import hashlib
import requests
import sys

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


def _set_task_results(md5):
    job = get_current_job()
    if job:
        task = Task.query.get(job.get_id())
        task.md5 = md5
        db.session.commit()


def md5_file(url, email=None):
    try:
        _set_task_status('running')
        data = []
        r = requests.get(url)
        md5 = hashlib.md5(r.content).hexdigest()
        data.append({'url': url, 'md5': md5})
        _set_task_results(md5)
        _set_task_status('complete')
        if email:
            send_email('MD5 of your file',
                       sender=app.config['ADMINS'][0], recipients=[email],
                       text_body=render_template('email/md5_mail.txt'),
                       html_body=render_template('email/md5_mail.html'),
                       attachments=[('results.json', 'application/json',
                                     json.dumps(data, indent=4))],
                       sync=True)
    except:
        _set_task_status('fail')
