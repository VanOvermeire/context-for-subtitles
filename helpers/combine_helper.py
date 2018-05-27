
def build_rekognition_dict(rekognition_json):
    rek_dict = dict()

    if 'Persons' in rekognition_json:
        for p in rekognition_json['Persons']:
            timestamp = p['Timestamp']
            name = 'Unknown person'

            rek_dict[timestamp] = name

    if 'Celebrities' in rekognition_json:
        for cel in rekognition_json['Celebrities']:
            timestamp = cel['Timestamp']
            name = cel['Celebrity']['Name']

            # might override the person timestamps, not an issue since this value gives more info
            rek_dict[timestamp] = name

    return rek_dict
