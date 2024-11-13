# Python PgDatabase-Pool Module

## 1. Primary Scope

The **pgdbpool** Python Module is a tiny database de-multiplexer primarily scoped for Web- / Application Server.

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

### 2.1. Explanation / Simplicity

If configured in a Web-Servers WSGI Python Script, the Pooling-Logic is quite simple.

From a configured **Pool** (Postgres Database Destination, Max Connection Count):

1. Check if a free connection in the pool exists
2. If yes, use it and protect it from beeing used until finished

## 3. Thread Safety / Global Interpreter Lock

Currently Thread Safety is guaranteed by `lock = threading.Lock()` which implies a Kernel Mutex syscall().

The concept works, but the GIL (Python Global Interpreter Lock) thwarts our plans 😞.

In detail: our concept works, but it is indeed a performance / scaling killer.

## 4. Dependencies / Installation

**Python 3** and **psycopg2** module is required. A simple `pip3 install pgdbpool` from PyPi should do the trick.

## 5. Documentation / Examples

See documentation [./doc](./doc) for detailed explanation / illustrative examples.

## 6. Future

DB-Pooling also should be usable in FalconAS Python Application Server (https://github.com/WEBcodeX1/http-1.2/).

The model here: 1 Process == 1 Python Interpreter (threading-less), GIL Problem solved :grin:.

>[!NOTE]
>  Also a Pool should be configurable to use multiple (read-loadbalanced) PostgreSQL endpoints.
