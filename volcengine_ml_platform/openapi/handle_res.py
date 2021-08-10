import logging


def handle_res(res_json):
    err = res_json['ResponseMetadata'].get('Error', None)
    if err:
        logging.error('error: %s', err['Message'])
        raise Exception('handle res failed') from err
    return res_json


def get_unique_flavor(list_flavor_result):
    flavor_map = list_flavor_result['Result']['List']
    for _, v in flavor_map.items():
        if v and len(v):
            return v[0]['FlavorID']
    return ''
