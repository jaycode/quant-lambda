# Quant-Lambda Project

## Initialization

1. RDS needs security group that has self-reference so lambda can connect to it.
2. Lambda role requires the following policies:
  - AmazonS3ReadOnlyAccess
  - AmazonRDSDataFullAccess
  - AWSLambdaVPCAccessExecutionRole
3. Lambda needs to be in the same VPC, subnet, and has the same security group as the RDS instance.
4. Lambda uses Python 3.7, blueprint name "s3-get-object-python".
5. We can upload our own packages to AWS lambda along with our lambda function.
6. Install psycopg2 module from [here](https://github.com/jkehler/awslambda-psycopg2).
7. Environment variables for database:
  - ENDPOINT='your-database-endpoint'
  - PORT='your-database-port'
  - DBUSER='your-database-user'
  - DBPASSWORD='your-database-user-password'
  - DATABASE='your-database-name'
  These values can be found on the RDS detail page.

## Development Process

1. Update `lambda_function.py`
2. Install additional modules with `pip install -t ./layers/module-layer/python module_name`.
3. Go to ./project directory (i.e. this directory)
4. Update and run `./zip.sh`. This function will create/update `function.zip` and other aws layers in the `layers` directory.
5. If adding new layers, create new layers on AWS and upload them there, then use these layers in the lambda function.
6. Upload `function.zip` to lambda function by setting "Code entry type" to "Upload a .zip file" then upload the file.


## PgAdmin
See the guide [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html).

To connect with local PgAdmin, make sure to first add an inbound rule in the security group with the computer's IP.

**IMPORTANT:** Get the computer's IP from [here](https://ipinfo.info/html/privacy-check.php) from cell **HTTP_X_FORWARDED_FOR**. RDS does not accept the incoming inbound from REMOTE_ADDR.

## Troubleshooting

### Timeouts

Symptom: Lambda timeouts when accessing RDS instance.

Fix: Usually caused by Lambda not being able to access the RDS instance. Make sure `AWSLambdaVPCAccessExecutionRole` is attached to Lambda role and the function is in the same VPC, subnet, and has the same security group as the RDS instance.

### Lambda under VPC cannot access S3

Symptom: Lambda instance under VPC can access RDS but cannot access S3.

Fix: The VPC needs to have an Endpoint. Go to VPC > Endpoints then add an endpoint with service "com.amazonaws.us-east-1.s3".

## References
1. Self-reference for RDS: https://docs.aws.amazon.com/glue/latest/dg/setup-vpc-for-glue-access.html
2. To install own dependencies in AWS lambda: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-dependencies
3. To query aws database from serverless application: https://aws.amazon.com/blogs/database/query-your-aws-database-from-your-serverless-application/
  - The key takeaway here is that we can use `psycopg2` to connect to PostgreSQL server. However, please install manually from [here](https://github.com/jkehler/awslambda-psycopg2).
  - The post has a Github link to the [sample code](https://github.com/awslabs/rds-support-tools/blob/master/serverless/serverless-query.py.postgresql) we can use as a reference.
  - However, we do not need to use more advanced security systems like KMS or cloudformation infrastructure to automatically set db credentials on deployment. Instead, we simply update the environment variables through the Lambda console interface (explained in the next item).
4. To store database credentials in environment variables: https://www.concurrencylabs.com/blog/configure-your-lambda-function-like-a-champ-sail-smoothly/

