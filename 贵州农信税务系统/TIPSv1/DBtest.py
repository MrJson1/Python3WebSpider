import pymongo

client = pymongo.MongoClient('11.18.16.50',27017)
print(client.database_names())
# db = client.SSTBDB
db = client.TIPSDB
# print(db)
collection = db['712301TABLE']
print(collection)

data = {'djxh': '10215203000000557146',
 'jklx': '1',
 'nsrmc': '遵义市老城小学',
 'nsrsbh': '12520302429400744T',
 'swjgmc': '国家税务总局遵义市红花岗区税务局',
 'zgswj_dm': '15203020000',
 'zgswskfj_dm': '15203026200',
 'zgswskfjmc': '国家税务总局遵义市红花岗区税务局第二税务分局'}

# result = collection.insert_one(data)
# print(result)
print(collection.find().count())
result = collection.find_one( {'nsrsbh': '12520302429400744'}
)
# result = collection.find_one()

# result['xyzt'] = '1'
# collection.update({'xyzt':'2'},result)
if result:
 print("result:", result)
if not result:
 print("不存在result:",result)
condition = {'taxpaycode':'222222'}
result = collection.find()
for item in result:
    print(item)


# print(collection.find_one({'taxorgcode', '25204210000'}))

#删除数据
# result = collection.remove({'dbcbxxbs':'1'})
# print(result)