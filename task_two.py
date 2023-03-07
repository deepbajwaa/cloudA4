import urllib.parse
import boto3
from datetime import datetime

# Name: Simrandeep Bajwa
# Student ID: 1040216
# Email: sbajwa05@uoguelph.ca
# Assignment: #4


s3 = boto3.client('s3')
s3_res = boto3.resource('s3')

def create_logfile(src_bucket, dest_bucket, key):
    log_filename = datetime.now().strftime("%Y-%m-%d;%H;%M;%S") + ".txt"
    s3.put_object(Body="Copied the file: \'{}\' from source bucket: \'{}\' to destination bucket: \'{}\'\n".format(key, src_bucket, dest_bucket), Bucket=dest_bucket, Key=log_filename)

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    except Exception as e:
        print(e)
        print('Error retreiving the bucket name and file name from the request!')
        raise e
    
    # Get the distribution list from a pre existing bucket
    try:
        response = s3.get_object(Bucket='sbajwa05-test-two', Key='distribution-list.txt')
        file = response['Body'].read().decode('utf-8').split("\r\n")
    except Exception as e:
        print(e)
        print('Could not retrieve the distribution list!')
        raise e
    
    # Put the newly uploaded file into the bucket of each user on the distribution list
    try:
        for name in file:
            print(name)
            bucket_name = "cis4010-a4-task-two-sbajwa05-" + name.lower()
            if s3_res.Bucket(bucket_name) in s3_res.buckets.all():
                s3.copy_object(Bucket=bucket_name, Key=key, CopySource={'Bucket': bucket,'Key': key})
            else:
                s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
                s3.copy_object(Bucket=bucket_name, Key=key, CopySource={'Bucket': bucket,'Key': key})
                
            create_logfile("sbajwa05-test-two", bucket_name, key)

        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
              