import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
s3_res = boto3.resource('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    distribution_list = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # hardcoded the location to the distribution list (this can be put anywhere you want)
        response = s3.get_object(Bucket=bucket, Key=distribution_list)
        file = response['Body'].read().decode('utf-8').split(" ")
        
        # create a unique name for a bucket associated with each name within the distribution list and put the object into that users bucket
        # you probably first want to verify if the bucket exists before you attempt to create a bucket
        
        
        for name in file:
            bucket_name = name + "_cis4010_a4_task_two_sbajwa05"
            if s3_res.Bucket(bucket_name) in s3_res.buckets.all() :
                s3.put_object(Bucket=bucket_name, Key=key)
            
        return "response"
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(distribution_list, bucket))
        raise e
              