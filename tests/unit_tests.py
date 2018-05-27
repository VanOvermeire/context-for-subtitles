import unittest
import json

from helpers import transcribe_helper, combine_helper


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

    def test_when_no_celebrities_should_return_empty_dict(self):
        json_payload = {
            "Key": 636801.0000000003,
            "Labels": [{
                "Label": {
                    "Confidence": 96.37960052490234,
                    "Name": "Bottle"
                },
                "Timestamp": 0
            }]
        }

        result = combine_helper.build_rekognition_dict(json_payload)

        self.assertEqual(0, len(result))

    def test_when_a_celebrities_should_return_dict_with_timestamps_and_names(self):
        json_payload = {
            "Key": 636801.0000000003,
            "Labels": [{
                "Label": {
                    "Confidence": 96.37960052490234,
                    "Name": "Bottle"
                },
                "Timestamp": 0
            }],
            "Celebrities": [{
                "Celebrity": {
                    "Confidence": 97,
                    "Id": "Z3He8D",
                    "Name": "Warren Buffett",
                },
                "Timestamp": 33
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Not Warren Buffett",
                },
                "Timestamp": 1634
            }]
        }

        result = combine_helper.build_rekognition_dict(json_payload)

        self.assertEqual(2, len(result))
        self.assertEqual(result[33], 'Warren Buffett')
        self.assertEqual(result[1634], 'Not Warren Buffett')

    def test_when_a_celebrities_should_return_dict_with_timestamps_and_names(self):
        json_payload = {
            "Key": 636801.0000000003,
            "Labels": [{
                "Label": {
                    "Confidence": 96.37960052490234,
                    "Name": "Bottle"
                },
                "Timestamp": 0
            }],
            "Celebrities": [{
                "Celebrity": {
                    "Confidence": 97,
                    "Id": "Z3He8D",
                    "Name": "Warren Buffett",
                },
                "Timestamp": 33
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Not Warren Buffett",
                },
                "Timestamp": 1634
            }]
        }

        result = combine_helper.build_rekognition_dict(json_payload)

        self.assertEqual(2, len(result))
        self.assertEqual(result[33], 'Warren Buffett')
        self.assertEqual(result[1634], 'Not Warren Buffett')

    def test_when_persons_should_return_dict_with_timestamps_and_unkown_as_name(self):
        json_payload = {
            "Key": 636801.0000000003,
            "Labels": [{
                "Label": {
                    "Confidence": 96.37960052490234,
                    "Name": "Bottle"
                },
                "Timestamp": 0
            }],
            "Persons": [{
                "Person": {
                    "Index": 0
                },
                "Timestamp": 33
            }, {
                "Person": {
                    "Index": 0
                },
                "Timestamp": 100
            }]
        }

        result = combine_helper.build_rekognition_dict(json_payload)

        self.assertEqual(2, len(result))
        self.assertEqual(result[33], 'Unknown person')
        self.assertEqual(result[100], 'Unknown person')

    def test_when_celebrities_and_unkown_people_should_prefer_celebrities(self):
        # such is life
        json_payload = {
            "Key": 636801.0000000003,
            "Labels": [{
                "Label": {
                    "Confidence": 96.37960052490234,
                    "Name": "Bottle"
                },
                "Timestamp": 0
            }],
            "Celebrities": [{
                "Celebrity": {
                    "Confidence": 97,
                    "Id": "Z3He8D",
                    "Name": "Warren Buffett",
                },
                "Timestamp": 33
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Not Warren Buffett",
                },
                "Timestamp": 1634
            }],
            "Persons": [{
                "Person": {
                    "Index": 0
                },
                "Timestamp": 33
            }, {
                "Person": {
                    "Index": 0
                },
                "Timestamp": 100
            }]
        }

        result = combine_helper.build_rekognition_dict(json_payload)

        self.assertEqual(3, len(result))
        self.assertEqual(result[33], 'Warren Buffett')
        self.assertEqual(result[100], 'Unknown person')
        self.assertEqual(result[1634], 'Not Warren Buffett')

