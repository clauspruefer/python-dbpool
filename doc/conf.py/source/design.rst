.. design

==================
Architecture Design
==================

Overview of pgdbpool's architecture patterns and deployment models.

1. Threading Models
===================

pgdbpool supports both threaded and non-threaded deployment models to optimize for different server architectures.

**Threaded Model (Default)**

Designed for threaded web servers like Apache with mod_wsgi, Gunicorn with threads, or Flask development servers:

.. code-block:: text

    +-----------------------------------------------------------------------------+
    | Web Server (Apache/Gunicorn+threads)                                       |
    |-----------------------------------------------------------------------------|
    | pgdbpool Module (Thread-Safe)                                              |
    | - Connection locking enabled                                                |
    | - Thread-safe connection iteration                                          |
    +-----------------------------------------------------------------------------+
    |  Thread 1     |  Thread 2     |  Thread 3     |  Thread 4     | Thread N   |
    |  Handler      |  Handler      |  Handler      |  Handler      | Handler    |
    +-----------------------------------------------------------------------------+
             |               |               |               |              |
    +--------+---------------+---------------+---------------+--------------+----+
    | Connection Pool (Shared across threads)                                    |
    | - Automatic load balancing across DB endpoints                             |
    | - Thread-safe connection allocation                                         |
    +-----------------------------------------------------------------------------+
             |               |               |               |              |
    +--------+---------------+---------------+---------------+--------------+----+
    |  DB Node 1    |  DB Node 1    |  DB Node 2    |  DB Node 2    | DB Node N  |
    |  Connection   |  Connection   |  Connection   |  Connection   | Connection |
    +-----------------------------------------------------------------------------+

**Non-Threaded Model**

Optimized for process-based servers like Gunicorn with workers, uWSGI, or single-threaded applications:

.. code-block:: text

    +-----------------------------------------------------------------------------+
    | Web Server (Gunicorn+workers/uWSGI)                                        |
    |-----------------------------------------------------------------------------|
    | pgdbpool Module (Non-Threaded)                                             |
    | - No connection locking overhead                                            |
    | - Optimized for single-threaded access                                     |
    +-----------------------------------------------------------------------------+
    |  Process 1    |  Process 2    |  Process 3    |  Process 4    | Process N  |
    |  Handler      |  Handler      |  Handler      |  Handler      | Handler    |
    |  (Isolated)   |  (Isolated)   |  (Isolated)   |  (Isolated)   | (Isolated) |
    +-----------------------------------------------------------------------------+
             |               |               |               |              |
    +--------+---------------+---------------+---------------+--------------+----+
    | Per-Process Connection Pool                                                 |
    | - Load balancing across DB endpoints                                        |
    | - No inter-process locking required                                         |
    +-----------------------------------------------------------------------------+

2. Multi-Database Load Balancing
=================================

pgdbpool now supports automatic load balancing across multiple database endpoints:

.. code-block:: text

    +-----------------------------------------------------------------------------+
    | Application Layer                                                           |
    +-----------------------------------------------------------------------------+
    | pgdbpool Connection Manager                                                 |
    | - Database endpoint rotation                                                |
    | - Automatic failover handling                                               |
    | - Connection health monitoring                                              |
    +-----------------------------------------------------------------------------+
                                    |
    +-----------------------------------+-----------------------------------+
    |                                   |                                   |
    +-------------------+               +-------------------+               +
    | Primary Database  |               | Secondary Database|               |
    | - Read/Write      |               | - Read/Write      |               |
    | - High Priority   |               | - Backup/Replica  |               |
    +-------------------+               +-------------------+               +
    | Connection Pool   |               | Connection Pool   |               |
    | Group 1: 15 conns |               | Group 1: 15 conns |               |
    | Group 2: 10 conns |               | Group 2: 10 conns |               |
    +-------------------+               +-------------------+               +

**Key Features:**

- **Transparent Load Balancing**: Connections are automatically distributed across available database endpoints
- **High Availability**: Automatic failover when database endpoints become unavailable
- **Scalability**: Add database replicas without application code changes
- **Performance**: Reduced load on individual database servers

3. Connection Group Architecture  
=================================

Connection groups allow fine-grained control over connection behavior:

**Autocommit Groups** (``autocommit: true``)
  - Immediate transaction commits
  - Optimal for read operations and simple writes
  - Lower overhead, higher throughput

**Transaction Groups** (``autocommit: false``)
  - Manual transaction control with ``commit()``
  - Essential for complex multi-statement transactions
  - ACID compliance for critical operations

.. code-block:: text

    +-----------------------------------------------------------------------------+
    | Application Handlers                                                        |
    +-----------------------------------------------------------------------------+
    |              |                    |                    |                   |
    | READ_POOL    | WRITE_POOL         | TRANSACTION_POOL   | BATCH_POOL        |
    | autocommit:  | autocommit:        | autocommit:        | autocommit:       |
    | true         | true               | false              | false             |
    |              |                    |                    |                   |
    | Simple       | Quick writes       | Complex            | Bulk operations   |
    | queries      | Single statements  | transactions       | Data imports      |
    +-----------------------------------------------------------------------------+

4. Deployment Recommendations
=============================

**Threaded Model Use Cases:**

- Apache with mod_wsgi (default)
- Gunicorn with ``--workers=1 --threads=N``
- Flask/Django development servers
- Applications with moderate concurrency

**Non-Threaded Model Use Cases:**

- Gunicorn with ``--workers=N --threads=1`` 
- uWSGI in worker mode
- High-performance applications avoiding GIL contention
- Microservices with dedicated processes

**Configuration Guidelines:**

.. list-table:: Threading Model Selection
   :widths: 20 40 40
   :header-rows: 1

   * - Server Type
     - Recommended Model
     - Configuration
   * - Apache + mod_wsgi
     - ``threaded``
     - Standard threading with connection locking
   * - Gunicorn (threads)
     - ``threaded``  
     - Thread-safe connection handling
   * - Gunicorn (workers)
     - ``non-threaded``
     - Process isolation, no locking overhead
   * - uWSGI (workers)
     - ``non-threaded``
     - Optimized for process-based architecture
   * - Development
     - ``threaded``
     - General compatibility, easier debugging

5. Performance Considerations
=============================

**Connection Pool Sizing:**

- **Threaded**: Pool size should accommodate peak concurrent threads
- **Non-threaded**: Smaller pools per process (typically 3-10 connections)
- **Multi-DB**: Connections distributed automatically across endpoints

**Memory Usage:**

- Each connection consumes ~8-16MB depending on ``session_tmp_buffer``
- Non-threaded model typically uses less memory per connection
- Monitor total memory usage: ``(connections × buffer_size × processes)``

**Latency Optimization:**

- Place database replicas geographically close to application servers
- Use appropriate ``connect_timeout`` and ``query_timeout`` values
- Consider connection keep-alive settings for high-frequency access
