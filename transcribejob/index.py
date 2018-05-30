import os
import boto3
from helpers import transcribe_helper, sns_helper

s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')


def my_handler(event, context):
    bucket, key = sns_helper.extract_bucket_and_key(event)
    extension = transcribe_helper.get_extension(key)

    if extension is not None:
        file_uri = transcribe_helper.generate_file_uri(os.environ['REGION'], bucket, key)
        media_info = {'MediaFileUri': file_uri}
        language_code = 'en-US'
        job_name = transcribe_helper.get_transcribe_job_name(key)
        print('Starting job with name ' + str(job_name) + ' and file uri ' + file_uri)

        response = transcribe_client.start_transcription_job(TranscriptionJobName=job_name, LanguageCode=language_code, MediaFormat=extension, Media=media_info)

        print('Started job ' + str(response))
    else:
        print('No valid extension detected, ignoring file.')

    return {
        'message': 'Finished handling job for key ' + key
    }
