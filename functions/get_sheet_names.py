import urllib.parse
import boto3
import re

# For xls
import xlrd # This is much faster than pyexcel and pandas for reading sheet names
            # without having to load the entire document.
            # see: https://stackoverflow.com/questions/12250024/how-to-obtain-sheet-names-from-xls-files-without-loading-the-whole-file

# For xlsx
import openpyxl as opx

import os
import io
from log_helper import *
from sheet_helper import *

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
        
        sheet_type = check_sheet_type(key)
        if sheet_type == OWNERSHIP_STRUCTURES or \
           sheet_type == LOCAL_MF_OWNERSHIPS:
            sheet_names = []
            if key[-3:].lower() == 'xls':
                xls = xlrd.open_workbook(file_contents=read_object(bucket, key), on_demand=True)
                sheet_names = xls.sheet_names()
            elif key[-4:].lower() == 'xlsx':
                wb = opx.load_workbook(io.BytesIO(read_object(bucket, key)), read_only=True)
                sheet_names = wb.sheetnames

            regex = re.compile(r'^[A-za-z]{3} [0-9]+$')
            sheet_names = [i for i in sheet_names if regex.match(i)]
        elif sheet_type == CASH_LEVELS:
            sheet_names = ['Sheet1']

        return sheet_names + ["DONE"]
    else:
        return event
