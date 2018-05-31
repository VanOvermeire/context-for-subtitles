ONE_SECOND = 10


def build_celebrity_rekognition_dict(rekognition_json):
    rekognition_dict = dict()

    if 'Celebrities' in rekognition_json:
        for cel in rekognition_json['Celebrities']:
            timestamp = cel['Timestamp']
            name = cel['Celebrity']['Name']

            if timestamp in rekognition_dict and name not in rekognition_dict[timestamp]:
                name = rekognition_dict[timestamp] + ', ' + name
            rekognition_dict[timestamp] = name

    print('Rekognition dict ' + str(rekognition_dict))

    return rekognition_dict


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

    print("Transcription dict " + str(transcription_dict))
    return transcription_dict


def combine_transcribe_and_rekognition(transcribe_json, rekognition_json):
    combined_result = ''
    previous_person = ''

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
                combined_result += transcribe_dict[i] + ' '
            elif i in rekognition_dict and rekognition_dict[i]:
                previous_person, combined_result = add_person_to_result(previous_person, rekognition_dict[i], combined_result)
            elif i in transcribe_dict:
                combined_result += transcribe_dict[i] + ' '

            i += 1

        if len(combined_result):
            combined_result = combined_result[0:len(combined_result) - 1]

    print('Result:   ' + str(combined_result))

    return combined_result


def add_person_to_result(previous_person, new_person, combined_results):
    if is_end_of_results_people(combined_results):
        if (new_person not in previous_person) and (previous_person not in new_person):
            previous_person = previous_person + ', ' + new_person
            combined_results = combined_results[0:combined_results.rfind('[')] + '[' + previous_person + '] '
    elif new_person != previous_person:
        previous_person = new_person
        combined_results += ' [' + new_person + '] '
    return previous_person, combined_results


def is_end_of_results_people(combined_results):
    return str(combined_results[len(combined_results) - 2: len(combined_results) - 1]) == ']'
