#!/usr/bin/env python
import healthpy
import os
import re

from jose import jwt
from flask import Flask, jsonify, current_app, request
from flask_rq2 import RQ

app = Flask(__name__)
rq = RQ(app)


@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    token: str = data.get('token')
    amount: int = int(data.get('amount'))
    currency: str = data.get('currency')

    if not token:
        return jsonify(error='Token is blank'), 422
    if not amount:
        return jsonify(error='Amount is blank'), 422
    if not currency:
        return jsonify(error='Currency is blank'), 422
    if not re.match(r'^[A-Z]{3}$', currency):
        return jsonify(error='Invalid currency code'), 422

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except jwt.JWTError as exc:
        return jsonify(error=str(exc)), 422
    else:
        if payload['enabled']:
            rq.get_queue().enqueue(
                '__main__.make_transaction',
                user_id=payload['user_id'],
                amount=amount,
                currency=currency,
            )
            return jsonify(
                user_id=payload['user_id'],
                amount=amount,
                currency=currency,
            )
        else:
            return jsonify(error='User not enabled for transactions'), 403


@app.route('/health')
def health():
    status = healthpy.pass_status  # replace with the aggregated status
    checks = {}  # replace with the computed checks
    return healthpy.response_body(status, checks=checks)


if __name__ == '__main__':
    # Environment variables
    redis_url: str = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
    http_port: int = int(os.getenv('HTTP_PORT', 5000))
    jwt_secret: str = os.environ['JWT_SECRET']

    # Flask config
    app.config['RQ_DEFAULT_URL'] = redis_url
    app.config['JWT_SECRET'] = jwt_secret

    # Run app
    app.run(host='0.0.0.0', port=http_port, threaded=True)
    