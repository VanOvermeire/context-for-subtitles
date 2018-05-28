from helpers import s3_helper

people_id_prefix = 'PEOPLE_JOB_ID='
job_name_prefix = 'TRANSCRIBE_JOB_NAME='


def generate_s3_key_and_data(celeb_job_id, people_job_id, transcribe_job_name):
    key = s3_helper.S3_NEW_JOB_FOLDER + celeb_job_id
    data = people_id_prefix + people_job_id + ',' + job_name_prefix + transcribe_job_name

    return key, data


def get_id_and_name_from_s3_data(s3_data):
    keys = s3_data.split(',')
    # TODO get id for people

    if job_name_prefix in keys[1]:
        return keys[1].split('=')[1]

