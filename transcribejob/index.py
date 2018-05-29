import os
import boto3
from helpers import s3_helper, transcribe_helper

s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')


def my_handler(event, context):
    bucket, key = s3_helper.extract_bucket_and_key_from_event(event)
    extension = transcribe_helper.get_extension(key)
    file_uri = transcribe_helper.generate_file_uri(os.environ['REGION'], bucket, key)

    media_info = {'MediaFileUri': file_uri}

    job_name = transcribe_helper.get_transcribe_job_name(key)

    if extension is not None:
        transcribe_client.start_transcription_job(TranscriptionJobName=job_name, LanguageCode='en-US', MediaFormat=extension, Media=media_info)
    else:
        print('No valid extension detected, ignoring file.')

    return {
        'message': 'started job for name ' + job_name
    }
