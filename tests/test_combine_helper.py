import json
import unittest
from helpers import combine_helper


class TestCombineHelper(unittest.TestCase):

    def test_given_no_celebs_or_people_when_build_rekognition_dict_should_return_empty_dict(self):
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

        result = combine_helper.build_celebrity_rekognition_dict(json_payload)

        self.assertEqual(0, len(result))

    def test_given_celebs_when_build_rekognition_dict_should_return_dict_with_timestamps_and_names(self):
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

        result = combine_helper.build_celebrity_rekognition_dict(json_payload)

        self.assertEqual(2, len(result))
        self.assertEqual(result[33], 'Warren Buffett')
        self.assertEqual(result[1634], 'Not Warren Buffett')

    def test_given_no_items_when_build_transcribe_dict_should_return_empty_dict(self):
        json_payload = {
            "jobName": "example-job",
            "results": {
                "transcripts": [{
                    "transcript": "Some transcript"
                }]
            }}

        result = combine_helper.build_transcribe_dict(json_payload)

        self.assertEqual(0, len(result))

    def test_given_items_when_build_transcribe_dict_should_return_timestamps_with_results(self):
        json_payload = {
            "jobName": "example-job",
            "results": {
                "transcripts": [{
                    "transcript": "Some transcript"
                }],
                "items": [{
                    "start_time": "0.670",
                    "end_time": "1.040",
                    "alternatives": [{
                        "confidence": "1.0000",
                        "content": "Some"
                    }],
                    "type": "pronunciation"
                }, {
                    "start_time": "1.040",
                    "end_time": "1.260",
                    "alternatives": [{
                        "confidence": "1.0000",
                        "content": "transcript"
                    }],
                    "type": "pronunciation"
                }]}}

        result = combine_helper.build_transcribe_dict(json_payload)

        self.assertEqual(2, len(result))
        self.assertEqual(result[670], 'Some')
        self.assertEqual(result[1040], 'transcript')

    def test_given_empty_payloads_when_combine_transcribe_and_rekognition_should_return_empty_string(self):
        result = combine_helper.combine_transcribe_and_rekognition('', '')

        self.assertEqual(len(result), 0)

    def test_given_items__and_celebs_when_combine_transcribe_and_rekognition_should_return_text_with_info_on_speakers_without_duplicating_speakers(self):
        rek_payload = {
            "Key": 636801.0000000003,
            "Celebrities": [{
                "Celebrity": {
                    "Confidence": 97,
                    "Id": "Z3He8D",
                    "Name": "Warren Buffett",
                },
                "Timestamp": 33
            }, {
                "Celebrity": {
                    "Confidence": 97,
                    "Id": "Z3He8D",
                    "Name": "Warren Buffett",
                },
                "Timestamp": 100
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
            }]}

        transcribe_payload = {
            "jobName": "example-job",
            "results": {
                "transcripts": [{
                    "transcript": "Some more transcript"
                }],
                "items": [{
                    "start_time": "0.500",
                    "end_time": "0.800",
                    "alternatives": [{
                        "confidence": "1.0000",
                        "content": "Some"
                    }],
                    "type": "pronunciation"
                }, {
                    "start_time": "0.900",
                    "end_time": "1.000",
                    "alternatives": [{
                        "confidence": "1.0000",
                        "content": "more"
                    }],
                    "type": "pronunciation"
                }, {
                    "start_time": "1.640",
                    "end_time": "1.660",
                    "alternatives": [{
                        "confidence": "1.0000",
                        "content": "transcript"
                    }],
                    "type": "pronunciation"
                }]}}

        result = combine_helper.combine_transcribe_and_rekognition(transcribe_payload, rek_payload)

        self.assertEqual(result, ' [Warren Buffett] Some more  [Not Warren Buffett] transcript')  # TODO too many spaces - fix

    def test_using_actual_json_outputs(self):
        with open('../examples/celebrity_output.json') as rekognition, open('../examples/transcribe_output.json') as transcribe:
            r_json = json.load(rekognition)
            t_json = json.load(transcribe)

            # combine_helper.build_celebrity_rekognition_dict(r_json)
            result = combine_helper.combine_transcribe_and_rekognition(t_json, r_json)


    def test_given_multiple_people_and_new_not_among_them_when_add_person_to_result_should_add_person_to_results_and_add_to_current(self):
        combined_result = 'I am talking now [Person A, Person B] '
        previous = 'Person A, Person B'
        new = 'Person C'

        people, result = combine_helper.add_person_to_result(previous, new, combined_result)

        self.assertEqual(people, 'Person A, Person B, Person C')
        self.assertEqual(result, 'I am talking now [Person A, Person B, Person C] ')

    def test_given_multiple_people_and_new_among_them_when_add_person_to_result_should_not_change_results(self):
        combined_result = 'I am talking now [Person A, Person B] '
        previous = 'Person A, Person B'
        new = 'Person A'

        people, result = combine_helper.add_person_to_result(previous, new, combined_result)

        self.assertEqual(people, 'Person A, Person B')
        self.assertEqual(result, 'I am talking now [Person A, Person B] ')

    def test_given_a_person_talking_earlier_when_add_person_to_result_should_add_person_and_set_current(self):
        combined_result = 'I am talking now [Person A, Person B], still talking'
        previous = 'Person A'
        new = 'Person B'

        people, result = combine_helper.add_person_to_result(previous, new, combined_result)

        self.assertEqual(people, 'Person B')
        self.assertEqual(result, 'I am talking now [Person A, Person B], still talking [Person B] ')



