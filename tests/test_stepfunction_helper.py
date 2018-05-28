import unittest

from helpers import stepfunction_helper


class TestStepFunctionHelper(unittest.TestCase):
    def test_given_job_id_and_name_when_generate_step_input_should_generate_the_step_function_input(self):
        job_id = '1234'
        tr_name = 'transcribe-name'

        result = stepfunction_helper.generate_step_input(job_id, tr_name)

        self.assertEqual(result, "{\"celeb-job-id\": \"1234\", \"transcribe-name\": \"transcribe-name\"}")
