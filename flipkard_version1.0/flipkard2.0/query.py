import  boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import re

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Flipkar_DB')

# table.delete()
# print(table.item_count)
# 查询
response = table.query(
    KeyConditionExpression=Key('AccountName').eq('vikram')
)
items = response['Items']
print(items)
