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
2. Install additional modules with `pip install --target ./package module_name`.
3. Go to ./project directory (i.e. this directory)
4. Run `./zip.sh`. This function will create/update `function.zip`.
5. Upload `function.zip` to lambda function by setting "Code entry type" to "Upload a .zip file".

## Troubleshooting

### Timeouts

Usually caused by Lambda not being able to access the RDS instance. Make sure `AWSLambdaVPCAccessExecutionRole` is attached to Lambda role and the function is in the same VPC, subnet, and has the same security group as the RDS instance.


## References
1. Self-reference for RDS: https://docs.aws.amazon.com/glue/latest/dg/setup-vpc-for-glue-access.html
2. To install own dependencies in AWS lambda: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-dependencies
3. To query aws database from serverless application: https://aws.amazon.com/blogs/database/query-your-aws-database-from-your-serverless-application/
  - The key takeaway here is that we can use `psycopg2` to connect to PostgreSQL server. However, please install manually from [here](https://github.com/jkehler/awslambda-psycopg2).
  - The post has a Github link to the [sample code](https://github.com/awslabs/rds-support-tools/blob/master/serverless/serverless-query.py.postgresql) we can use as a reference.
  - However, we do not need to use more advanced security systems like KMS or cloudformation infrastructure to automatically set db credentials on deployment. Instead, we simply update the environment variables through the Lambda console interface (explained in the next item).
4. To store database credentials in environment variables: https://www.concurrencylabs.com/blog/configure-your-lambda-function-like-a-champ-sail-smoothly/

