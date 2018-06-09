import json
from urllib.request import urlopen

TRANSCRIPTION_PREFIX = 'tr-job-'


def get_extension(key):
    key_parts = key.split('.')
    last_part = key_parts[len(key_parts) - 1]

    if last_part in ('mp3', 'mp4', 'wav', 'flac'):
        return last_part

    return None


def generate_file_uri(region, bucket, key):
    return 'https://s3-' + region + '.amazonaws.com/' + bucket + '/' + key


def get_transcribe_job_name(key):
    key = key[key.rfind("/") + 1:key.rfind(".")]

    return TRANSCRIPTION_PREFIX + key


def get_transcribe_data(transcription_response):
    tr_file_uri = transcription_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    tr_data_as_bytes = urlopen(tr_file_uri).read()
    tr_data_as_string = tr_data_as_bytes.decode('utf-8')

    return json.loads(tr_data_as_string)
