
S3_NEW_JOB_FOLDER = 'new-transcription-names/'


def extract_bucket_and_key_from_event(event):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    return bucket, key


def get_object_as_string(client, bucket, key):
    s3_object = client.get_object(Bucket=bucket, Key=key)
    s3_object = s3_object['Body'].read()
    return s3_object.decode('utf-8')
