import boto3

# Name: Simrandeep Bajwa
# Student ID: 1040216
# Email: sbajwa05@uoguelph.ca
# Assignment: #4

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # bucket = event['params']['querystring']['bucket']
    # filename = event['params']['querystring']['filename']
    
    try:
        bucket = event['bucket']
        filename = event['filename']
    except Exception as e:
        return {
            'statusCode': 200,
            'error': 'Missing \'bucket\' and \'filename\' parameters from request!'
        }
    
    # Get the link to download the file specified by the user
    try:
        download_url = s3.generate_presigned_url(
            'get_object',
            Params = {'Bucket': bucket, 'Key': filename},
            ExpiresIn = 3600
        )
    except Exception as e:
        return {
            'statusCode': 200,
            'error': 'Could not retreive the bcuket: {} and file: {}'.format(bucket, filename)
        }
    
    # Return a response with the download link
    return {
            'statusCode': 200,
            'download_url': download_url
        }
