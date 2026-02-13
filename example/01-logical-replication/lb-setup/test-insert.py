from pgdbpool import pool
import dbconfig

pool.Connection.init(dbconfig.config)

for i in range(0, 200):

    with pool.Handler('writer1') as db1:
        db1.query("INSERT INTO table1 (col1, col2) VALUES ('test1', 'test2')")
        db1.query("INSERT INTO table1 (col1, col2) VALUES ('test3', 'test4')")

    with pool.Handler('writer2') as db2:
        db2.query("INSERT INTO table1 (col1, col2) VALUES ('test100', 'test200')")
        db2.query("INSERT INTO table1 (col1, col2) VALUES ('test300', 'test400')")
