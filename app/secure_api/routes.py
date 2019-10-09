from app import db

from app.secure_api import bp
from app.models import Task

from flask import jsonify
from flask import request


@bp.route('/submit', methods=['POST'])
def submit():
    url, email = request.values.get('url'), request.values.get('email')
    task = Task.launch_task('md5_file', url, email)
    db.session.commit()
    return jsonify(task.id), 202


@bp.route('/check')
def check():
    task_id = request.args.get('id', '')
    if not task_id:
        return jsonify({"errors": "task_id expected"}), 400
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"status": "not exist"}), 404
    status = task.get_status()
    data = {"status": status}
    status_code = 102
    if status == "complete":
        data.update({"md5": task.md5})
        data.update({"url": task.url})
        status_code = 200
    elif status == "fail":
        status_code = 502
    return jsonify(data), status_code
