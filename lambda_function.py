import json
import urllib.parse
import boto3
from pyexcel_xlsx import get_data
import psycopg2
import logging
from os import environ
import traceback

print('Loading function')

s3 = boto3.client('s3')

endpoint=environ.get('ENDPOINT')
port=environ.get('PORT')
dbuser=environ.get('DBUSER')
password=environ.get('DBPASSWORD')
database=environ.get('DATABASE')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def make_connection():
    conn_str="host={0} dbname={1} user={2} password={3} port={4}".format(
        endpoint,database,dbuser,password,port)
    logger.info(conn_str)
    conn = psycopg2.connect(conn_str)
    conn.autocommit=True
    return conn 


def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg , "headers": {}, "statusCode": 400,
        "isBase64Encoded":"false"}

logger.info("Cold start complete.") 

def execute_query(query):
    try:
        cursor.execute(query)
    except:
        return log_err ("ERROR: Cannot execute cursor.\n{}".format(
            traceback.format_exc()) )

    try:
        results_list=[]
        for result in cursor: results_list.append(result)
        print(results_list)
        cursor.close()

    except:
        return log_err("ERROR: Cannot retrieve query data.\n{}".format(
            traceback.format_exc()))

def lambda_handler(event, context):
    logger.info("HELLO")
    logger.info("Received event: " + json.dumps(event, indent=2))

    try:
        cnx = make_connection()
        cursor=cnx.cursor()

        logger.info('Connected!')

        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            logger.info("CONTENT TYPE: " + response['ContentType'])
            
            
            return response['ContentType']
        except Exception as e:
            logger.error(e)
            log_err('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
            raise e

        # return {"body": str(results_list), "headers": {}, "statusCode": 200,
        # "isBase64Encoded":"false"}

    except:
        return log_err("ERROR: Cannot connect to database from handler.\n{}".format(
            traceback.format_exc()))