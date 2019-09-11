import boto3
import os
import json

def lambda_handler(event, context):
    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn=os.environ.get('ARN_TO_RUN'),
        input=json.dump(event)
    )
    return True
