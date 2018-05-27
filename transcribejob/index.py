import boto3
from helpers import s3_helper, transcribe_helper

s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')


def my_handler(event, context):
    bucket, key = s3_helper.extract_bucket_and_key_from_event(event)
    extension = transcribe_helper.get_extension(key)
    file_uri = transcribe_helper.generate_file_uri(bucket, key)

    # settings = {'ShowSpeakerLabels': 'true', 'MaxSpeakerLabels': '10'}
    media_info = {'MediaFileUri': file_uri}

    job_name = 'tr-job-for-' + extension  # random suffix would make sure you can submit a video multiple times

    if extension is not None:
        response = transcribe_client.start_transcription_job(TranscriptionJobName=job_name, LanguageCode='en-US', MediaFormat=extension,
                                                             Media=media_info)
        print('Started transcribe job. Got back ' + str(response))
    else:
        print('No valid extension detected, ignoring file.')

    return {
        'message': 'started job for name ' + job_name
    }
