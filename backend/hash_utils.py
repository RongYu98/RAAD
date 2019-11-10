import hmac
import hashlib
import random

def generate_salt():
    letters = '1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmQWERUIOPASDFGHJKLZXCVBNM[\;{}|'
    salt = ''
    for x in range(0, 30):
        salt += letters[random.randint(0, len(letters)-1)]
    return salt

def store_hash(salt):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    credentials.salt.delete_many({}) # delete everything
    credentials.salt.insert({'salt':salt})
    return

def get_salt():
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    return credentials.salt.find_one({})
    

def hmac_hash(password, key):
    h = hmac.new(key.encode('utf-8'), password.encode('utf-8'), hashlib.sha256)
    return h.digest()

def store_password(digest, key):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    credentials.hash.delete_many({})
    credentials.hash.insert({'digest':digest, 'key':key})
    return

def get_password_digest(username):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    credentials = client["login_credentials"]
    # data = credentials.hash.find_one({'username'username})
    # we're not using multiple users, so this one thing is fine.
    data = credentials.hash.find_one({}) # should be only one in the database
    if (data==None):
        return None
    return data['digest']
