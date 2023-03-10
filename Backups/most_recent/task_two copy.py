import urllib.parse
import boto3
from datetime import datetime
import json

# Name: Simrandeep Bajwa
# Student ID: 1040216
# Email: sbajwa05@uoguelph.ca
# Assignment: #4

s3 = boto3.client('s3')
s3_res = boto3.resource('s3')

def create_logfile(users):
    log_filename = datetime.now().strftime("%Y-%m-%d;%H;%M;%S") + ".txt"

    # Create the log
    log = 'Copied the file: \'{}\' to the following users: \n'

    for user in users:
        bucket_name = "cis4010-a4-task-two-sbajwa05-" + user.lower()
        log += 'User: \'{}\' with the Bucket Name: \'{}\'\n'.format(user, bucket_name)

    s3.put_object(Body=log, Bucket="sbajwa05-test-two", Key=log_filename)

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    except Exception as e:
        error_msg = 'Error retreiving the bucket name and file name from the request!'
        print(error_msg)
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
    
    # Get the distribution list from a pre existing bucket
    try:
        response = s3.get_object(Bucket='sbajwa05-test-two', Key='distribution-list.txt')
        file = response['Body'].read().decode('utf-8').split("\r\n")
    except Exception as e:
        error_msg = 'Could not retrieve the distribution list (should be located at the root of the bucket: \'sbajwa05-test-two\' with the filename: \'distribution-list.txt\')!'
        print(error_msg)
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
    
    # Put the newly uploaded file into the bucket of each user on the distribution list
    try:
        users = []

        for name in file:
            bucket_name = "cis4010-a4-task-two-sbajwa05-" + name.lower()
            print("The file: \'{}\' is being sent to the user: \'{}\' (bucket name: \'{}\')".format(key, name, bucket_name))
            print("bucket name: {}".format(bucket))

            if s3_res.Bucket(bucket_name) in s3_res.buckets.all():
                s3.copy_object(Bucket=bucket_name, Key=key, CopySource={'Bucket': bucket,'Key': key})
            else:
                s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
                s3.copy_object(Bucket=bucket_name, Key=key, CopySource={'Bucket': bucket,'Key': key})
            users.append(name)

        create_logfile(users)
        return {
            'statusCode': 200,
            'body': json.dumps(response['ContentType'])
        }
    except Exception as e:
        error_msg = 'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket)
        print(error_msg)
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
    