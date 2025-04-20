# Python PgDatabase-Pool Module

![push main](https://github.com/clauspruefer/python-dbpool/actions/workflows/pylint.yaml/badge.svg)
[![PyPI version](https://badge.fury.io/py/pgdbpool.svg)](https://badge.fury.io/py/pgdbpool)

## 1. Primary Scope

<<<<<<< HEAD
The **pgdbpool** Python Module is a tiny **PostgreSQL Database Connection De-Multiplexer** primarily scoped for *Web- / Application Server*.
=======
The **pgdbpool** Python module is a tiny **PostgreSQL Database Connection De-Multiplexer**, primarily designed for *Web- / Application Servers*.
>>>>>>> cb59058 (Corrected syntactically)

## 2. Current Implementation

```text
+----------------------+                         +---------------------
| WebServer Service.py | -- Handler Con #1 ----> | PostgreSQL
| Request / Thread #1  |                         | Backend
+----------------------+                         |
                                                 |
+----------------------+                         |
| WebServer Service.py | -- Handler Con #2 ----> |
| Request / Thread #2  |                         |
+----------------------+                         +---------------------
```

### 2.1. Concept / Simplicity

If configured in a Web Server's WSGI Python script, the pooling logic is straightforward:

1. Check if a free connection in the pool exists.
2. Verify if the connection is usable (SQL ping).
3. Use the connection and protect it from being accessed until the query/queries are completed.
4. Release the connection for reuse.
5. Reconnect to the endpoint if the connection is lost.

## 3. Thread Safety / Global Interpreter Lock

Thread safety is currently ensured via `lock = threading.Lock()`, which relies on a kernel mutex `syscall()`.

While this concept works, the GIL (Global Interpreter Lock) in Python thwarts scalability under heavy loads in a threaded Web Server setup.

>[!IMPORTANT]
> Refer to Section **6: Future** for a potential solution to this problem.

## 4. Dependencies / Installation

<<<<<<< HEAD
**Python3** and **psycopg2** module is required.
=======
**Python 3** and the **psycopg2** module are required.
>>>>>>> cb59058 (Corrected syntactically)

```bash
# install (debian)
apt-get install python3-psycopg2
pip install pgdbpool
```

## 5. Documentation / Examples

<<<<<<< HEAD
See documentation either at ./doc or [https://pythondocs.webcodex.de/pgdbpool](https://pythondocs.webcodex.de/pgdbpool) for detailed explanation / illustrative examples.
=======
Detailed documentation and examples can be found in the `./doc` directory
or at: https://pythondocs.webcodex.de/pgdbpool
>>>>>>> cb59058 (Corrected syntactically)

## 6. Future

The DB-pooling functionality should also be compatible with the FalconAS
Python Application Server (https://github.com/WEBcodeX1/http-1.2).

The proposed model: **1 Process == 1 Python Interpreter (threading-less)**,
effectively solving the GIL issue.

>[!NOTE]
<<<<<<< HEAD
>  Also a Pool should be configurable to use multiple (read-loadbalanced) PostgreSQL Endpoints.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
=======
>  The pool should also be configurable to use multiple (read-load-balanced)
> PostgreSQL endpoints.
>>>>>>> cb59058 (Corrected syntactically)
