import unittest
from helpers import transcribe_helper

REGION = 'eu-west-1'


class TestCombineHelper(unittest.TestCase):

    def test_given_mp3_extension_when_get_extension_should_return_extension(self):
        key = 'some-valid-extension.mp3'

        result = transcribe_helper.get_extension(key)

        self.assertTrue(result, 'mp3')

    def test_given_mp4_extension_when_get_extension_should_return_extension(self):
        key = 'some-valid-extension.mp4'

        result = transcribe_helper.get_extension(key)

        self.assertTrue(result, 'mp4')

    def test_given_invalid_extension_when_get_extension_should_return_none(self):
        key = 'some-invalid-extension.txt'

        result = transcribe_helper.get_extension(key)

        self.assertTrue(result is None)

    def test_when_generate_file_uri_should_return_correct_uri(self):
        bucket = 'examplebucket'
        key = 'data/example.mp4'

        result = transcribe_helper.generate_file_uri(REGION, bucket, key)

        self.assertEqual(result, 'https://s3-eu-west-1.amazonaws.com/examplebucket/data/example.mp4')

    def test_given_s3_key_should_generate_a_name_without_extension(self):
        key = 'data/example.mp4'

        result = transcribe_helper.get_transcribe_job_name(key)

        self.assertEqual(result, 'tr-job-example')
