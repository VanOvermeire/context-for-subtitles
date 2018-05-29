import os
import boto3
from helpers import combine_helper, s3_helper, stepfunction_helper, transcribe_helper

rek_client = boto3.client('rekognition')
tr_client = boto3.client('transcribe')
s3_client = boto3.client('s3')


def my_handler(event, context):
    job_id, transcription_name = stepfunction_helper.get_job_id_and_name(event)

    celebrity_response = rek_client.get_celebrity_recognition(JobId=job_id)

    transcription_response = tr_client.get_transcription_job(TranscriptionJobName=transcription_name)
    transcription_response_as_string = transcribe_helper.get_transcribe_data(transcription_response)

    combine_result = combine_helper.combine_transcribe_and_rekognition(transcription_response_as_string, celebrity_response)
    key = s3_helper.generate_key_for_combine_result(transcription_name)

    s3_client.put_object(Body=combine_result, Bucket=os.environ['BUCKET'], Key=key)

    return {
        'message': 'Finished combining data.'
    }
