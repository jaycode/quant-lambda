import os
import boto3

def get_keys(s3client, prefix):
	keys = []
	objects = s3client.list_objects_v2(
		Bucket=os.environ.get('BUCKET'),
		Prefix=prefix
	)
	if len(objects['Contents']) > 1:
		keys = list(map(lambda c: c['Key'], objects['Contents'][1:]))
	return keys

def lambda_handler(event, context):
	access = "DIRECT"
	
	# Access through Trigger
	if 'Records' in event and len(event['Records']) > 0:
		if 'eventVersion' in event['Records'][0]:
			access = "TRIGGER"
	else:
		# todo: Reload all tables. Read documents from S3.
		s3client = boto3.client('s3')
		keys = []
		
		keys += get_keys(s3client, 'data/ownership_structures/')
		keys += get_keys(s3client, 'data/local_mf_ownerships/')
		keys += get_keys(s3client, 'data/cash_levels/')
		event = {"Records": []}
		for key in keys:
			event['Records'].append({
				's3': {
					'bucket': {'name': os.environ.get('BUCKET')},
					'object': {
						'key': key
					}
				}
			})
	
	return {
		"DBConnection": {
			"endpoint": os.environ.get('ENDPOINT'),
			"port": os.environ.get('PORT'),
			"dbuser": os.environ.get('DBUSER'),
			"dbpassword": os.environ.get('DBPASSWORD'),
			"database": os.environ.get('DATABASE')	
		},
		"Records": event["Records"] + ["DONE"],
		"Access": access
	}