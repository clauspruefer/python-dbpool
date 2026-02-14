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

The example creates a multi-node PostgreSQL cluster with logical replication, where each node acts as both a publisher and subscriber. This enables a multi-master topology where writes can be distributed across nodes and automatically synchronized.

This setup does not work 100% out of the box (using postgresql native write ahead log streaming alone), we adapted some slight modifications which guarantee 100% data synchronization for INSERT, UPDATE **and** DELETE scenarios.

a) The table(s) primary key (bigserial type) sequences will be set individually on each node (so that enough space exists between, each node has space for serial 4byte/32bit type)
b) Using a update timestamp column and an appropriate update trigger which only updates if current time > ts in update column (prevents overwriting by delayed updates)

### 2.1. PostgreSQL Cluster

Before the test setup is startable, a local PostgreSQL cluster will be set up using Docker containers. The number of nodes to start is configurable in `sysconfig.json` (`['system']['networks'][0]['config']['scale']['max_nodes']`), with a default range of 2-8 nodes.

**Architecture Overview (Multi-Node PostgreSQL Replication)**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ Host Machine (172.16.1.254)                                         │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Orchestrator (orchestrator.py)                             │    │
│  │ - Starts Docker containers                                 │    │
│  │ - Configures replication topology                          │    │
│  │ - Manages JSON-RPC communication                           │    │
│  └─────────┬──────────────┬──────────────┬────────────────────┘    │
│            │ JSON-RPC     │ JSON-RPC     │ JSON-RPC                 │
│            │ :64000       │ :64000       │ :64000                   │
└────────────┼──────────────┼──────────────┼──────────────────────────┘
             │              │              │
   ┌─────────▼─────┐ ┌─────▼──────┐ ┌─────▼──────┐
   │ Node0         │ │ Node1      │ │ Node2      │
   │ 172.16.1.0    │ │ 172.16.1.1 │ │ 172.16.1.2 │
   │               │ │            │ │            │
   │ PostgreSQL    │ │ PostgreSQL │ │ PostgreSQL │
   │ :5432         │ │ :5432      │ │ :5432      │
   │               │ │            │ │            │
   │ JSON-RPC Srv  │ │ JSON-RPC   │ │ JSON-RPC   │
   │ :64000        │ │ Srv :64000 │ │ Srv :64000 │
   └───────┬───────┘ └─────┬──────┘ └──────┬─────┘
           │               │               │
           │  Logical      │   Logical     │
           │  Replication  │   Replication │
           │  (Pub/Sub)    │   (Pub/Sub)   │
           └───────────────┴───────────────┘
                Bidirectional Sync
```

Each node in the cluster:
- Runs PostgreSQL with **logical replication** enabled (`wal_level = logical`)
- Acts as both **publisher** and **subscriber** (multi-master topology)
- Has a dedicated JSON-RPC server on port 64000 for management commands
- Exposes PostgreSQL on port 5432 for client connections
- Contains an identical `table1` schema with unique sequence ranges per node

### 2.2. Cluster Orchestration

The orchestrator runs on the "host" using JSON-RPC to communicate with each Docker container (node) after the nodes have been started. While this could have been done via direct PostgreSQL port 5432 communication, JSON-RPC encapsulation via python-microesb was chosen to build a clean, abstracted OOP model on the container nodes.

The orchestration model adds nodes sequentially (**one at a time**, not multiple simultaneously) to support later scale-up/scale-down operations (as used in the SDMI project).

**JSON-RPC Communication Flow**:

```
Host Orchestrator                        Docker Node (e.g., node1)
(orchestrator.py)                        (JSON-RPC Server :64000)
      │                                            │
      │  1. update_net_topology                   │
      ├──────────────────────────────────────────►│
      │     (network config, node metadata)       │
      │                                            │
      │◄───────────────────────────────────────────┤
      │  {status: success}                        │
      │                                            │
      │  2. init_database                         │
      ├──────────────────────────────────────────►│
      │     (create database, roles, etc.)        │
      │                                            │
      │◄───────────────────────────────────────────┤
      │  {status: success}                        │
      │                                            │
      │  3. create_repl_table                     │
      ├──────────────────────────────────────────►│
      │     (create table1 with adjusted          │
      │      sequence range)                      │
      │                                            │
      │◄───────────────────────────────────────────┤
      │  {status: success}                        │
      │                                            │
      │  4. create_publication                    │
      ├──────────────────────────────────────────►│
      │     (create pub_node1_table1)             │
      │                                            │
      │◄───────────────────────────────────────────┤
      │  {status: success}                        │
      │                                            │
      │  5. subscribe_to_others                   │
      ├──────────────────────────────────────────►│
      │     (subscribe to previous nodes)         │
      │                                            │
      │◄───────────────────────────────────────────┤
      │  {status: success}                        │
      │                                            │
      │  6. subscribe_to_node (on prev nodes)     │
      ├──────────────────────────────────────────►│
      │     (make prev nodes subscribe to         │
      │      this node)                            │
      │                                            │
```

**Key Management Commands**:
- `update_net_topology`: Configures network settings and node metadata
- `init_database`: Creates database, users, and roles
- `create_repl_table`: Creates `table1` with node-specific sequence ranges and update triggers
- `create_publication`: Creates logical replication publication for the node's data
- `subscribe_to_others`: Subscribes current node to all previous nodes
- `subscribe_to_node`: Makes previous nodes subscribe to the current node (bidirectional sync)

### 2.3. Test Setup

After the cluster orchestration (setup) has been completed successfully, the tests can be run.

**Load Balancing Architecture**:

```
┌──────────────────────────────────────────────────────────────────┐
│ Test Scripts (lb-setup/)                                         │
│                                                                   │
│  test-insert.py        test-update.py        test-select.py      │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      │
│  │ writer1 (20)│      │ writer1 (20)│      │ reader1 (24)│      │
│  │ writer2 (10)│      │ writer2 (10)│      │ reader2 (48)│      │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘      │
│         │                    │                    │              │
│         │  pgdbpool Connection Pool (dbconfig.py) │              │
│         └────────────────────┼────────────────────┘              │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
   ┌───▼────┐             ┌────▼───┐             ┌────▼───┐
   │ Node0  │             │ Node1  │             │ Node2  │
   │ :5432  │◄───────────►│ :5432  │◄───────────►│ :5432  │
   │        │  Replication│        │  Replication│        │
   └────────┘             └────────┘             └────────┘

Writer Groups:
  - writer1: 20 connections, round-robin across all nodes
  - writer2: 10 connections, round-robin across all nodes

Reader Groups:
  - reader1: 24 connections, load-balanced across all nodes
  - reader2: 48 connections, load-balanced across all nodes
```

The following tests exist and must be started in the given order:

**1. Insert Test (`test-insert.py`)**
   - **Purpose**: Demonstrates write load balancing across multiple PostgreSQL nodes
   - **Operation**: Performs 200 iterations of bulk inserts using two writer groups
   - **Writer Groups**: 
     - `writer1`: Inserts 2 rows per iteration ('test1', 'test2' and 'test3', 'test4')
     - `writer2`: Inserts 2 rows per iteration ('test100', 'test200' and 'test300', 'test400')
   - **Total Rows**: 800 rows inserted across all nodes
   - **Validation**: All nodes should eventually contain the same data via logical replication

**2. Update Test (`test-update.py`)**
   - **Purpose**: Verifies that concurrent updates from multiple writers work correctly with timestamp-based conflict resolution
   - **Operation**: Creates test rows, then performs concurrent updates using 3 threads
   - **Thread Behavior**:
     - `updater1`: 20 updates with 0.1s sleep (writer1)
     - `updater2`: 40 updates with 0.2s sleep (writer2)
     - `updater3`: 15 updates with 0.8s sleep (writer1)
   - **Conflict Resolution**: The update trigger ensures that only updates with newer timestamps overwrite existing data
   - **Expected Result**: The final value should be from the most recent update based on timestamp

**3. Select Test (`test-select.py`)**
   - **Purpose**: Demonstrates read load balancing across replica nodes
   - **Operation**: Runs 3 concurrent reader threads executing different SELECT queries
   - **Thread Behavior**:
     - `reader1`: 50 iterations, queries rows with id between 1 and 100000 (0.1s sleep)
     - `reader2`: 80 iterations, queries rows with id > 100000 (0.2s sleep)
     - `reader3`: 150 iterations, full table scan (0.1s sleep)
   - **Load Distribution**: Queries are distributed across all available nodes using the reader connection pools
   - **Total Queries**: 280 SELECT operations distributed across the cluster

> [!WARNING]
> To restart the tests, DELETE all rows from `table1` or restart the orchestrator (after stopping all containers)

## 3. OOP Model

The OOP models quality used inside each container node is modeled by python-microesb which allows fine grained (clean code) modeling and
is considered *production-ready* whereas the codes quality in `orchestrator.py` is limited (*fast time to market* was the directive).

## 4. How to Run Tests

```bash
cd ./example/01-logical-replication
./docker-build.sh
python3 orchestrator.py
```
