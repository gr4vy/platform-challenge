#!/usr/bin/env python
import datetime
import healthpy
import json
import os
import sys

from jose import jwt
from quart import Quart, request, current_app, jsonify

app = Quart(__name__)


# In-memory user database
with open(os.path.join(os.path.dirname(__file__), 'users.json'), 'rb') as f:
    users = json.load(f)


@app.route("/token", methods=["POST"])
async def create_token():
    """
    Authenticates a user by username and password, returning an authentication token (valid for 30s)
    that can be used to make authenticated requests to other services.
    """
    data = await request.get_json()
    username: str = data.get('username')
    password: str = data.get('password')

    if not username:
        return jsonify(error='Username is blank'), 422
    if not password:
        return jsonify(error='Password is blank'), 422

    for user in users:
        # Find user by username
        if user['username'] == username:
            # Validate password
            if user['password'] == password:
                payload = {
                    "user_id": user['id'],
                    "username": user['username'],
                    "enabled": user['enabled'],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),  # jwt expiration time claim
                }

                token = jwt.encode(
                    payload,
                    current_app.config['JWT_SECRET'],
                    algorithm='HS256',
                )

                return jsonify(token=token)
            else:
                return jsonify(error='Invalid password'), 401
    else:
        return jsonify(error='User not found'), 404


@app.route('/health')
async def health():
    status = healthpy.pass_status  # replace with the aggregated status
    checks = {}  # replace with the computed checks
    return healthpy.response_body(status, checks=checks)


if __name__ == '__main__':
    # Environment variables
    try:  
        jwt_secret: str = os.environ['JWT_SECRET']
    except KeyError: 
        print('[error]: `JWT_SECRET` environment variable required')
        sys.exit(1)
    
    http_port: int = int(os.getenv('HTTP_PORT', 5000))

    # Quart config
    app.config['JWT_SECRET'] = jwt_secret

    # Run app
    app.run(host='0.0.0.0', port=http_port)
