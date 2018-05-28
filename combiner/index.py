import boto3

from helpers import combine_helper, s3_helper

rek_client = boto3.client('rekognition')


def my_handler(event, context):
    # receive job id(s) and job name
    response = rek_client.get_celebrity_recognition(JobId='14e160ba3b06f3e0973105322993aa81be3e4b119369466df3193cf2154f52e2')
    # get the data

    # combine

    # save results to bucket

    return {
        'message': 'Finished combining data.'
    }


# {
#     "resource": "arn:aws:lambda:eu-west-1:262438358359:function:state-machine-combiner",
#     "input": {
#         "celeb-job-id": "1234",
#         "transcribe-name": "job-for-mp4",
#         "ourValue": "True"
#     },
#     "timeoutInSeconds": null
# }