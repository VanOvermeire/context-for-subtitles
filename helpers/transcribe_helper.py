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
    key = key[0:key.rfind(".")]
    return TRANSCRIPTION_PREFIX + key
