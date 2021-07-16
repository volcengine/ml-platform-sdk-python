import logging


def handle_res(res_json):
    err = res_json['ResponseMetadata']['Error']
    if err:
        logging.error('error: %s', err['Message'])
    return res_json
