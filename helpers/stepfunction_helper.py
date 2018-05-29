def generate_step_input(celeb_job_id, transcribe_name):
    return "{\"celeb-job-id\": \"" + celeb_job_id + "\", \"transcribe-name\": \"" + transcribe_name + "\"}"


def get_job_id_and_name(event):
    return event['celeb-job-id'], event['transcribe-name']
