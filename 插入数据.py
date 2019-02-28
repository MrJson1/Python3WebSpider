import json
import pymysql

f=open('C://sysadmin/config.ini','r')
configure_info = json.loads(f.readline())
aws_access_key_id=configure_info['aws_access_key_id']
aws_secret_access_key=configure_info['aws_secret_access_key']
host_name=configure_info['host_name']
db_user_name=configure_info['db_user_name']
password_code=configure_info['password_code']

conn=pymysql.connect(host=host_name,user=db_user_name,passwd=password_code,db='bank_info',charset="utf8")
cursor = conn.cursor()

file_name = "./BankName_new.txt"
f = open(file_name, 'r')
records = f.readlines()
for record in records:
    record = json.loads(record)
    try:
        bank = record['Bank']
        branch = record['Branch']
        ifsc_code = record['IFSCCode']
        address = record['Address']
        state = record['State']
        city = record['City']

        print('a\n\n')
        bank_details = record['BankDetails']
        contact_number = record['Contact']
        print('b\n\n')
        mode_of_payment = record['ModeOfPayment']
        open_hours = record['OpenHours']
        location = record['Location']
        country = record['Country']
        pin_code = record['Pincode']
        print('c\n\n')
        insert_lang = 'insert into bank_info (ifsc_code,address,bank,branch,bank_details,state,city,contact_number,mode_of_payment,open_hours,location,country,pin_code) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}") ; '.format(
            ifsc_code, address, bank, branch, bank_details, state, city, contact_number, mode_of_payment, open_hours,
            location,
            country, pin_code)
        cursor.execute(insert_lang)
        conn.commit()
    except:
        print(record)
        with open("./ErrorDatas"  + ".text", "a+") as f:
            f.write(str(record) + '\n')




