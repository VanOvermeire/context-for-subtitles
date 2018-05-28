import unittest

from helpers import sns_helper


class TestSnsHelper(unittest.TestCase):
    def test_given_no_celebs_or_people_when_build_rekognition_dict_should_return_empty_dict(self):
        json_payload = {
            "Records": [
                {
                    "EventSource": 'aws:sns',
                    "Sns": {
                        "Message": {
                            "JobId":"815a81feb7252fcdbfc9ea6d2f246a46ab13513fc5c022c2f26abdc6ae8908ec",
                            "Status":"SUCCEEDED"
                        }
                    }
                }
            ]
        }

        result = sns_helper.extract_job_id(json_payload)

        self.assertEqual(result, "815a81feb7252fcdbfc9ea6d2f246a46ab13513fc5c022c2f26abdc6ae8908ec")
