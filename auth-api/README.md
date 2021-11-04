# Authentication Service

This service creates authentication tokens to valid users that have provided correct authentication details.

The tokens are valid for **30 seconds** and can be used to make requests to [`core-api`](../core-api).

## Dependencies

- Python 3.9

## Quickstart

Example:

```bash
$ python --version
Python 3.9.7
$ pip install -r requirements.txt
$ export HTTP_PORT=5000
$ export JWT_SECRET=secret
$ python main.py  
 * Serving Quart app 'main'
 * Environment: production
 * Please use an ASGI server (e.g. Hypercorn) directly in production
 * Debug mode: False
 * Running on http://0.0.0.0:5000 (CTRL + C to quit)
[2021-11-02 20:10:05,269] Running on http://0.0.0.0:5000 (CTRL + C to quit)
```

## Environment variables

| Environment variable | Description                                                                            |
| -------------------- | -------------------------------------------------------------------------------------- |
| `HTTP_PORT`            | **Required**. Port to bind HTTP server. Default: `5000`.                               |
| `JWT_SECRET`           | **Required**. [JSON Web Tokens](https://jwt.io/) secret. Must be the same as that of [`core-api`](). |

## User database

User credentials are stored in the [users.json](users.json) file.

Example user model:

```json
{
    "id": 1,
    "username": "alice",
    "password": "password",
    "enabled": true
}
```

`enabled` determines whether the user is allowed to make transactions with [`core-api`](../core-api).

User creation and management are out of the scope of this service.

## Endpoints

### `GET /health` - Health check

Health check to see if the service is up.

#### Request

```bash
$ http -v http://0.0.0.0:5000/health
```

```http
GET /health HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: 0.0.0.0:5000
User-Agent: HTTPie/2.6.0
```

#### Response

```http
HTTP/1.1 200 
content-length: 29
content-type: application/json
date: Tue, 02 Nov 2021 20:20:46 GMT
server: hypercorn-h11

{
    "checks": {},
    "status": "pass"
}

```


### `POST /token` - Create an authentication token

Create an authentication token for the given user. Tokens are valid for **30 seconds**.

#### Request

| Argument | Description                                  |
| -------- | -------------------------------------------- |
| username | **Required**. Username in the user database. |
| password | **Required**. Password for the user.         |

Usage:

```bash
$ http -v POST http://0.0.0.0:5000/token \
  username=alice \
  password=password
```

```http
POST /token HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 45
Content-Type: application/json
Host: 0.0.0.0:5000
User-Agent: HTTPie/2.6.0

{
    "password": "password",
    "username": "alice"
}
```

#### Response

```http
HTTP/1.1 200 
content-length: 179
content-type: application/json
date: Tue, 02 Nov 2021 20:26:03 GMT
server: hypercorn-h11

{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFsaWNlIiwiZW5hYmxlZCI6dHJ1ZSwiZXhwIjoxNjM1ODg0NzkzfQ.t4fLg-F8Ev3nwDED18OiQaqCOCzG7bgIO0s1AbFoRZo"
}

```
