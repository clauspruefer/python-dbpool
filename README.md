# Python PgDatabase-Pool Module

![push main](https://github.com/clauspruefer/python-dbpool/actions/workflows/pylint.yaml/badge.svg)
[![PyPI version](https://badge.fury.io/py/pgdbpool.svg)](https://badge.fury.io/py/pgdbpool)

## 1. Primary Scope

The **pgdbpool** Python Module is a tiny PostgreSQL Database Connection De-Multiplexer primarily scoped for *Web- / Application Server*.

## 2. Current Implementation

```bash

+----------------------+                         +--------------- -  -   -
| WebServer Service.py | -- Handler Con #1 ----> | PostgreSQL 
| Request / Thread #1  |                         | Backend
+----------------------+                         |
                                                 |
+----------------------+                         |
| WebServer Service.py | -- Handler Con #2 ----> | 
| Request / Thread #2  |                         |
+----------------------+                         +--------------- -  -   -
```

### 2.1. Concept / Simplicity

If configured in a Web-Servers WSGI Python Script, the Pooling-Logic is quite simple.

1. Check if a free connection in the pool exists
2. Check if connection usable (SQL ping)
3. Use connection and protect it from beeing used until querie(s) finished
4. Release connection for usage again
5. Try reconnecting to endpoint if connection has been lost

## 3. Thread Safety / Global Interpreter Lock

Currently Thread Safety is guaranteed by `lock = threading.Lock()` which implies a Kernel Mutex syscall().

The concept works, but the GIL (Python Global Interpreter Lock) thwarts our plans 😞.

In detail: if used in a threaded Web-Server setup, it does not really scale well on heavy loads.

>[!IMPORTANT]
> Take a closer look at **"6. Future"**, problem solved probably.

## 4. Dependencies / Installation

**Python3** and **psycopg2** module is required.

```bash
# install (debian)
apt-get install python3-psycopg2
pip install pgdbpool
```

## 5. Documentation / Examples

See documentation either at ./doc or [https://pythondocs.webcodex.de/pgdbpool](https://pythondocs.webcodex.de/pgdbpool) for detailed explanation / illustrative examples.

## 6. Future

DB-Pooling also should be usable in FalconAS Python Application Server (https://github.com/WEBcodeX1/http-1.2).

The model here: 1 Process == 1 Python Interpreter (threading-less), GIL Problem solved.

>[!NOTE]
>  Also a Pool should be configurable to use multiple (read-loadbalanced) PostgreSQL Endpoints.
