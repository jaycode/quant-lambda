# Convert xlsb and xlsx to xls for further processing.
import urllib.parse
import boto3
# import pyexcel as pe
import openpyxl as opx
import os
import io
from log_helper import *

s3 = boto3.client('s3')

def read_object(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    except Exception as e:
        logger.error(e)
        log_err('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

def lambda_handler(event, context):
    if 'Records' in event:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key'],
            encoding='utf-8')
        
        wb = opx.load_workbook(io.BytesIO(read_object(bucket, key)), read_only=True)
        sheet_names = wb.sheetnames
        return sheet_names
    else:
        return event
