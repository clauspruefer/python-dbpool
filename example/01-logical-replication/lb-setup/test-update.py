import threading
import time

from pgdbpool import pool
import dbconfig

pool.Connection.init(dbconfig.config)

with pool.Handler('writer1') as db1:
    db1.query("INSERT INTO table1 (id, col1, col2) VALUES (1235433221, 'update1', 'update2')")
    db1.query("INSERT INTO table1 (id, col1, col2) VALUES (1235433241, 'update3', 'update4')")

with pool.Handler('writer2') as db1:
    db1.query("INSERT INTO table1 (id, col1, col2) VALUES (1235433261, 'update5', 'update6')")
    db1.query("INSERT INTO table1 (id, col1, col2) VALUES (1235433281, 'update7', 'update8')")


def updater1():
    for i in range (0, 20):
        with pool.Handler('writer1') as db1:
            db1.query("UPDATE table1 SET col1='update1-new-t1-{}' WHERE id = 1235433221".format(i))
            time.sleep(0.1)

def updater2():
    for i in range (0, 40):
        with pool.Handler('writer2') as db1:
            db1.query("UPDATE table1 SET col1='update1-new-t2-{}' WHERE id = 1235433221".format(i))
            time.sleep(0.2)

def updater3():
    for i in range (0, 15):
        with pool.Handler('writer1') as db1:
            db1.query("UPDATE table1 SET col1='update1-new-t3-{}' WHERE id = 1235433221".format(i))
            time.sleep(0.8)

t1 = threading.Thread(target=updater1)
t2 = threading.Thread(target=updater2)
t3 = threading.Thread(target=updater3)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
