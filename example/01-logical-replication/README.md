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

The example creates a multi-node PostgreSQL cluster with logical replication, where each node acts as both a publisher and subscriber. This enables a multi-master topology where writes can be distributed across nodes and automatically synchronized.
