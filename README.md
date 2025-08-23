# :elephant: Python PgDatabase-Pool Module

![push main](https://github.com/clauspruefer/python-dbpool/actions/workflows/pylint.yaml/badge.svg)
[![PyPI version](https://badge.fury.io/py/pgdbpool.svg)](https://badge.fury.io/py/pgdbpool)

## 1. Primary Scope

The **pgdbpool** Python module is a tiny **PostgreSQL Database Connection De-Multiplexer**, primarily designed for *Web- / Application Servers*.

**Key Features:**
- **Multi-endpoint support**: Load balance across multiple PostgreSQL servers
- **Flexible threading models**: Choose between threaded and non-threaded modes
- **Transaction control**: Manual commit support for complex transactions
- **High availability**: Built-in failover and connection management

## 2. Current Implementation

```text
+----------------------+                         +---------------------
| WebServer Service.py | -- Handler Con #1 ----> | PostgreSQL
| Request / Thread #1  |                         | Backend #1
+----------------------+                         |
                                                 |
+----------------------+                         |
| WebServer Service.py | -- Handler Con #2 ----> | PostgreSQL
| Request / Thread #2  |                         | Backend #2
+----------------------+                         +---------------------
```

### 2.1. Multiple Database Endpoints

The connection pool now supports **multiple PostgreSQL database endpoints** for load balancing and high availability:

- ✅ Configure multiple database hosts in the configuration
- ✅ Connections are automatically distributed across available endpoints
- ✅ Provides built-in load balancing for read operations
- ✅ Enhances fault tolerance and scalability

### 2.2. Concept / Simplicity

If configured in a Web Server's WSGI Python script, the pooling logic is straightforward:

1. Check if a free connection in the pool exists.
2. Verify if the connection is usable (SQL ping).
3. Use the connection and protect it from being accessed until the query/queries are completed.
4. Release the connection for reuse.
5. Reconnect to the endpoint if the connection is lost.

## 3. Thread Safety / Global Interpreter Lock

### 3.1. Threading Model Configuration

The pool now supports **two threading models** that can be configured based on your application's architecture:

- **`threaded`** (default): Uses `threading.Lock()` for thread safety, suitable for traditional multi-threaded web servers
- **`non-threaded`**: Disables locking for single-threaded applications, eliminating GIL overhead

### 3.2. Threaded Mode

Thread safety is ensured via `lock = threading.Lock()`, which relies on a kernel mutex `syscall()`.

While this concept works, the GIL (Global Interpreter Lock) in Python thwarts scalability under heavy loads in a threaded Web Server setup.

### 3.3. Non-Threaded Mode

For applications using a single-threaded, process-per-request model (like the FalconAS Python Application Server), the non-threaded mode provides:

- **No locking overhead** - eliminates mutex syscalls
- **Better performance** - avoids GIL contention  
- **Simpler architecture** - designed for 1 Process == 1 Python Interpreter

>[!IMPORTANT]
> Refer to Section **6: Future** for more details on threading-less architectures.

## 4. Dependencies / Installation

**Python 3** and the **psycopg2** module are required.

```bash
# install (debian)
apt-get install python3-psycopg2
pip install pgdbpool
```

## 5. Documentation / Examples

See documentation either at `./doc` or [https://pythondocs.webcodex.de/pgdbpool/v1.0](https://pythondocs.webcodex.de/pgdbpool/v1.0)
for detailed explanation / illustrative examples.

### 5.1. Multiple Database Configuration

```python
config = {
    'db': [
        {
            'host': 'postgres-server-1.example.com',
            'name': 'mydb',
            'user': 'dbuser',
            'pass': 'dbpass'
        },
        {
            'host': 'postgres-server-2.example.com', 
            'name': 'mydb',
            'user': 'dbuser',
            'pass': 'dbpass'
        }
    ],
    'groups': {
        'default': {
            'connection_count': 20,
            'autocommit': True
        }
    }
}
```

### 5.2. Threading Model Configuration

```python
# for non-threaded applications (e.g., FalconAS)
config = {
    'type': 'non-threaded',
    'db': { ... },
    'groups': { ... }
}

# for traditional threaded applications (default)
config = {
    'type': 'threaded',  # or omit for default
    'db': { ... },
    'groups': { ... }
}
```

### 5.3. Manual Transaction Control

```python
import pgdbpool as dbpool

dbpool.Connection.init(config)

# for autocommit=False connections
with dbpool.Handler('group1') as db:
    db.query('INSERT INTO table1 VALUES (%s)', ('value1',))
    db.query('INSERT INTO table2 VALUES (%s)', ('value2',))
    db.commit()  # Manual commit
```

## 6. Future

### 6.1. FalconAS Compatibility

The DB-pooling functionality is now compatible with the FalconAS
Python Application Server (https://github.com/WEBcodeX1/http-1.2).

The implemented model: **1 Process == 1 Python Interpreter (threading-less)**,
effectively solving the GIL issue through the `non-threaded` configuration mode.

### 6.2. Load Balancing

The pool now supports multiple (read-load-balanced) PostgreSQL endpoints:

- ✅ **Implemented**: Multiple database endpoint configuration
- ✅ **Implemented**: Automatic connection distribution across endpoints
- ✅ **Implemented**: Built-in load balancing for database connections
- ✅ **Implemented**: Read / write / endpoint group separation

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
