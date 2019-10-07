from app.secure_api import bp

from flask import jsonify
from flask import request


@bp.route('/submit', methods=['POST'])
def submit():
    url, email = request.values.get('url'), request.values.get('email')

    return jsonify(url, email)


@bp.route('/check')
def check():
    pass
