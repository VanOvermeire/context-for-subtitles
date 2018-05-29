import os

import boto3
from urllib.request import urlopen
from helpers import combine_helper, s3_helper, stepfunction_helper

rek_client = boto3.client('rekognition')
tr_client = boto3.client('transcribe')
s3_client = boto3.client('s3')


def my_handler(event, context):
    job_id, transcription_name = stepfunction_helper.get_job_id_and_name(event)

    celeb_response = rek_client.get_celebrity_recognition(JobId=job_id)

    transcription_response = tr_client.get_transcription_job(TranscriptionJobName=transcription_name)
    tr_file_uri = transcription_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    tr_data_as_bytes = urlopen(tr_file_uri).read()
    tr_data_as_string = tr_data_as_bytes.decode('utf-8')

    combine_result = combine_helper.combine_transcribe_and_rekognition(tr_data_as_string, celeb_response)
    key = s3_helper.generate_key_for_combine_result(transcription_name)

    s3_client.put_object(Body=combine_result, Bucket=os.environ['BUCKET'], Key=key)

    return {
        'message': 'Finished combining data.'
    }
