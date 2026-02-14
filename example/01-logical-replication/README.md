# DB-Pool Example Logical Replication

This example demonstrates how the python-dbpool module works with multiple a) write and b) read configurations.
Additionally it introduces a minimal docker orchestration mechanism which configures a running 'logical replicated' postgresql environment consisting of a test-table replicated to multiple postgresql docker nodes.

The setup configures a 'static' set of postgresql nodes which afterwards will be used to run all load-balancing tests. The setup (needs only slight modifications) is prepared to be extended for using runtime adding and removing nodes dynamically (scale up/down).

To demonstrate encapsulated menagement control channel communications used as prototype in our SDMI (Simple Docker Management Instrumentation) project, communication between host (orchestrator) and the docker containers has been implemented as non-direct-postgresql communication using a json-rpc-socket communication protocol between host and docker nodes.

## Architecture

#TODO: add description and architectural overview diagram(s)

## OOP Abstraction

The OOP abstraction model inside the docker container(s) has been ... by using the python-microesb ...

The orchestrator code insode `orchestrator.py` (due to time aspects) is still quite spaghetti-like and will also be abstracted (see SDMI project) with python-microesb.

