init_db = '''
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_senders = 10;

CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator';
'''

create_table = '''
CREATE TABLE {tablename} (
{tablecolumns}
);
'''
