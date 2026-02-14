import threading
import time

from pgdbpool import pool
import dbconfig

pool.Connection.init(dbconfig.config)

def reader1():
    for i in range (0, 50):
        with pool.Handler('reader1') as db1:
            db1.query("SELECT * FROM table1 WHERE id between 1 AND 100000")
            time.sleep(0.1)

def reader2():
    for i in range (0, 80):
        with pool.Handler('reader2') as db1:
            db1.query("SELECT * FROM table1 WHERE id > 100000")
            time.sleep(0.2)

def reader3():
    for i in range (0, 150):
        with pool.Handler('reader1') as db1:
            db1.query("SELECT * FROM table1")
            time.sleep(0.1)

t1 = threading.Thread(target=reader1)
t2 = threading.Thread(target=reader2)
t3 = threading.Thread(target=reader3)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
