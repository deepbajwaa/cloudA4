import boto3
import json

# Name: Simrandeep Bajwa
# Student ID: 1040216
# Email: sbajwa05@uoguelph.ca
# Assignment: #4

s3 = boto3.client('s3')
s3_res = boto3.resource('s3')

# This function checks if a bucket exists within the user's s3 space
def check_if_bucket_exists(bucket_name):
    return (s3_res.Bucket(bucket_name) in s3_res.buckets.all())

# This function checks if a file exists on s3
def check_if_file_exists_s3(bucket_name, filename):
    # Check if the given file exists within the specifed bucket
    try:    
        for object in s3_res.Bucket(bucket_name).objects.all():
            if (filename == object.key.strip("/")):
                return True
    except Exception as e:
        return False

    return False

def lambda_handler(event, context):
    try:
        bucket = event['queryStringParameters']['bucket']
        filename = event['queryStringParameters']['filename']
    except Exception as e:
        print(e)
        error_msg = 'Missing \'bucket\' and \'filename\' parameters from request!'
        print(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
    
    # Check if the bucket exists
    if not check_if_bucket_exists(bucket):
        return_msg = "The bucket: \'{}\' does not exist within your s3 space!".format(bucket)
        print(return_msg)
        return {
            'statusCode': 200,
            'body': json.dumps(return_msg)
        }

    # Check if the file exists
    if not check_if_file_exists_s3(bucket, filename):
        return_msg = "The file: \'{}\' does not exist within the bucket: \'{}\'".format(filename, bucket)
        print(return_msg)
        return {
            'statusCode': 200,
            'body': json.dumps(return_msg)
        }
    
    # Get the link to download the file specified by the user
    try:
        download_url = s3.generate_presigned_url(
            'get_object',
            Params = {'Bucket': bucket, 'Key': filename},
            ExpiresIn = 3600
        )
    except Exception as e:
        print(e)
        error_msg = 'Could not retreive the bucket: \'{}\' and file: \'{}\''.format(bucket, filename)
        print(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
    
    # Return a response with the download link
    print("download_url: ", download_url)
    return {
        'statusCode': 200,
        'body': json.dumps(download_url)
    }