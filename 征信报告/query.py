import  boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import re

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Credit_DB')

# table.delete()
# print(table.item_count)

# table.delete()
# print(table.item_count)
# 查询
# response = table.get_item(
#     Key={
#         'ProfileName': '杨凯',
#         'University': '辽宁大学'
#     }
# )

response = table.query(
    KeyConditionExpression=Key('transaction_id').eq('8140eeda-c5ea-4416-bc17-7e9f991d9f18')
)
items = response['Items'][0]['wholeData']
print(items)
