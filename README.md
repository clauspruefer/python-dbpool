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
