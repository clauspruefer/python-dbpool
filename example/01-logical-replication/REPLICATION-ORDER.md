# Precise Replication Order

| NodeID  | SrcNode | Function            | ProcOn | Command                             |
| ------- | ------- | ------------------- | ------ | ----------------------------------- |
| Node0   | node0   | create_publication  | node   | create pub 'pub_node0_table1'       |
| Node1   | node1   | create_publication  | node   | create pub 'pub_node1_table1'       |
|         | node1   | subscribe_to_others | node   | create sub 'sub_node1_node0_table1' |
|         | node0   | subscribe_to_node   | orch   | create sub 'sub_node0_node1_table1' |
| Node2   | node2   | create_publication  | node   | create pub 'pub_node2_table1'       |
|         | node2   | subscribe_to_others | node   | create sub 'sub_node2_node1_table1' |
|         | node2   | subscribe_to_others | node   | create sub 'sub_node2_node0_table1' |
|         | node1   | subscribe_to_node   | orch   | create sub 'sub_node1_node2_table1' |
|         | node0   | subscribe_to_node   | orch   | create sub 'sub_node0_node2_table1' |
