

def my_handler(event, context):
    job_name = 'rek-job-for'

    return {
        'message': 'started job for name ' + job_name
    }