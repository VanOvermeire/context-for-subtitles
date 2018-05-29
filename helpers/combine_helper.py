def build_rekognition_dict(rekognition_json):
    rekognition_dict = dict()

    # TODO, not using this yet
    # if 'Persons' in rekognition_json:
    #     for p in rekognition_json['Persons']:
    #         timestamp = p['Timestamp']
    #         name = 'Unknown Person'
    #
    #         rekognition_dict[timestamp] = name

    if 'Celebrities' in rekognition_json:
        for cel in rekognition_json['Celebrities']:
            timestamp = cel['Timestamp']
            name = cel['Celebrity']['Name']

            # might override the person timestamps, not an issue since this value gives more info
            rekognition_dict[timestamp] = name

    return rekognition_dict


def build_transcribe_dict(transcribe_json):
    transcription_dict = dict()

    if 'results' in transcribe_json and 'items' in transcribe_json['results']:
        for item in transcribe_json['results']['items']:
            timestamp = item['start_time']
            timestamp = int(float(timestamp) * 1000)  # we want the same timestamp as for the rekognition job
            text = item['alternatives'][0]['content']  # prefer the first alternative if there are multiple

            transcription_dict[timestamp] = text

    return transcription_dict


def combine_transcribe_and_rekognition(transcribe_json, rekognition_json):
    result = ''
    current_person = ''

    transcribe_dict = build_transcribe_dict(transcribe_json)
    rekognition_dict = build_rekognition_dict(rekognition_json)

    if len(transcribe_dict) > 0 and len(rekognition_dict) > 0:
        highest_value = max(max(transcribe_dict, key=transcribe_dict.get), max(rekognition_dict, key=rekognition_dict.get))
        i = 0

        while i <= highest_value:
            if i in transcribe_dict and i in rekognition_dict and rekognition_dict[i] != current_person:
                result += '[' + rekognition_dict[i] + '] ' + transcribe_dict[i] + ' '
                current_person = rekognition_dict[i]
            elif i in rekognition_dict and rekognition_dict[i] != current_person:
                result += '[' + rekognition_dict[i] + '] '
                current_person = rekognition_dict[i]
            elif i in transcribe_dict:
                result += transcribe_dict[i] + ' '

            i += 1

        if len(result):
            result = result[0:len(result) - 1]

    return result
