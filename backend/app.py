from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from datetime import datetime
import pymongo
import time as TIME

import os

from threading import Timer
import utils
import hash_utils


app = Flask(__name__)
CORS(app)

events = {} # basically ip address to whitelisting

client = pymongo.MongoClient("mongodb://localhost:27017/")
login_records = client["login_records"]

tolerance_time = 60 # in minutes
attempt_limit = 3 # number of attempts within the timespan limit before calling ban
ban_time = 10 # in seconds

@app.route('/failed_login', methods=['POST'])
def record_failed_login():
    info = request.json # subject to change
    ip_address = info['ip']
    time = info['time']
    source = info['source']
    failed = info['failed']

    if (failed==False):
        return record_successful_login()
    
    failed = login_records.failed
    login_records.failed.insert(
        {"ip":ip_address, "time":time, 'source':source}) # time shall be converted to seconds
    attempts = login_records.failed.find({"ip":ip_address, 'source':source})
    
    t = TIME.time()
    failedWithinTime = 0
    for attempt in attempts:
        print(attempt)
        time = attempt["time"]
        if (t-time < tolerance_time):
            failedWithinTime += 1
    print(failedWithinTime)
    if failedWithinTime >= attempt_limit:
        blacklistIP(ip_address)
        return jsonify(status="BANNED")
    else:
        return jsonify(status="Let's wait")

def blacklistIP(ip_address):
    print(ip_address)
    data = login_records.ban.find_one({'ip':ip_address})
    if (data==None or data==False):
        utils.ban(ip_address)
        login_records.ban.insert(
            {'ip':ip_address, 'start_time':TIME.time(), 'duration':ban_time})

        print("ban_time "+str(ban_time))
        
        events[ip_address] = Timer(ban_time, whitelistIP, kwargs={"ip_address":ip_address})
        events[ip_address].start()
        print("Scheduled whitelisting")
        return True
    # else do nothing? they already banned?

    return False
def whitelistIP(ip_address):
    # CHECK TO SEE IF IT"S BEEN SCHEDULED, remove if it has?
    utils.unban(ip_address)
    print(ip_address)
    print("WHITELISTED")
    if (ip_address in events):
        del events[ip_address]
        
    login_records.ban.delete_many({'ip':ip_address})
    return None

    
@app.route('/successful_login', methods=['POST'])
def record_successful_login():
    info = request.json
    ip_address = info['ip']
    time = info['time']
    source = info['source']
    
    if login_records.failed.find_one({"ip":ip_address, 'source':source})==None:
        return jsonify(status="Great Kid")
    else:
        login_records.failed.delete_many({"ip":ip_address, 'source':source})
        return jsonify(status="Delinquet Pardoned")
    
@app.route('/get_threshold', methods=['GET'])
def get_threshold():
    print
    
    global tolerance_time
    global attempt_limit
    global ban_time

    data = {'maxretry':attempt_limit, 'findtime':tolerance_time, 'bantime':ban_time}
    return jsonify(status=200, result='success', detail=data)

@app.route('/set_threshold', methods=['PUT'])
def set_threshold():
    info = request.values
    global tolerance_time
    global attempt_limit
    global ban_time

    ## need to have them all together
    try:
        print(info)
        if ("findtime" in info):
            tolerance_time = int(info["findtime"])
        if ("maxretry" in info):
            attempt_limit = int(info["maxretry"])
        if ("bantime" in info):
            ban_time = int(info["bantime"])
    except Exception as e:
        return jsonify(status=500, result='failed', detail=e)
    thresholds = login_records.thresholds.find_one({'ban_time':{"$exists":True},
                                                    'tolerance_time':{"$exists":True},
                                                    'attempt_limit':{"$exists":True}})
    print(thresholds)
    login_records.thresholds.update(thresholds, {'ban_time':ban_time,
                                                 'tolerance_time':tolerance_time,
                                                 'attempt_limit':attempt_limit})
    print(tolerance_time, attempt_limit, ban_time)

        
    return jsonify(status=200, result='success')

@app.route('/blacklisted_ips', methods=['GET'])
def get_blacklisted_ips():
    ips = []
    cursor = login_records.ban.find({})
    for doc in cursor:
        ips.append({'ip':doc['ip']})
    return jsonify(status=200, result='success', detail=ips)

@app.route('/remove_blacklisted_ip', methods=['DELETE'])
def remove_blacklisted_ip():
    info = request.values
    if ('ip' not in info):
        return jsonify(status=500, result='failed', details='IP Address not specified')
    if (info['ip'] not in events):
        return jsonify(status=500, result='failed', details='IP Address not banned')
    events[info['ip']].cancel() # halt the timer, and then manually call it
    whitelistIP(info['ip'])
    return jsonify(status=200, result='success')

@app.route('/blacklist_ip', methods=['POST'])
def blacklist_blacklisted_ip():
    info = request.form
    if ("ip" not in info):
        return jsonify(status=500, result='failed', details='IP Address not specified')
    if (blacklistIP(info["ip"])): # sucessfully blacklisted
        return jsonify(status=200, result='success')
    return jsonify(status=500, result='failed', details='IP Address already banned.')

@app.route('/get_random_salt', methods=['GET'])
def random_salt():
    salt = hash_utils.generate_salt()
    hash_utils.store_salt(salt)
    return jsonify(status=200, result='success', detail=salt)

@app.route('/get_current_salt', methods=['GET'])
def get_salt():
    salt = hash_utils.get_salt() # salt should never be None unless something went wrong...
    return jsonify(status=200, result='success', detail=salt)


@app.route('/set_password', methods=['POST'])
def set_password():
    info = request.values
    if ('password' not in info or 'username' not in info):
        return jsonify(status=500, result='failed', detail='missing password or username')
    hash_utils.store_password(info['password'])
    return jsonify(status=200, result="success", detail="Set")

@app.route('/check_password', methods=['POST'])
def check_password():
    info = request.values
    if ('password' not in info or 'username' not in info):
        return jsonify(status=500, result='failed', detail='missing password or username')
    digest = hash_utils.get_password_digest(info['username'])
    print(digest)
    if (digest==info['password']):
        return jsonify(status=200, result='success')
    return jsonify(status=500, result='failed', detail='Wrong password')

def startup():
    # function to initiate ban-values, and to check past blacklistings
    
    global tolerance_time # 5
    global attempt_limit # 3
    global ban_time # 3600

    data = login_records.thresholds.find_one({'ban_time':{"$exists":True},
                                              'tolerance_time':{"$exists":True},
                                              'attempt_limit':{"$exists":True}})
    print(data)
    if (data==None):
        tolerance_time = 5 # minutes
        attempt_limit = 3 # tries
        ban_time = 3600 # seconds
        print("data initiated")
        login_records.thresholds.insert({'ban_time':3600,
                                         'tolerance_time':5,
                                         'attempt_limit':3})
    else:
        tolerance_time = data['tolerance_time']
        ban_time = data['ban_time']
        attempt_limit = data['attempt_limit']

    data = login_records.ban.find({})
    
    for d in data:
        if (d==None):
            continue
        print(d)
        time = d['start_time']+d['duration'] - TIME.time() # basically, see if it should still be banned
        if (time < 1): # if should be whitelisting in 1 second or less, then it will whitelist now
            whitelistIP(d['ip'])
        else: # schedule whitelisting
            events[d['ip']] = Timer(time, whitelistIP, kwargs={"ip_address":d['ip']})
            events[d['ip']].start()

    
if __name__ == "__main__":
    startup()
    # login_records.ban.insert({'ip':'1.1.1.1', 'time':TIME.time(), 'duration':ban_time})
    # blacklistIP('7.4.2.4')
    # app.run(host='0.0.0.0', port=9000, debug=True)
    # app.run(host='0.0.0.0', port=9000, debug=True, ssl_context=('adhoc'))
    # app.run(host='0.0.0.0', port=9000, debug=True, ssl_context=('/etc/ssl/certs/raad.crt', '/etc/ssl/certs/raad.key'))
    if (os.path.isfile('/etc/ssl/certs/raad.crt') and os.path.isfile('/etc/ssl/certs/raa.key')):
        app.run(host='0.0.0.0', port=9000, debug=True, ssl_context=('/etc/ssl/certs/raad.crt', '/etc/ssl/certs/raa.key'))
    else:
        app.run(host='0.0.0.0', port=9000, debug=True, ssl_context=('adhoc'))
