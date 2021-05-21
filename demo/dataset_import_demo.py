import os

from operator_sdk.dataset.importer import download_dataset

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-north-1'

# set download location
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'test_import')

if __name__ == '__main__':
    download_dataset('d-20210512141706-mckhc', output_dir, region, ak, sk)
