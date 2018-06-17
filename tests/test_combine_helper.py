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

    def test_given_celebs_at_different_times_when_build_rekognition_dict_should_return_dict_with_timestamps_and_sets_with_single_names(self):
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
                    "Name": "Person A",
                },
                "Timestamp": 33
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Person B",
                },
                "Timestamp": 1634
            }]
        }

        result = combine_helper.build_celebrity_rekognition_dict(json_payload)

        self.assertEqual(2, len(result))
        self.assertEqual({'Person A'}, result[0])
        self.assertEqual({'Person B'}, result[2000])

    def test_given_celebs_at_one_time_when_build_rekognition_dict_should_return_dict_with_set_with_those_names(self):
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
                    "Name": "Person A",
                },
                "Timestamp": 1501
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Person B",
                },
                "Timestamp": 1501
            }]
        }

        result = combine_helper.build_celebrity_rekognition_dict(json_payload)

        self.assertEqual(1, len(result))
        self.assertEqual({'Person B', 'Person A'}, result[2000])

    def test_given_celebs_at_several_times_when_build_rekognition_dict_should_return_dict_with_multiple_sets(self):
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
                    "Name": "Person A",
                },
                "Timestamp": 1501
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Person B",
                },
                "Timestamp": 1501
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Person A",
                },
                "Timestamp": 2980
            }]
        }

        result = combine_helper.build_celebrity_rekognition_dict(json_payload)

        self.assertEqual(2, len(result))
        self.assertEqual({'Person A', 'Person B'}, result[2000])
        self.assertEqual({'Person A'}, result[3000])

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
        self.assertEqual('Some', result[670])
        self.assertEqual('transcript', result[1040])

    def test_given_empty_payloads_when_combine_transcribe_and_rekognition_should_return_empty_string(self):
        result = combine_helper.combine_transcribe_and_rekognition('', '')

        self.assertEqual(len(result), 0)

    def test_given_items_and_celebs_when_combine_transcribe_and_rekognition_should_return_text_with_info_on_speakers_without_duplicating_speakers(self):
        rek_payload = {
            "Key": 636801.0000000003,
            "Celebrities": [{
                "Celebrity": {
                    "Confidence": 97,
                    "Id": "Z3He8D",
                    "Name": "Person A",
                },
                "Timestamp": 33
            }, {
                "Celebrity": {
                    "Confidence": 97,
                    "Id": "Z3He8D",
                    "Name": "Person A",
                },
                "Timestamp": 100
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Person B",
                },
                "Timestamp": 1634
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Person C",
                },
                "Timestamp": 2200
            }, {
                "Celebrity": {
                    "Confidence": 52.999996185302734,
                    "Id": "Z3He8D",
                    "Name": "Person A",
                },
                "Timestamp": 4001
            }]
        }

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
                }, {
                    "start_time": "3.640",
                    "end_time": "3.660",
                    "alternatives": [{
                        "confidence": "1.0000",
                        "content": "here"
                    }],
                    "type": "pronunciation"
                }]
            }
        }

        result = combine_helper.combine_transcribe_and_rekognition(transcribe_payload, rek_payload)

        self.assertEqual('[Person A] Some more transcript [Person B, Person C] here [Person A]', result)

    def test_given_multiple_people_and_new_not_among_them_when_add_person_to_result_should_add_person_to_results_and_set_to_current(self):
        combined_result = 'I am talking now [Person A, Person B]'
        previous = set()
        previous.add('Person A')
        previous.add('Person B')
        new_person = set()
        new_person.add('Person C')

        people, result = combine_helper.add_person_to_result(previous, new_person, combined_result)

        self.assertEqual(people, {'Person A', 'Person B', 'Person C'})
        self.assertEqual('I am talking now [Person A, Person B, Person C]', result)

    def test_given_multiple_people_and_new_among_them_when_add_person_to_result_should_not_change_results(self):
        combined_result = 'I am talking now [Person A, Person B] '
        previous = set()
        previous.add('Person A')
        previous.add('Person B')
        new_person = set()
        new_person.add('Person A')

        people, result = combine_helper.add_person_to_result(previous, new_person, combined_result)

        self.assertEqual({'Person A', 'Person B'}, people)
        self.assertEqual('I am talking now [Person A, Person B]', result)

    def test_given_a_person_talking_earlier_when_add_person_to_result_should_add_person_and_set_current(self):
        combined_result = 'I am talking now [Person A, Person B], still talking'
        previous = set()
        previous.add('Person A')
        new_person = set()
        new_person.add('Person B')

        people, result = combine_helper.add_person_to_result(previous, new_person, combined_result)

        self.assertEqual(people, {'Person B'})
        self.assertEqual(result, 'I am talking now [Person A, Person B], still talking [Person B]')

    def test_given_a_result_ending_with_people_when_end_of_results_is_a_people_reference_should_return_true(self):
        current_results = 'some results [Person A, Person B] '

        result = combine_helper.end_of_results_is_a_people_reference(current_results)

        self.assertEqual(True, result)

    def test_given_a_result_ending_with_people_and_no_whitespace_when_end_of_results_is_a_people_reference_should_return_true(self):
        current_results = 'some results [Person A, Person B]'

        result = combine_helper.end_of_results_is_a_people_reference(current_results)

        self.assertEqual(True, result)

    def test_given_a_result_not_ending_with_people_when_end_of_results_is_a_people_reference_should_return_false(self):
        current_results = 'some results [Person A, Person B] and some more '

        result = combine_helper.end_of_results_is_a_people_reference(current_results)

        self.assertEqual(False, result)

    def test_given_a_result_not_ending_with_people_no_whitespace_when_end_of_results_is_a_people_reference_should_return_false(self):
        current_results = 'some results [Person A, Person B] and some more'

        result = combine_helper.end_of_results_is_a_people_reference(current_results)

        self.assertEqual(False, result)
