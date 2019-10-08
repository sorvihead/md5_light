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
    return jsonify(task.id)


@bp.route('/check')
def check():
    task_id = request.args.get('id', '')
    if not task_id:
        return jsonify({"errors": "task_id expected"}), 400
    task = Task.query.get(task_id)
    if not task:
        return jsonify("task is not found"), 404
    status = task.get_status()
    data = {"status": status}
    if status == "complete":
        data.update({"md5": task.md5})
    return jsonify(data), 200
