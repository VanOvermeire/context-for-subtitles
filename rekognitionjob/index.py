import os
import boto3
from helpers import transcribe_helper, rekognition_helper, sns_helper

s3_client = boto3.client('s3')
rek_client = boto3.client('rekognition')


def my_handler(event, context):
    bucket, key = sns_helper.extract_bucket_and_key(event)
    extension = transcribe_helper.get_extension(key)

    if extension is not None:
        celeb_job_name = rekognition_helper.generate_job_tag(key, 'celeb')

        video = {'S3Object': {'Bucket': bucket, 'Name': key}}

        celeb_response = rek_client.start_celebrity_recognition(
            Video=video,
            NotificationChannel={
                'SNSTopicArn': os.environ['CELEB_SNS'],
                'RoleArn': os.environ['REK_ROLE']
            },
            JobTag=celeb_job_name
        )

        celeb_job_id = celeb_response['JobId']
        tr_job_name = transcribe_helper.get_transcribe_job_name(key)

        print('Celeb id is ' + celeb_job_id + ', and transcribe job name is ' + tr_job_name)

        s3_key, s3_data = rekognition_helper.generate_s3_key_and_data(celeb_job_id, tr_job_name)
        print('Saving our job data under ' + s3_key + ' in bucket ' + bucket)
        s3_client.put_object(Body=s3_data, Bucket=bucket, Key=s3_key)
    else:
        print('No valid extension detected, ignoring file.')

    return {
        'message': 'Finished handling job'
    }
