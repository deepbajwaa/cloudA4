import boto3
import json

# Name: Simrandeep Bajwa
# Student ID: 1040216
# Email: sbajwa05@uoguelph.ca
# Assignment: #4

s3 = boto3.client('s3')
s3_res = boto3.resource('s3')

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
    # bucket = event['params']['querystring']['bucket']
    # filename = event['params']['querystring']['filename']

    try:
        # bucket = event['bucket']
        # filename = event['filename']
        bucket = event['queryStringParameters']['bucket']
        filename = event['queryStringParameters']['filename']
    except Exception as e:
        print(e)
        return 'Missing \'bucket\' and \'filename\' parameters from request!'
    
    # Check if the file exists
    if not check_if_file_exists_s3(bucket, filename):
        return "The file: \'{}\' does not exist within the bucket: \'{}\'".format(filename, bucket)
    
    # Get the link to download the file specified by the user
    try:
        download_url = s3.generate_presigned_url(
            'get_object',
            Params = {'Bucket': bucket, 'Key': filename},
            ExpiresIn = 3600
        )
    except Exception as e:
        print(e)
        return 'Could not retreive the bucket: \'{}\' and file: \'{}\''.format(bucket, filename)
    
    # Return a response with the download link
    print("download_url: ", download_url)
    # return_block = {}
    # return_block['statusCode'] = 200
    # return_block['download_url'] = download_url
    return {
        'statusCode': 200,
        'body': json.dumps(download_url)
    }
    # return JSON.stringify(return_block)
    # return download_url