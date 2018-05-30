import unittest

from helpers import rekognition_helper


class TestRekognitionHelper(unittest.TestCase):
    def test_given_job_id_and_name_when_generate_s3_data_should_return_key_and_data(self):
        celeb_job_id = 'celeb-job-id'
        person_job_id = 'person-job-id'
        job_name = 'tr-job-name'

        key, data = rekognition_helper.generate_s3_key_and_data(celeb_job_id, person_job_id, job_name)

        self.assertEqual(key, 'new-transcription-names/celeb-job-id')
        self.assertEqual(data, 'PEOPLE_JOB_ID=person-job-id,TRANSCRIBE_JOB_NAME=tr-job-name')

    def test_given_s3_data_when_get_id_and_name_from_s3_data_should_return_the_transcribe_job_name(self):
        data = 'PEOPLE_JOB_ID=person-job-id,TRANSCRIBE_JOB_NAME=tr-job-name'

        name = rekognition_helper.get_id_and_name_from_s3_data(data)

        self.assertEqual(name, 'tr-job-name')

    def test_given_a_key_with_prefix_and_extension_when_generate_job_tag_should_return_tag_without_the_prefix_or_extension(self):
        data = 'data/example.mp4'

        tag = rekognition_helper.generate_job_tag(data, 'celeb')

        self.assertEqual(tag, 'celeb-job-for-example')

    def test_given_a_key_with_extension_when_generate_job_tag_should_return_tag_without_extension(self):
        data = 'example.mp4'

        tag = rekognition_helper.generate_job_tag(data, 'celeb')

        self.assertEqual(tag, 'celeb-job-for-example')

    def test_given_a_key_when_generate_job_tag_should_return_tag_(self):
        data = 'example'

        tag = rekognition_helper.generate_job_tag(data, 'celeb')

        self.assertEqual(tag, 'celeb-job-for-example')
