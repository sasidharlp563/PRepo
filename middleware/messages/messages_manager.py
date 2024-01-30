import mysql.connector
import os
import shortuuid


host = os.environ.get('DB_HOST', 'localhost')  
user = os.environ.get('DB_USER')  
password = os.environ.get('DB_PASSWORD') 
database = os.environ.get('DB_NAME','vault')
port = os.environ.get('DB_PORT', 3306)  

def create_message(account_id, sender_number, receiver_number):
    if len(account_id)!=10 or not(account_id.isdigit()):
        return 200, "Success", dict(errorMessage="Account id should be at length of 10 characters")
    elif len(sender_number)!=10 or not(sender_number.isdigit()):
        return 200, "Success", dict(errorMessage=" Please share a valid sender number in 10 digits without countrycode")
    elif len(receiver_number)!=10 or not(receiver_number.isdigit()):
        return 200, "Success", dict(errorMessage=" Please share a valid receiver number in 10 digits without countrycode")
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        uuid=shortuuid.ShortUUID().random(length=16)
        query = f"INSERT INTO vault.messages(message_id,account_id,sender_no,receiver_no) VALUES(\"{uuid}\",{account_id},{sender_number},{receiver_number})"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return 200, "Success", dict(message_id=uuid)
    except Exception as e:
        return 500, "Error", dict(errorMessage="Database connection failed or error in the query {e}")


def get_messages(account_id):
    if len(account_id)!=10 or not(account_id.isdigit()):
        return 200, "Success", dict(errorMessage="Account id should be at length of 10 characters")
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        query = f"SELECT * from vault.messages where account_id={account_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        keys=['message_id','account_id','sender_no','receiver_no']
        result=[]
        for row in rows:
            temp = {key: value for key, value in zip(keys, row)}
            result.append(temp)
        conn.commit()
        cursor.close()
        conn.close()
        return 200, "Success", dict(messages=result)
    except Exception as e:
        return 500, "Error", dict(errorMessage="Database connection failed or error in the query {e}")

def search_message(message_id, sender_no, receiver_no):
    if len(message_id)!=16:
        return 200, "Success", dict(errorMessage="Please share a valid 16 digit message_id")
    elif len(sender_no)!=10 or not(sender_no.isdigit()):
        return 200, "Success", dict(errorMessage=" Please share a valid sender number in 10 digits without countrycode")
    elif len(receiver_no)!=10 or not(receiver_no.isdigit()):
        return 200, "Success", dict(errorMessage=" Please share a valid receiver number in 10 digits without countrycode")
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        query = "SELECT * FROM vault.messages WHERE"
        conditions = []
        if message_id is not None:
            conditions.append(f" message_id = '{message_id}'")
        if sender_no is not None:
            conditions.append(f" sender_no = '{sender_no}'")
        if receiver_no is not None:
            conditions.append(f" receiver_no = '{receiver_no}'")
        query += " AND ".join(conditions)
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        keys=['message_id','account_id','sender_no','receiver_no']
        result=[]
        for row in rows:
            temp = {key: value for key, value in zip(keys, row)}
            result.append(temp)
        conn.commit()
        cursor.close()
        conn.close()
        return 200, "Success", dict(messages=result)
    except Exception as e:
        return 500, "Error", dict(errorMessage="Database connection failed or error in the query {e}")