import os
import boto3

from helpers import sns_helper, s3_helper, rekognition_helper, stepfunction_helper

step_client = boto3.client('stepfunctions')
s3_client = boto3.client('s3')


def my_handler(event, context):
    job_id = sns_helper.extract_job_id(event)
    key = s3_helper.S3_NEW_JOB_FOLDER + job_id

    print('Extracted' + str(job_id) + '. Now getting data from s3 under key ' + str(key))

    s3_data = s3_helper.get_object_as_string(s3_client, os.environ['BUCKET'], key)

    print('Found s3 data ' + str(s3_data) + ' for key ' + str(key))

    transcribe_name = rekognition_helper.get_id_and_name_from_s3_data(s3_data)
    step_input = stepfunction_helper.generate_step_input(job_id, transcribe_name)

    print('Starting step function with input ' + str(step_input))

    response = step_client.start_execution(
        stateMachineArn=os.environ['STEP_FUNCTION'],
        name='step-name-of-' + job_id,
        input=step_input
    )

    print('Started step function: ' + str(response))

    return {
        'message': 'Started step function.'
    }
