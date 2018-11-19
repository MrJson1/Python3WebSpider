import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def load_json(path):
    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except Exception as e:
        print('ERROR: no such file like ' + path)
        exit(-1)
    else:
        return data
def create_dynamodb(path):
    conf =load_json(path)
    client = boto3.client('dynamodb', region_name=conf['region_name'],
                               aws_access_key_id=conf['aws_access_key_id'],
                               aws_secret_access_key=conf['aws_secret_access_key'])

    table = client.create_table(
        TableName='Flipkar_DB',
        KeySchema=[
            {
                'AttributeName': 'UserId',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'AccountName',
                'KeyType': 'RANGE'
            },

        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'UserId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'AccountName',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    client.get_waiter('table_exists').wait(TableName='Flipkar_DB')
    # table.meta.client.get_waiter('table_exists').wait(TableName='Linkedin_DB', )
    response = client.describe_table(TableName='Flipkar_DB')
    print(response)


create_dynamodb('./config')
    # print(table.item_count)

