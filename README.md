# Datawarehousing final project 


## Setting up an Amazon Relational Database (RDS)

First we need to create a database instance on [Amazon RDS](https://aws.amazon.com/es/rds/). This requires an Amazon AWS account. Once the account is setup the following steps are required:

1. Choose *DB Instances*
2. Click *Create Database*
3. Choose *MariaDB* as the Engine option
4. Choose version 10.2.21
5. Choose the *free tier* template
6. Choose the identifier for the database
7. Setup credentials. **Remember them!**
8. Create database

After the database instance is created we need to open the access to it!

## Creating a Lambda function

1. Upload the deployment package provided (zipped folder)

## Creating a Cloudwatch Event