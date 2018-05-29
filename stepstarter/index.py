import boto3

from helpers import sns_helper, s3_helper, rekognition_helper

step_client = boto3.client('stepfunctions')
s3_client = boto3.client('s3')


def my_handler(event, context):
    job_id = sns_helper.extract_job_id(event)
    print("Extracted" + str(job_id))

    s3_data = s3_helper.get_object_as_string(s3_client, 'FILL IN BUCKET', s3_helper.S3_NEW_JOB_FOLDER + job_id)  # TODO env var

    print("Found " + s3_data)

    transcribe_name = rekognition_helper.get_id_and_name_from_s3_data(s3_data)

    response = step_client.start_execution(
        stateMachineArn='string',  # TODO env var
        name='name-of-' + job_id,
        input="{\"celeb-job-id\": \"" + job_id + "\", \"transcribe-name\": \"" + transcribe_name + "\"}"
    )

    print("Got back response " + str(response))

    return {
        'message': 'Started step function.'
    }
