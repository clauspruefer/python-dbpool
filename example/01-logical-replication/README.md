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

- Docker
- Setting Docker permissions correctly

The following PyPi modules will be installed ...

- Python Micro ESB ()

## 2. Architecture

The example creates a multi-node PostgreSQL cluster with logical replication, where each node acts as both a publisher and subscriber. This enables a multi-master topology where writes can be distributed across nodes and automatically synchronized.

This setup does not work 100% out of the box (using postgresql native write ahead log streaming alone), we adapted some slight modifications which guarantee 100% data synchronization for INSERT, UPDATE **and** DELETE scenarios.

a) The table(s) primary key (bigserial type) sequences will be set individually on each node (so that enough space exists between, each node has space for serial 4byte/32bit type)
b) Using a update timestamp column and an appropriate update trigger which only updates if current time > ts in update column (prevents overwriting by delayed updates)

### 2.1. PostgreSQL Cluster

Before the test setup is startable, a local postgresql cluster will be set up using docker containers. How many nodes will be started is configurable inside `sysconfig.json` (['system']['networks'][0]['config']['scale']['max_nodes']).

#TODO: add base architectural diagram, 3 node setup (visio)

### 2.2. Cluster Orchestration

The orchestrator runs on the "host" using JSON-RPC to communicate with each docker container (node) after the nodes have been started.
(this could have been done by direct postgresql port 5432 communication; to build a clean abstracted OOP model on the container node(s) encapsulation via JSON-RPC and the python-microesb have been chosen).

The orchestration model allows adding a single node after each other (**not** multiple at once) to allow later up/down scaling (used in the SDMI project).

#TODO: add architectural JSON-RPC overview (visio)

### 2.3. Test Setup

After the cluster orchestration (setup) has been completed successfully the tests can be run.

#TODO: add architectural diagram, showing detailed load balancing (visio)

The following tests exist and must be started in the given order:

1. Insert test (`test-insert.py`)
2. Update test (`test-update.py`)
3. Select test (`test-select.py`)

> [!WARNING]
> To restart the tests, DELETE all rows from table1 or restart the orchestrator (after stopping all containers)

#TODO: describe each test (moderately)

## 3. OOP Model

The OOP models quality used inside each container node is modeled by python-microesb which allows fine grained (clean code) modeling and
is considered *production-ready* whereas the codes quality in `orchestrator.py` is limited (*fast time to market* was the directive).

## 4. Hwoto Run Tests

```bash
cd ./example/01-logical-replication
./docker-build.sh
python3 orchestrator.py
```
