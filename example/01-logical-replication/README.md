# PostgreSQL Logical Replication Load-Balancing Example

This example demonstrates how the `python-dbpool` module works with multiple write and read configurations in a PostgreSQL logical replication environment. It showcases:

- **Load Balancing**: Distributing database operations across multiple PostgreSQL nodes
- **Write Balancing**: Multiple writer groups (`writer1`, `writer2`) distributing INSERT/UPDATE operations
- **Read Balancing**: Multiple reader groups (`reader1`, `reader2`) distributing SELECT operations
- **Multi-Master Replication**: PostgreSQL logical replication with bidirectional data synchronization

Additionally, this example introduces a minimal Docker orchestration mechanism that configures a running logical-replicated PostgreSQL environment consisting of a test table replicated across multiple PostgreSQL Docker nodes.

The setup configures a static set of PostgreSQL nodes which are then used to run all load-balancing tests. With slight modifications, the setup can be extended to support dynamically adding and removing nodes at runtime (scale up/down).

To demonstrate encapsulated management control channel communications (used as a prototype in our SDMI - Simple Docker Management Instrumentation project), communication between the host orchestrator and Docker containers has been implemented using a JSON-RPC socket communication protocol instead of direct PostgreSQL connections.

## Architecture

### System Overview

The example creates a multi-node PostgreSQL cluster with logical replication, where each node acts as both a publisher and subscriber. This enables a multi-master topology where writes can be distributed across nodes and automatically synchronized.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Host System                                   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Orchestrator (orchestrator.py)           │    │
│  │                                                              │    │
│  │  • Network Configuration (172.16.1.0/24)                   │    │
│  │  • Container Lifecycle Management                          │    │
│  │  • Replication Topology Setup                              │    │
│  │  • JSON-RPC Client Connections                             │    │
│  └──────┬──────────────────┬──────────────────┬────────────────┘    │
│         │                  │                  │                      │
│         │ JSON-RPC         │ JSON-RPC         │ JSON-RPC            │
│         │ Port 64000       │ Port 64000       │ Port 64000          │
├─────────┼──────────────────┼──────────────────┼──────────────────────┤
│         │                  │                  │                      │
│  ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐             │
│  │   Node 0    │    │   Node 1    │    │   Node 2    │   ...       │
│  │ 172.16.1.0  │    │ 172.16.1.1  │    │ 172.16.1.2  │             │
│  │             │    │             │    │             │             │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │             │
│  │ │JSON-RPC │ │    │ │JSON-RPC │ │    │ │JSON-RPC │ │             │
│  │ │ Server  │ │    │ │ Server  │ │    │ │ Server  │ │             │
│  │ │:64000   │ │    │ │:64000   │ │    │ │:64000   │ │             │
│  │ └────┬────┘ │    │ └────┬────┘ │    │ └────┬────┘ │             │
│  │      │      │    │      │      │    │      │      │             │
│  │ ┌────▼────┐ │    │ ┌────▼────┐ │    │ ┌────▼────┐ │             │
│  │ │  PostgreSQL  │ │    │ │  PostgreSQL  │ │    │ │  PostgreSQL  │ │             │
│  │ │  Service │ │    │ │  Service │ │    │ │  Service │ │             │
│  │ │  :5432   │ │    │ │  :5432   │ │    │ │  :5432   │ │             │
│  │ │          │ │    │ │          │ │    │ │          │ │             │
│  │ │ DB: lb-test  │ │    │ │ DB: lb-test  │ │    │ │ DB: lb-test  │ │             │
│  │ │ Table: table1│ │    │ │ Table: table1│ │    │ │ Table: table1│ │             │
│  │ └──────────┘ │    │ └──────────┘ │    │ └──────────┘ │             │
│  │              │    │              │    │              │             │
│  │ Docker Container  │    │ Docker Container  │    │ Docker Container  │             │
│  └──────────────┘    └──────────────┘    └──────────────┘             │
│                                                                       │
│                     Docker Network: dbpool-net                        │
└──────────────────────────────────────────────────────────────────────┘

        ┌──────────────────────────────────────────────┐
        │      Load-Balancing Test Applications        │
        │                                               │
        │  • test-insert.py  (writer1, writer2)        │
        │  • test-update.py  (writer1, writer2)        │
        │  • test-select.py  (reader1, reader2)        │
        │                                               │
        │  Uses python-dbpool with multiple connection │
        │  groups to distribute operations across nodes│
        └──────────────────────────────────────────────┘
```

### Logical Replication Topology

Each node participates in a **multi-master bidirectional replication** setup:

```
Node 0 ────────► Node 1 ────────► Node 2
  ▲                ▲                ▲
  │                │                │
  └────────────────┴────────────────┘
       (Bidirectional Subscriptions)

Publications & Subscriptions:
• Node 0: pub_node0_table1 → subscribed by Node 1, Node 2
• Node 1: pub_node1_table1 → subscribed by Node 0, Node 2
• Node 2: pub_node2_table1 → subscribed by Node 0, Node 1
```

Each node:
1. **Publishes** its changes via a publication (e.g., `pub_node0_table1`)
2. **Subscribes** to all other nodes' publications to receive their changes
3. Uses conflict resolution through timestamps (`update_timestamp` column)

### Components

#### 1. Orchestrator (`orchestrator.py`)
- **Purpose**: Manages the entire cluster lifecycle
- **Responsibilities**:
  - Creates Docker network (`dbpool-net`)
  - Spawns PostgreSQL containers (default: up to 8 nodes)
  - Configures IP addresses from subnet (172.16.1.0/24)
  - Establishes JSON-RPC connections to each node
  - Orchestrates replication setup (publications, subscriptions)
  - Sends commands via JSON-RPC to initialize databases and tables

#### 2. Database Node Containers
Each container includes:

- **PostgreSQL Server** (port 5432)
  - Configured for logical replication (`wal_level = logical`)
  - Hosts database `lb-test` with `table1`
  - Includes replication user credentials
  
- **JSON-RPC Server** (port 64000)
  - Implemented with `microesb` framework
  - Provides service endpoints for database operations
  - Executes SQL commands received from orchestrator
  - Returns operation results via JSON-RPC responses

#### 3. Load-Balancing Test Suite (`lb-setup/`)
- **test-insert.py**: Demonstrates INSERT operations using `writer1` and `writer2` groups
- **test-update.py**: Demonstrates UPDATE operations across writer groups
- **test-select.py**: Demonstrates SELECT operations using `reader1` and `reader2` groups
- **dbconfig.py**: Generates `python-dbpool` configuration from `sysconfig.json`

### Communication Flow

1. **Orchestrator → Node**: JSON-RPC requests (e.g., `init_database`, `create_repl_table`)
2. **Node JSON-RPC Server → PostgreSQL**: Executes SQL commands
3. **PostgreSQL → PostgreSQL**: Logical replication streams (publications/subscriptions)
4. **Test Applications → Nodes**: Direct PostgreSQL connections via `python-dbpool`

### Network Configuration

- **Docker Network**: `dbpool-net` (bridge mode)
- **IP Range**: 172.16.1.0/24
- **Node IP Assignment**: Sequential (172.16.1.0, 172.16.1.1, 172.16.1.2, ...)
- **Configurable Scale**: 2-8 nodes (default: 8) via `sysconfig.json`

## Prerequisites

- **Docker**: Version 20.10 or later
- **Python**: 3.8 or later
- **Python Packages**:
  - `python-dbpool` (the library being demonstrated)
  - `jsocket` (JSON-RPC socket communication)
  - `microesb` (Enterprise Service Bus framework)
  - `ipcalc` (IP address calculations)
  - `psycopg2` (PostgreSQL adapter)

## Setup and Execution

### Step 1: Build the Database Node Docker Image

```bash
cd example/01-logical-replication
./docker-build.sh
```

This creates a Docker image with PostgreSQL and the JSON-RPC server.

### Step 2: Create the Docker Network

```bash
./docker-network.sh
```

This creates the `dbpool-net` bridge network.

### Step 3: Run the Orchestrator

```bash
python3 orchestrator.py
```

The orchestrator will:
1. Start the configured number of PostgreSQL containers
2. Assign IP addresses sequentially
3. Start JSON-RPC servers on each node
4. Initialize databases and create the test table
5. Configure logical replication (publications and subscriptions)

**Expected Output**: JSON-RPC responses confirming successful operations.

### Step 4: Run Load-Balancing Tests

#### Test Inserts (Write Load-Balancing)
```bash
cd lb-setup
python3 test-insert.py
```

Inserts 200 iterations × 4 rows = 800 total rows distributed across `writer1` and `writer2` connection groups.

#### Test Updates (Write Load-Balancing)
```bash
python3 test-update.py
```

Updates rows across multiple writer groups to test replication and conflict resolution.

#### Test Selects (Read Load-Balancing)
```bash
python3 test-select.py
```

Performs SELECT queries distributed across `reader1` and `reader2` connection groups.

### Step 5: Verify Replication

Connect to any node and verify that all rows are replicated:

```bash
docker exec -it node0 psql -U testwriter -d lb-test -c "SELECT COUNT(*) FROM table1;"
docker exec -it node1 psql -U testwriter -d lb-test -c "SELECT COUNT(*) FROM table1;"
docker exec -it node2 psql -U testwriter -d lb-test -c "SELECT COUNT(*) FROM table1;"
```

All nodes should return the same row count, demonstrating successful replication.

## Configuration

### System Configuration (`sysconfig.json`)

Key parameters:
- **`max-nodes`**: Maximum number of database nodes (default: 8)
- **`subnet`**: IPv4 subnet for Docker network
- **`roles`**: Database user credentials (admin, replication user)

### Connection Pool Configuration (`lb-setup/dbconfig.py`)

Defines connection groups:
- **`writer1`**: 20 connections for write operations
- **`writer2`**: 10 connections for write operations
- **`reader1`**: 24 connections for read operations
- **`reader2`**: 48 connections for read operations

Each group automatically load-balances across all available nodes.

## Expected Outcomes

1. **Load Distribution**: Operations are evenly distributed across nodes based on connection pool configuration
2. **Data Consistency**: All nodes contain identical data due to logical replication
3. **Write Scalability**: Write throughput scales with additional nodes (writer groups)
4. **Read Scalability**: Read throughput scales with additional nodes and larger reader connection pools
5. **Conflict Resolution**: Timestamp-based conflict resolution handles concurrent updates

## OOP Abstraction

The OOP abstraction model inside the Docker containers has been implemented using the **python-microesb** framework, which provides:
- Service registration and discovery
- JSON-RPC endpoint management
- Method routing and invocation
- Structured request/response handling

The orchestrator code inside `orchestrator.py` (due to time constraints) is currently procedural and will be refactored to use the python-microesb abstraction model (see SDMI project for the evolved architecture).

## Cleanup

To stop and remove all containers:

```bash
docker ps -a --filter "name=node" --format "{{.Names}}" | xargs docker stop
docker ps -a --filter "name=node" --format "{{.Names}}" | xargs docker rm
```

To remove the Docker network:

```bash
docker network rm dbpool-net
```

## Notes

- This is a **development/testing example** with hardcoded credentials. Never use these credentials in production.
- The setup is designed for local development and demonstration purposes.
- For production use, implement proper security measures (credential management, TLS encryption, firewall rules).
- The example can be extended to support dynamic node addition/removal for elastic scaling.

## Related Documentation

- See `REPLICATION-ORDER.md` for detailed replication setup sequence
- See `svc_call_metadata.py` for JSON-RPC service call definitions
- See `db-node-rpc/` directory for JSON-RPC server implementation details
