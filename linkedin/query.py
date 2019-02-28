import  boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import re

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Linkedin_DB')
# # 获取一个Item
# response = table.get_item(
#     Key={
#         'ProfileName': '杨凯',
#         'University': '辽宁大学'
#     }
# )
# print(table.item_count)
# item = response['Item']
# print(item)

# 查询
response = table.query(
    KeyConditionExpression=Key('ProfileName').eq('susu zhou')
)
items = response['Items']
print(items)
