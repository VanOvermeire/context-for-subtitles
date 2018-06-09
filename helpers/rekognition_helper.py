from helpers import s3_helper

job_name_prefix = 'TRANSCRIBE_JOB_NAME='


def generate_job_tag(key, job_type):
    if '/' in key:
        key = key[key.rfind('/') + 1:len(key)]

    if '.' in key:
        key = key.split('.')[0]

    return job_type + '-job-for-' + key


def generate_s3_key_and_data(celeb_job_id, transcribe_job_name):
    key = s3_helper.S3_NEW_JOB_FOLDER + celeb_job_id
    data = job_name_prefix + transcribe_job_name

    return key, data


def get_id_and_name_from_s3_data(s3_data):
    if job_name_prefix in s3_data:
        return s3_data.split('=')[1]

    return None
