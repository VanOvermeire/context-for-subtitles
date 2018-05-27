import os
import boto3
from helpers import s3_helper

s3_client = boto3.client('s3')
rek_client = boto3.client('rekognition')


def my_handler(event, context):
    bucket, key = s3_helper.extract_bucket_and_key_from_event(event)
    job_name = 'rek-job-for-' + key

    # TODO use ClientRequestToken
    response = rek_client.start_celebrity_recognition(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        NotificationChannel={
            'SNSTopicArn': os.environ['REK_SNS'],
            'RoleArn': os.environ['REK_ROLE']
        },
        JobTag=job_name
    )

    print('Job id is ' + response['JobId'])

    return {
        'message': 'started job for ' + job_name
    }
