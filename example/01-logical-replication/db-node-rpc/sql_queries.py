init_roles = '''
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator';
CREATE ROLE testreader WITH LOGIN PASSWORD 'testreader';
CREATE ROLE testwriter WITH LOGIN PASSWORD 'testwriter';
'''

create_table = '''
CREATE TABLE {table_name} (
 {table_columns}
);

SELECT setval('{table_name}_id_seq', {table_seq_start}, true);

GRANT USAGE ON SCHEMA public TO replicator;
GRANT SELECT ON TABLE {table_name} TO replicator;
GRANT SELECT ON TABLE {table_name} TO testreader;
GRANT INSERT ON TABLE {table_name} TO testwriter;
GRANT ALL ON {table_name}_id_seq TO testwriter;
'''

table_upd_ts_trigger = '''
CREATE FUNCTION upd_ts_trigger_{table_name}()
RETURNS trigger LANGUAGE plpgsql AS
$$BEGIN
  NEW.modified_ts := current_timestamp;
  RETURN NEW;
END;$$;

CREATE TRIGGER "00_upd_ts_triger_{table_name}"
  BEFORE UPDATE ON {table_name}
FOR EACH ROW EXECUTE PROCEDURE upd_ts_trigger_{table_name}();

CREATE FUNCTION check_{table_name}_update_ts()
RETURNS TRIGGER LANGUAGE plpgsql AS
$$BEGIN
  IF NEW.modified_ts > OLD.modified_ts THEN
    RETURN NEW;
  ELSE
    RETURN OLD;
  END IF;
END;$$;

CREATE TRIGGER "01_check_{table_name}_update_ts"
  BEFORE UPDATE ON {table_name}
  FOR EACH ROW
  WHEN (OLD.* IS DISTINCT FROM NEW.*)
  EXECUTE FUNCTION check_{table_name}_update_ts();
'''

create_publication = '''
CREATE PUBLICATION {publication_id} FOR TABLE {table_name};
'''

create_subscription = '''
CREATE SUBSCRIPTION {subscription_id} CONNECTION 'host={host_ip} dbname=lb-test user=replicator port=5432' PUBLICATION {publication_id} WITH (copy_data = false, origin = none);
'''
