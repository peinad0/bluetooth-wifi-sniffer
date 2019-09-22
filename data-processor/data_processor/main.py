"""Connect to postgres tests."""

import time
import psycopg2


GET_TABLES_STATEMENT = """
SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='openiot'
   AND table_type='BASE TABLE';
"""

TABLE_NAME = 'processed_data_{}'.format(int(time.time()))
CREATE_TABLE_STATEMENT = """
-- Table: openiot.{table_name}

-- DROP TABLE openiot.{table_name};

CREATE TABLE openiot.{table_name}
(
    recvtimets bigint,
    recvtime text COLLATE pg_catalog."default",
    fiwareservicepath text COLLATE pg_catalog."default",
    entityid text COLLATE pg_catalog."default",
    entitytype text COLLATE pg_catalog."default",
    attrname text COLLATE pg_catalog."default",
    attrtype text COLLATE pg_catalog."default",
    attrvalue text COLLATE pg_catalog."default",
    attrmd text COLLATE pg_catalog."default",
    source text COLLATE pg_catalog."default",
    device_id text COLLATE pg_catalog."default",
    instant text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE openiot.{table_name}
    OWNER to postgres;
""".format(table_name=TABLE_NAME)


def statement_insert_data_from_table(table_source):
    """Build insert statement from table."""
    return """
    insert into openiot.{table_name}
    SELECT 
	    *,
	    split_part(attrvalue, ' ', 1) as source,
	    split_part(attrvalue, ' ', 2) as device_id,
	    split_part(attrvalue, ' ', 3) as instant
    from 
	    openiot.{table_source}
    """.format(table_name=TABLE_NAME, table_source=table_source)


def main():
    """Main function."""
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="password",
            host="172.23.0.2",
            port="5432",
            database="postgres"
        )

        cursor = connection.cursor()

        cursor.execute(CREATE_TABLE_STATEMENT)

        cursor.execute(GET_TABLES_STATEMENT)
        record = cursor.fetchall()
        sniffer_tables = []
        for table in record:
            table_name = table[0]
            if table_name.startswith('urn_ngsi_sniffer_'):
                sniffer_tables.append(table_name)

        for sniffer in sniffer_tables:
            cursor.execute(statement_insert_data_from_table(sniffer))

        connection.commit()
        print('Data processed and dumped to %s' % TABLE_NAME)
        print('To search for an identifier, run the following query:')
        print('\tSELECT * FROM openiot.%s WHERE device_id="IDENTIFIER";' % TABLE_NAME)
        #record = cursor.fetchone()
        #print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:  #pylint: disable=broad-except
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()
