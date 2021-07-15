import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def create_connection():
    """ 
    Connect to the PostgreSQL database server 
    
    """
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database')
        conn = psycopg2.connect("host=pg_container dbname=cargill_db user=cargill password=cargill")
        conn.set_session(autocommit=True)

        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
    
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_connection(cur, conn):
    """ 
    Close the connection with PostgreSQL database server 
    """
    try:
        cur.close()
        if conn is not None:
            conn.close()
            print('Database connection closed')                        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def drop_tables(cur, conn):
    """
    This method will Drop each table using the queries in drop_table_queries list.
    """    
    for query in drop_table_queries:
        print(f"Executing: {query}")
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This method will Create each table using the queries in create_table_queries list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()        