# platform-challenge

## Background

Gr4vy is a building a payment orchestration platform.

As a Platform engineer, you are tasked with improving the engineering efficiency by producing automation tools that provision services in an efficient, predictable and reproducible way.

In this exercise we use [HTTPie](https://github.com/httpie/httpie) in our examples for clarity.

## Architecture Overview

```
+----------------------------------+
|            Merchant              |
+-+--------^------------+--------^-+
  |        |            |        |
 (1)      (2)          (3)      (5)
  |        |            |        |
+-v--------+-+        +-v--------+-+        +-----------------+
|  Auth API  |        |  Core API  |        |  PSP Connector  | 
+------------+        +------+-----+        +---------^-------+
                             |                        |
                            (4)                      (6)
                             |                        |
                      +------v------------------------+-------+
                      |          Redis Message Queue          |
                      +---------------------------------------+
```

There are 3 distinct services:

- [Auth API] - Creates authentication tokens to valid users.
- [Core API] - Processes transaction requests.
- [PSP Connector] - Processes the transactions with a Payment Service Provider (PSP).

A transaction flow is as follows:

1. A merchant authenticates with the [Auth API] by providing a valid username and password.
2. An authentication token that is valid for 30 seconds is returned.
3. Use this authentication token to make a transaction request to the [Core API].
4. The [Core API] submits the transaction to a message queue for further background processing.
5. A successful response is returned.
6. Meanwhile, a [PSP Connector] processes the transaction from the message queue by connecting to a Payment Service Provider.

We use environment variables to configure a service.

## Your task

- Read the documentation for each service. Run and test them to make sure they work as expected.
- Once you're familiar with the services, use your preferred tools to automate provisioning of a **local development** environment.
- Be sure to include external dependencies like Redis and configuration management.
- In order for a microservices-based architecture to work best, implement a HTTP router in front of the services that routes requests to the correct service. A popular solution is path-based routing:
    - http://platform/auth/* → http://auth-api/*
    - http://platform/transaction/* → http://core-api/*
- Make your automation available on a public GitHub repository with a `README` on how to get things started.

Don't worry too much about making this production ready. We may discuss production considerations with you later on.

Please spend no more than 1-2 hours on this exercise.

## Bonus (Optional)

- Containerise services.
- Apply the [Twelve Factor App](https://12factor.net/) methodology.

[Auth API]: auth-api
[Core API]: core-api
[PSP Connector]: psp-connector