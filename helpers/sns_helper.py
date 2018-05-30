import json


def extract_job_id(event):
    sns = event["Records"][0]['Sns']['Message']
    sns_message = json.loads(sns)
    job_id = sns_message["JobId"]
    return job_id


def extract_bucket_and_key(event):
    sns = event["Records"][0]['Sns']['Message']
    sns_message = json.loads(sns)
    s3 = sns_message['Records'][0]['s3']
    bucket = s3['bucket']['name']
    key = s3['object']['key']

    return bucket, key
