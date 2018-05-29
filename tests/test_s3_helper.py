import unittest

from helpers import s3_helper


class TestS3Helper(unittest.TestCase):
    def test_given_transcribe_name_should_return_suffix_with_results_prefix(self):
        name = 'tr-job-example'

        result = s3_helper.generate_key_for_combine_result(name)

        self.assertEqual(result, 'results/example')

    def test_given_transcribe_name_with_no_prefix_should_return_entire_name_with_results_prefix(self):
        name = 'example'

        result = s3_helper.generate_key_for_combine_result(name)

        self.assertEqual(result, 'results/example')

    def test_given_event_when_extract_bucket_and_key_from_event_should_get_bucket_and_key(self):
        s3 = dict()
        s3['bucket'] = {'name': 'example-bucket'}
        s3['object'] = {'key': 'data/new-stuff'}

        event = dict()
        event['Records'] = [{'s3': s3}]

        bucket, key = s3_helper.extract_bucket_and_key_from_event(event)

        self.assertTrue(bucket, 'example-bucket')
        self.assertTrue(key, 'data/new-stuff')
