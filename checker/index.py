import boto3

tr_client = boto3.client('transcribe')


def my_handler(event, context):
    result = False
    transcription_name = event['transcribe-name']

    response = tr_client.get_transcription_job(TranscriptionJobName=transcription_name)
    print('Got back response: ' + str(response))

    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        result = True

    return '' + str(result)
