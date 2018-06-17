ONE_SECOND = 1000


# TODO alternatively, go to seconds for both dictionaries
def build_celebrity_rekognition_dict(rekognition_json):
    temporary_rekognition_dict = dict()

    if 'Celebrities' in rekognition_json:
        for cel in rekognition_json['Celebrities']:
            timestamp = cel['Timestamp']
            timestamp = timestamp / ONE_SECOND  # one identification per second will do
            timestamp = int(round(timestamp))

            name = cel['Celebrity']['Name']

            if timestamp not in temporary_rekognition_dict:
                name_set = set()
                name_set.add(name)
                temporary_rekognition_dict[timestamp] = name_set
            elif name not in temporary_rekognition_dict[timestamp]:
                name_set = temporary_rekognition_dict[timestamp]
                name_set.add(name)

                temporary_rekognition_dict[timestamp] = name_set

    rekogntion_dict = dict()

    for old_key in temporary_rekognition_dict.keys():
        new_key = old_key * ONE_SECOND  # reset the timestamps so we can match with transcription
        rekogntion_dict[new_key] = temporary_rekognition_dict[old_key]

    return rekogntion_dict


def build_transcribe_dict(transcribe_json):
    transcription_dict = dict()
    timestamp = 0

    if 'results' in transcribe_json and 'items' in transcribe_json['results']:
        for item in transcribe_json['results']['items']:
            try:
                timestamp = item['start_time']
                timestamp = int(float(timestamp) * 1000)  # we want the same timestamp as for the rekognition job
                text = item['alternatives'][0]['content']  # prefer the first alternative if there are multiple
            except KeyError:
                timestamp = timestamp + 1
                text = item['alternatives'][0]['content']

            transcription_dict[timestamp] = text

    return transcription_dict


def combine_transcribe_and_rekognition(transcribe_json, rekognition_json):
    combined_result = ''
    previous_person = set()

    transcribe_dict = build_transcribe_dict(transcribe_json)
    rekognition_dict = build_celebrity_rekognition_dict(rekognition_json)

    if len(transcribe_dict) > 0 and len(rekognition_dict) > 0:
        tr_key = max(transcribe_dict, key=int)
        rek_key = max(rekognition_dict, key=int)
        highest_value = max(tr_key, rek_key)

        i = 0

        while i <= highest_value:
            if i in transcribe_dict and i in rekognition_dict:
                previous_person, combined_result = add_person_to_result(previous_person, rekognition_dict[i], combined_result)
                combined_result = add_transcription_to_result(transcribe_dict[i], combined_result)
            elif i in rekognition_dict:
                previous_person, combined_result = add_person_to_result(previous_person, rekognition_dict[i], combined_result)
            elif i in transcribe_dict:
                combined_result = add_transcription_to_result(transcribe_dict[i], combined_result)

            i += 1

    return combined_result


def add_person_to_result(previous_person, new_person, combined_results):
    if end_of_results_is_a_people_reference(combined_results):
        if previous_person != new_person:
            previous_person = previous_person.union(new_person)
            combined_results = combined_results[0:combined_results.rfind('[')]
            combined_results = add_person_with_whitespace_if_needed(previous_person, combined_results)
    elif new_person != previous_person:
        previous_person = new_person
        combined_results = add_person_with_whitespace_if_needed(previous_person, combined_results)

    return previous_person, combined_results


def add_person_with_whitespace_if_needed(to_add_set, combined_results):
    to_add_list = sorted(to_add_set)
    to_add = '[' + str(to_add_list).strip('[]').replace('\'', '') + ']'

    if len(combined_results) == 0 or str(combined_results[len(combined_results) - 1: len(combined_results)]) == ' ':
        combined_results += to_add
    else:
        combined_results += ' ' + to_add

    return combined_results


def add_transcription_to_result(to_add, combined_results):
    if len(combined_results) == 0 or to_add == '.':
        combined_results += to_add
    else:
        combined_results += ' ' + to_add

    return combined_results


def end_of_results_is_a_people_reference(combined_results):
    trimmed_results = combined_results.strip()
    return str(trimmed_results[len(trimmed_results) - 1: len(trimmed_results)]) == ']'
