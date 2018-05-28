def extract_job_id(event):
    sns = event["Records"][0]['Sns']
    job_id = sns['Message']["JobId"]
    return job_id

