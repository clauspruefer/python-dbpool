# Precise Replication Order

| NodeID  | SrcNode | Function          | ProcOn | Command                       |
| ------- | ------- | ----------------- | ------ | ----------------------------- |
| Node1   | node1   | node_pub_self     | node   | create pub 'pub-node1-table1' |
| Node2   | node2   | node_pub_self     | node   | create pub 'pub-node2-table1' |
|         | node2   | node_sub_2others  | node   | create sub 'sub-node1-table1' |
|         | node1   | others_sub_2node  | orch   | create sub 'sub-node2-table1' |
| Node3   | node3   | node_pub_self     | node   | create pub 'pub-node3-table1' |
|         | node3   | node_sub_2others  | node   | create sub 'sub-node2-table1' |
|         | node3   | node_sub_2others  | node   | create sub 'sub-node1-table1' |
|         | node2   | others_sub_2node  | orch   | create sub 'sub-node3-table1' |
|         | node1   | others_sub_2node  | orch   | create sub 'sub-node3-table1' |
