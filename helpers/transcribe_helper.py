def get_extension(key):
    key_parts = key.split('.')
    last_part = key_parts[len(key_parts) - 1]

    if last_part in ('mp3', 'mp4', 'wav', 'flac'):
        return last_part

    return None


def generate_file_uri(bucket, key):
    region = 'eu-west-1'  # TODO find current region

    return 'https://s3-' + region + '.amazonaws.com/' + bucket + '/' + key
