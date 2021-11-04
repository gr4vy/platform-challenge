# PSP Connector

This service is a worker that processes transactions from a message queue.

For this exercise, this service is a work-in-progress and only prints transaction to the console.

## Dependencies

- Python 3.9
- Redis

## Quickstart

Example:

```bash
$ python --version
Python 3.9.7
$ redis-cli ping
PONG
$ pip install -r requirements.txt
$ export HTTP_PORT=5000
$ export REDIS_URL=redis://127.0.0.1:6379/0
$ python main.py
11:56:46 Worker rq:worker:106c1fbd480049988536d2f88c7a9904: started, version 1.10.0
11:56:46 Subscribing to channel rq:pubsub:106c1fbd480049988536d2f88c7a9904
11:56:46 *** Listening on default...
```

## Environment variables

| Environment variable | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `REDIS_URL`            | **Required**. Redis URL. Default: `redis://127.0.0.1:6379/0` |


## Example Output

```
11:57:11 default: __main__.make_transaction(amount=100, currency='USD', user_id=1) (089f53a1-de72-4c55-b8c0-7a3108987118)
==> Making transaction with PSP: User ID: 1, Amount: 100, Currency: USD
11:57:11 default: Job OK (089f53a1-de72-4c55-b8c0-7a3108987118)
11:57:11 Result is kept for 500 seconds
```
