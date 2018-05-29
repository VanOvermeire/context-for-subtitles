import unittest

from helpers import stepfunction_helper


class TestStepFunctionHelper(unittest.TestCase):
    def test_given_job_id_and_name_when_generate_step_input_should_generate_the_step_function_input(self):
        job_id = '1234'
        tr_name = 'transcribe-name'

        result = stepfunction_helper.generate_step_input(job_id, tr_name)

        self.assertEqual(result, "{\"celeb-job-id\": \"1234\", \"transcribe-name\": \"transcribe-name\"}")

    def test_given_an_event_when_get_job_id_and_name_should_return_the_id_and_name(self):
        event = {"celeb-job-id": "id", "transcribe-name": "name"}

        job_id, name = stepfunction_helper.get_job_id_and_name(event)

        self.assertEqual(job_id, 'id')
        self.assertEqual(name, 'name')
