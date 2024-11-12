# Python PgDatabase-Pool Module

## 1. Primary Scope

The **pg-dbpool** Python Module is a tiny database de-multiplexer primarily scoped for Web- / Application Server.

## 2. Current Implementation

```bash

+----------------------+                         +--------------- -  -   -
| WebServer Service.py | -- Con Handler #1 ----> | PostgreSQL 
| Request / Thread #1  |                         | Backend
+----------------------+                         |
                                                 |
+----------------------+                         |
| WebServer Service.py | -- Con Handler #2 ----> | 
| Request / Thread #2  |                         |
+----------------------+                         +--------------- -  -   -
```

### 2.1. Explanation / Simplicity

If configured in a WebServers WSGI Python Script, the Pooling-Logic is quite simple.

From a configured **Pool** (Postgres Database Destination, Max Connection Count):

1. Check if a free connection in the pool exists
2. If yes, use it and protect it from beeing used until finished

## 3. Thread Safety / Global Interpreter Lock

## 4. Documentation / Examples

## 5. Future

DB-Pooling also should be usable in FalconAS Python Application Server (https://github.com/WEBcodeX1/http-1.2/).

The model here: 1 Process == 1 Python Interpreter (without threading). 

>[!NOTE]
> Logic has to be adapted.
