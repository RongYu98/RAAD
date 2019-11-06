from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from datetime import datetime
import pymongo
import time as TIME
import utils

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient("mongodb://localhost:27017/")
login_records = client["login_records"]

tolerance_time = 30 # in secnonds
attempt_limit = 3 # number of attempts within the timespan limit before calling ban
ban_time = 3600 # in seconds

@app.route('/failed_login', methods=['POST'])
def record_failed_login():
    info = request.json # subject to change
    ip_address = info['ip']
    time = info['time']

    failed = login_records.failed
    login_records.failed.insert(
        {"ip":ip_address, "time":time}) # time shall be converted to seconds
    attempts = db.accounts.find({"ip":ip_address})
    t = time.time()
    failedWithinTime = 0
    for attempt in attempts:
        time = attempts["time"]
        if (t-time < timespan_limit):
            failedWithinTime += 1
    if failedWithinTime > attempt_limit:
        blacklistIP(ip_address)
        return jsonify(status="BANNED")
    else:
        return jsonify(status="Let's wait")

def blacklistIP(ip_address):
    if (login_records.ban.find_one({'ip':ip_address})==None):
        utils.ban(ip_address)
        login_records.ban.insert(
            {'ip':ip_address, 'start_time':TIME.time(), 'duration':ban_time})
        # SCHEDULE EVENT TO WHITELIST
        # THEN SAVE THE BANNING INTO A DICTIONARY, TO CANCEL IF THEY CHANGE THE TIME

    # else do nothing? they already banned?
    return None
def whitelistIP(ip_address):
    # CHECK TO SEE IF IT"S BEEN SCHEDULED, remove if it has?
    utils.unban(ip_address)
    login_records.ban.delete_many({'ip':ip_address})
    return None
    
    
@app.route('/successful_login', methods=['POST'])
def record_successful_login():
    info = request.json
    ip_address = info['ip']
    time = info['time']
    if login_records.failed.find_one({"ip":ip_address})==None:
        return jsonify(status="Great Kid")
    else:
        login_records.failed.delete_many({"ip":ip_address})
        return jsonify(status="Delinquet Pardoned")
    
@app.route('/get_threshold', methods=['GET'])
def get_threshold():
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
        if ("findtime" in info):
            tolerance_time = int(info["findtime"])
        if ("maxretry" in info):
            attempt_limit = int(info["maxretry"])
        if ("bantime" in info):
            ban_time = int(info["bantime"])
    except Exception as e:
        return jsonify(status=500, result='failed', detail=e)
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
    whitelistIP(info['ip'])
    return jsonify(status=200, result='success')

@app.route('/blacklist_ip', methods=['POST'])
def blacklist_blacklisted_ip():
    info = request.form
    if ("ip" not in info):
        return jsonify(status=500, result='failed', details='IP Address not specified')
    blacklistIP(info["ip"])
    return jsonify(status=200, result='success')


if __name__ == "__main__":
    # login_records.ban.insert({'ip':'1.1.1.1', 'time':TIME.time(), 'duration':ban_time})
    blacklistIP('2.2.2.2')
    app.run(host='0.0.0.0', port=9000, debug=True)
    
