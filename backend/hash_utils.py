import hmac
import hashlib
import random

def generate_salt():
    letters = '1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmQWERUIOPASDFGHJKLZXCVBNM[\;{}|'
    salt = ''
    for x in range(0, 30):
        salt += letters[random.randint(0, len(letters)-1)]
    return salt

def get_salt():
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    return credentials.hash.find_one({"salt":{"$exists":True}})["salt"]
    

def hmac_hash(password, key):
    h = hmac.new(key.encode('utf-8'), password.encode('utf-8'), hashlib.sha256)
    return h.hexdigest()

def store_salt(key):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    credentials.hash.remove({"salt":{"$exists":True}}) # delete the salt
    credentials.hash.insert({"salt":key})
    return

def store_password(digest):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    #credentials.hash.delete_many({})
    #credentials.hash.insert({'digest':digest, 'key':key})
    credentials.hash.remove({"digest":{"$exists":True}}) # delete the hashed password
    credentials.hash.insert({'digest':digest})
    return

def get_password_digest(username):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    # data = credentials.hash.find_one({'username'username})
    # we're not using multiple users, so this one thing is fine.
    data = credentials.hash.find_one({'digest':{"$exists":True}}) # should be only one in the database
    if (data==None):
        return None
    print(data)
    return data['digest']
