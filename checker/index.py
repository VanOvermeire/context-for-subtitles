import boto3

from helpers import stepfunction_helper

tr_client = boto3.client('transcribe')


def my_handler(event, context):
    result = False
    job_id, transcription_name = stepfunction_helper.get_job_id_and_name(event)
    response = tr_client.get_transcription_job(TranscriptionJobName=transcription_name)
    print('Found transcription job: ' + str(response) + ' for job name ' + str(transcription_name))

    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        print('Job was completed successfully.')
        result = True
    elif response['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
        print('Job failed. For more information see: ' + str(response['TranscriptionJobSummaries']))
        raise Exception('Transcription job failed.')

    return '' + str(result)
