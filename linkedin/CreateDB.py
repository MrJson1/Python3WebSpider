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
        TableName='Linkedin_DB',
        KeySchema=[
            {
                'AttributeName': 'ProfileName',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'University',
                'KeyType': 'RANGE'
            },

        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ProfileName',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'University',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    client.get_waiter('table_exists').wait(TableName='Linkedin_DB')
    # table.meta.client.get_waiter('table_exists').wait(TableName='Linkedin_DB', )
    response = client.describe_table(TableName='Linkedin_DB')
    print(response)

create_dynamodb('./config')
    # print(table.item_count)

