# Precise Replication Order

| NodeID  | SrcNode | Function            | ProcOn | Command                       |
| ------- | ------- | ------------------- | ------ | ----------------------------- |
| Node1   | node1   | create_publication  | node   | create pub 'pub-node1-table1' |
| Node2   | node2   | create_publication  | node   | create pub 'pub-node2-table1' |
|         | node2   | subscribe_to_others | node   | create sub 'sub-node1-table1' |
|         | node1   | subscribe_to_node   | orch   | create sub 'sub-node2-table1' |
| Node3   | node3   | create_publication  | node   | create pub 'pub-node3-table1' |
|         | node3   | subscribe_to_others | node   | create sub 'sub-node2-table1' |
|         | node3   | subscribe_to_others | node   | create sub 'sub-node1-table1' |
|         | node2   | subscribe_to_node   | orch   | create sub 'sub-node3-table1' |
|         | node1   | subscribe_to_node   | orch   | create sub 'sub-node3-table1' |
