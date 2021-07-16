import psycopg2
import pandas as pd
from sql_queries import create_table_queries, drop_table_queries, insert_table_queries, update_identifier


def create_connection(params):
    """
     create a new connection with the postgreSQL 
     database and return the cur and conn object

    :param params: connection string   

    """
    conn = None
    try:
        print('Connecting to the PostgreSQL database')
        conn = psycopg2.connect(**params)
        conn.set_session(autocommit=True)

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)
    
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_connection(cur, conn):
    """
     close the connection with the postgreSQL database     

    :param cur: cursor
    :param conn: connection object

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
     drop all the tables in the example     

    :param cur: cursor
    :param conn: connection object

    """

    for query in drop_table_queries:
        print(f"Executing: {query}")
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
     create all the tables in the example     

    :param cur: cursor
    :param conn: connection object

    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    print("Tables created")

def pg_to_pd(cur, query, columns):
    """
     return the select result as panda dataframe

    :param cur: cursor
    :param query: SELECT query string
    :param columns: columns name in the select

    """
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        return 1
        
    tupples = cur.fetchall()
    

    df = pd.DataFrame(tupples, columns=columns)
    return df


def insert_all(cur, conn):
    """
     Insert all the test records in the tables

    :param cur: cursor
    :param conn: connection object

    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
    print("Records were inserted")        

def update(cur, conn, table, params):
    """
     Insert all the test records in the tables

    :param cur: cursor
    :param conn: connection object
    :param table: index to search the query string into the dictionary to update

    """

    query = update_identifier[table]    
    cur.execute(query, params)
    conn.commit()
    print("Table updated")
