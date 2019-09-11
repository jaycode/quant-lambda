import os
import traceback
import queries as q
import io
from db_helper import *

def lambda_handler(event, context):

    try:

        cnx = make_connection(event['DBConnection']['endpoint'],
                              event['DBConnection']['port'],
                              event['DBConnection']['dbuser'],
                              event['DBConnection']['dbpassword'],
                              event['DBConnection']['database'])
        cursor=cnx.cursor()
        logger.info('Connected!')
    except:
        return log_err("ERROR: Cannot connect to database from handler.\n{}".format(
            traceback.format_exc()))

    execute_query(cursor, q.create_views, result=False)
    
    logger.info('Views created!')

    return True