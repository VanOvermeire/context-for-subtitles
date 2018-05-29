import boto3

from helpers import stepfunction_helper

tr_client = boto3.client('transcribe')


def my_handler(event, context):
    result = False
    job_id, transcription_name = stepfunction_helper.get_job_id_and_name(event)

    response = tr_client.get_transcription_job(TranscriptionJobName=transcription_name)
    print('Got back response: ' + str(response))

    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        result = True

    return '' + str(result)
