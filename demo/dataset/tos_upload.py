import sys
import logging
from tqdm import tqdm

from volcengine_ml_platform.tos.tos import TOSClient

# export env vars as follow:

#  export VOLC_ACCESSKEY="AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE"
#  export VOLC_SECRETKEY="WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=="
#  export VOLC_REGION="cn-north-1"
#  export VOLC_ML_PLATFORM_ENV="BOE"            # optional

# usage:
# 0. change bucket name.
# 1. upload file to tos bucket, `cat ./demo/dataset/tos_upload.py | python3`
# 2. create dataset on https://v-vconsole.bytedance.net/ml-platform in env of boe
if __name__ == '__main__':

    bucket = "mlplatform-test-for-middle-dataset"
    prefix = './demo/dataset/'
    origin = 'origin.jpg'
    region = 'cn-north-1'

    tosCli = TOSClient()
    if not tosCli.bucket_exists(bucket) and not tosCli.create_bucket(
            bucket, region):
        logging.error("fail to create the bucket")
        sys.exit(1)

    for i in tqdm(range(5000)):
        tosCli.upload_file(prefix + origin, bucket, "origin{}.jpg".format(i))
