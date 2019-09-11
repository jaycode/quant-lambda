import psycopg2
from log_helper import *

def make_connection(endpoint, port, dbuser, password, database):
    conn_str="host={0} dbname={1} user={2} password={3} port={4}".format(
        endpoint,database,dbuser,password,port)
    logger.info(conn_str)
    conn = psycopg2.connect(conn_str)
    conn.autocommit=True
    return conn 

def execute_query(cursor, query, inputs=[], get_result=True):
    try:
        cursor.execute(query, inputs)
    except:
        return log_err ("ERROR: Cannot execute cursor.\n{}".format(
            traceback.format_exc()) )

    if get_result:
        try:
            results_list=[]
            for result in cursor: results_list.append(result)
            
            return results_list
    
        except:
            return log_err("ERROR: Cannot retrieve query data.\n{}".format(
                traceback.format_exc()))
    else:
        return True