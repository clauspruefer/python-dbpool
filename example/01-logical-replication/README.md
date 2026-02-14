# PostgreSQL Logical Replication Load-Balancing Example

This example demonstrates how the `python-dbpool` module works with multiple write and read configurations in a PostgreSQL logical replication environment. It showcases:

- **Load Balancing**: Distributing database operations across multiple PostgreSQL nodes
- **Write Balancing**: Multiple writer groups (`writer1`, `writer2`) distributing INSERT/UPDATE operations
- **Read Balancing**: Multiple reader groups (`reader1`, `reader2`) distributing SELECT operations
- **Multi-Master Replication**: PostgreSQL logical replication with bidirectional data synchronization

Additionally, this example introduces a minimal Docker orchestration mechanism that configures a running logical-replicated PostgreSQL environment consisting of a test table replicated across multiple PostgreSQL Docker nodes.

The setup configures a static set of PostgreSQL nodes which are then used to run all load-balancing tests. With slight modifications, the setup can be extended to support dynamically adding and removing nodes at runtime (scale up/down).

To demonstrate encapsulated management control channel communications (used as a prototype in our SDMI - Simple Docker Management Instrumentation project), communication between the host orchestrator and Docker containers has been implemented using a JSON-RPC socket communication protocol instead of direct PostgreSQL connections.

## 1. Prerequisites

- **Docker**: Required for running PostgreSQL nodes in containers
- **Docker Permissions**: Ensure your user has proper Docker permissions (add user to `docker` group or run with appropriate privileges)
- **Python 3.x**: Python 3.6 or higher
- **Network Configuration**: The setup creates a Docker network `172.16.1.0/24` - ensure this subnet doesn't conflict with existing networks

The following Python packages are required on the **host** machine:

- **pgdbpool**: The database connection pool library (this repository's package)
- **jsocket**: JSON socket communication library (included in `packages/` directory)
- **ipcalc**: IP address calculation utilities for network configuration

The following PyPi modules will be installed **inside each Docker container**:

- **python3-psycopg2**: PostgreSQL adapter for Python (installed via apt)
- **microesb**: Python Micro ESB framework for service orchestration and message routing
- **jsocket**: JSON-RPC socket communication protocol (version 1.9.5)

## 2. Architecture

This demonstration instantiates a multi-node PostgreSQL cluster employing bidirectional logical replication, wherein each node functions simultaneously as both a publisher and subscriber. Such a configuration establishes a multi-master topology, permitting writes to be distributed across nodes while maintaining automatic, eventual data consistency through PostgreSQL's logical replication mechanism.

Standard PostgreSQL logical replication using native write-ahead log (WAL) streaming exhibits inherent limitations in multi-master scenarios, particularly concerning primary key conflicts and update sequencing. To guarantee deterministic data synchronization across INSERT, UPDATE, and DELETE operations, this implementation incorporates two architectural enhancements:

1. **Partitioned Primary Key Space**: The primary key sequences (PostgreSQL `bigserial` type) are initialized with node-specific offsets and multiplicators. Each node operates within a designated range of the 32-bit integer space, thereby eliminating primary key collisions during concurrent insert operations across nodes.

2. **Temporal Conflict Resolution**: An update timestamp column (`upd_ts`) with a corresponding trigger function ensures temporal ordering of updates. The trigger conditionally applies updates only when the incoming modification timestamp exceeds the existing column value, effectively preventing stale updates from overwriting more recent data in scenarios involving replication lag or out-of-order delivery.

### 2.1. PostgreSQL Cluster

The PostgreSQL cluster is instantiated as a collection of containerized database instances, each executing within an isolated Docker environment. The cluster's cardinality—defined by the parameter `['system']['networks'][0]['config']['scale']['max_nodes']` in `sysconfig.json`—determines the number of peer nodes participating in the logical replication topology.

Each PostgreSQL instance is provisioned with identical schema definitions but operates with node-specific configuration parameters to enable multi-master replication. Critical configuration adjustments include elevated `wal_level` (set to `logical`), increased `max_wal_senders` and `max_replication_slots` to accommodate multiple replication channels, and `max_logical_replication_workers` to support concurrent subscription processing. These parameters are applied via the `patch-config.sh` initialization script during container bootstrapping.

The cluster topology is fully connected: each node establishes publication and subscription relationships with all other nodes, creating a mesh replication architecture. This ensures that modifications committed to any node propagate bidirectionally to all peers, achieving eventual consistency across the distributed dataset.

### 2.2. Cluster Orchestration

The orchestration subsystem (`orchestrator.py`) executes on the host system and coordinates the lifecycle management of PostgreSQL nodes through a JSON-RPC communication channel rather than direct PostgreSQL protocol connections. This architectural decision provides encapsulation of control-plane operations, separating administrative workflows from data-plane database traffic—a design pattern employed as a prototype within the SDMI (Simple Docker Management Instrumentation) project.

Communication between the orchestrator and containerized nodes leverages the `jsocket` library, implementing a synchronous request-response protocol over TCP sockets. Each container exposes a JSON-RPC service endpoint (port 64000) that accepts administrative commands for database initialization, replication configuration, and topology management.

The orchestrator's add node mechanism is **designed** to add **one** node **after each other** to the replication topology, making it possible to dynamically scale up or down by adding single nodes sequentially. This design enables gradual cluster expansion and contraction in production environments without requiring batch operations. The orchestrator maintains a persistent connection pool to all active nodes, enabling efficient command dispatch throughout the cluster's operational lifetime.

### 2.3. Test Setup

Following successful cluster orchestration, the test harness can be executed to validate load-balancing and replication behavior. The test suite comprises three sequential components, each exercising distinct database operation patterns:

1. **Insert Test** (`test-insert.py`): Performs concurrent bulk insertions using two writer groups (`writer1` and `writer2`). The test distributes 400 insert operations across the configured writer endpoints, validating that pgdbpool correctly balances write traffic and that logical replication propagates inserts to all nodes.

2. **Update Test** (`test-update.py`): Validates concurrent update handling through three parallel threads executing conflicting modifications to shared records. This test specifically exercises the temporal conflict resolution mechanism, ensuring that the `upd_ts` trigger correctly serializes concurrent updates based on timestamp ordering.

3. **Select Test** (`test-select.py`): Executes concurrent read operations using two reader groups (`reader1` and `reader2`) with varying query patterns and frequencies. This test confirms that pgdbpool distributes read load across available replica nodes and that replicated data remains consistent across all cluster members.

> [!WARNING]
> To restart the tests, DELETE all rows from table1 or restart the orchestrator (after stopping all containers)

## 3. OOP Model

The object-oriented design within each containerized node employs the `python-microesb` framework, which provides structured abstractions for message routing, command dispatch, and service orchestration. This microservice-oriented architecture encapsulates database management operations (e.g., replication subscription establishment, publication configuration, schema manipulation) as discrete service handlers, promoting separation of concerns and testability.

In contrast, the orchestrator implementation (`orchestrator.py`) exhibits a more procedural structure, prioritizing rapid prototyping over architectural refinement. This disparity in code quality reflects deliberate engineering tradeoffs: the containerized service layer is designed for production deployment and extensibility, whereas the orchestrator serves primarily as a bootstrapping utility and will undergo future refactoring to align with the microesb abstraction patterns utilized in the SDMI project.

## 4. How to Run Tests

The execution workflow consists of three sequential phases: Docker image construction, cluster orchestration, and test execution. 

First, navigate to the example directory and build the custom PostgreSQL Docker image using the provided build script. This image extends the official PostgreSQL base image with Python runtime, `psycopg2` adapter, and the `microesb` framework required for JSON-RPC service endpoints:

```bash
cd ./example/01-logical-replication
./docker-build.sh
```

Next, execute the orchestrator script to provision the PostgreSQL cluster. This script creates the Docker network, instantiates the configured number of containers, establishes logical replication topology, and initializes the test schema:

```bash
python3 orchestrator.py
```

Finally, run the test suite sequentially from the `lb-setup` directory. Each test must complete before proceeding to the next, as they have ordered dependencies (insert before update, update before select):

```bash
cd lb-setup
python3 test-insert.py
python3 test-update.py
python3 test-select.py
```

Monitor cluster behavior by observing replication lag, connection distribution across pool groups, and data consistency across nodes. PostgreSQL logs within each container provide detailed information regarding logical replication worker activity and subscription synchronization status.
