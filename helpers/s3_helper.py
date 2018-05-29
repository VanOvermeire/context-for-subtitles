from helpers import transcribe_helper


S3_NEW_DATA_FOLDER = 'data/'
S3_NEW_JOB_FOLDER = 'new-transcription-names/'
S3_RESULTS_FOLDER = 'results/'


def extract_bucket_and_key_from_event(event):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    return bucket, key


def get_object_as_string(client, bucket, key):
    s3_object = client.get_object(Bucket=bucket, Key=key)
    s3_object = s3_object['Body'].read()
    return s3_object.decode('utf-8')


def generate_key_for_combine_result(transcription_name):
    if transcribe_helper.TRANSCRIPTION_PREFIX not in transcription_name:
        return S3_RESULTS_FOLDER + transcription_name
    return S3_RESULTS_FOLDER + transcription_name.split(transcribe_helper.TRANSCRIPTION_PREFIX)[1]
