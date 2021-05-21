from operator_sdk.service.dataset_service import DatasetService

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    client = DatasetService(region, ak, sk)

    # Get dataset info
    print(client.get_dataset('d-20210512141706-mckhc'))

    # List datasets
    print(client.list_datasets())
