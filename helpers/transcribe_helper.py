def get_extension(key):
    key_parts = key.split('.')
    last_part = key_parts[len(key_parts) - 1]

    if last_part in ('mp3', 'mp4', 'wav', 'flac'):
        return last_part

    return None


def generate_file_uri(region, bucket, key):
    return 'https://s3-' + region + '.amazonaws.com/' + bucket + '/' + key


def generate_s3_key_and_data(celeb_job_id, people_job_id, transcribe_job_name):
    key = 'new-transcription-names/' + celeb_job_id
    data = 'PEOPLE_JOB_ID=' + people_job_id + ',TRANSCRIBE_JOB_NAME=' + transcribe_job_name

    return key, data


def get_transcribe_job_name(key):
    key = key[0:key.rfind(".")]
    return 'tr-job-' + key
