import unittest

from helpers import sns_helper


class TestSnsHelper(unittest.TestCase):
    def test_given_an_sns_payload_when_extract_job_id_should_get_the_job_id(self):
        json_payload = {
            "Records": [
                {
                    "EventSource": 'aws:sns',
                    "Sns": {
                        "Message": '{"JobId": "815a81feb7252fcdbfc9ea6d2f246a46ab13513fc5c022c2f26abdc6ae8908ec", "Status": "SUCCEEDED"}'
                    }
                }
            ]
        }

        result = sns_helper.extract_job_id(json_payload)

        self.assertEqual(result, "815a81feb7252fcdbfc9ea6d2f246a46ab13513fc5c022c2f26abdc6ae8908ec")

    def test_given_an_sns_payload_when_extract_bucket_and_key_should_get_bucket_and_key(self):
        json_payload = {
            "Records": [
                {
                    "EventSource": 'aws:sns',
                    "Sns": {
                        "Message": '{"Records":[{"s3":{"bucket":{"name":"examplebucket"},"object":{"key":"examplekey"}}}]}',
                    }
                }

            ]
        }

        bucket, key = sns_helper.extract_bucket_and_key(json_payload)

        self.assertEqual(bucket, 'examplebucket')
        self.assertEqual(key, 'examplekey')
