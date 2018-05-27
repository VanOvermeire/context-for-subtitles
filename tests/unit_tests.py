import unittest
from helpers import transcribe_helper


class TestHelpers(unittest.TestCase):
    def test_when_get_extension_with_mp3_extension_should_return_extension(self):
        key = 'some-valid-extension.mp3'

        result = transcribe_helper.get_extension(key)

        self.assertTrue(result, 'mp3')

    def test_when_get_extension_with_mp4_extension_should_return_extension(self):
        key = 'some-valid-extension.mp4'

        result = transcribe_helper.get_extension(key)

        self.assertTrue(result, 'mp4')

    def test_when_get_extension_with_invalid_extension_should_return_none(self):
        key = 'some-invalid-extension.txt'

        result = transcribe_helper.get_extension(key)

        self.assertTrue(result is None)

    def test_when_generate_file_uri_should_return_correct_uri(self):
        bucket = 'examplebucket'
        key = 'example.mp4'

        result = transcribe_helper.generate_file_uri(bucket, key)

        self.assertEqual(result, 'https://s3-eu-west-1.amazonaws.com/examplebucket/example.mp4')
