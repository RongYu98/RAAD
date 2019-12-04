import subprocess, select, re, requests, datetime
from subprocess import Popen, PIPE
from time import strptime
from time import sleep

sleep(5)

f1 = subprocess.Popen(['tail', '-F', '/var/log/auth.log'],\
    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
f2 = subprocess.Popen(['tail', '-F', '/var/log/syslog'],\
    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
f3 = subprocess.Popen(['tail', '-F', '/var/www/html/mediawiki/extensions/RAADMW/RAADMW.log'],\
    stdout = subprocess.PIPE, stderr = subprocess.PIPE)

p1 = select.poll()
p1.register(f1.stdout)
p2 = select.poll()
p2.register(f2.stdout)
p3 = select.poll()
p3.register(f3.stdout)

print("Checked Auth Log")
url = 'https://localhost:9000/failed_login'

while True:
    if p1.poll(1):
        print("SSH Checked")
        message = f1.stdout.readline().decode().split()
        validMessage = False
        source = None
        failed = True
        repeat = 1
        if (re.search("^sshd.", message[4])):
            source = 'ssh'
            if (message[5] == "Failed"):
                ip = message[10]
                validMessage = True
            elif (message[5] == "Connection" and (message[6] == "reset" or message[6] == "closed")):
                ip = message[11]
                validMessage = True
            elif (message[5] + message[6] == "Acceptedpublickey"):
                ip = message[10]
                validMessage = True
                failed = False
        elif (re.search("^phpMyAdmin.", message[4])):
            source = 'php'
            if (message[5] + message[6] == "userdenied:"):
                ip = message[10]
                validMessage = True
            if (message[5] + message[6] == 'userauthenticated:'):
                ip = message[9]
                validMessage = True
                failed = False
            if (message[5] + message[6] == 'message repeated' and message[10] + message[11] == 'userdenied:'):
                try:
                    repeat = int(message[7])
                    ip = message[15]
                    validMessage = True
                except:
                    pass
        if validMessage and source:
            month = strptime(message[0], '%b').tm_mon
            day = int(message[1])
            time = message[2].split(':')
            seconds = datetime.datetime(2019, month, day, int(time[0]), int(time[1]), int(time[2])).timestamp()
            print(seconds)
            print(ip)
            data = {'ip':ip, 'time':seconds, 'source':source, 'failed':failed}
            for x in range(repeat):
                requests.post(url, json = data, verify = False)
    if p2.poll(1):
        print("Drupal Checked")
        message = f2.stdout.readline().decode().split()
        validMessage = False
        source = None
        failed = True
        if (re.search("^drupal.", message[4])):
            source = 'drupal'
            if (message[7] == "failed"):
                validMessage = True
            elif (message[6] == "opened"):
                validMessage = True
                failed = False
        if validMessage and source:
            ip = message[5].split("|")[3]
            month = strptime(message[0], '%b').tm_mon
            day = int(message[1])
            time = message[2].split(':')
            seconds = datetime.datetime(2019, month, day, int(time[0]), int(time[1]), int(time[2])).timestamp()
            print(seconds)
            print(ip)
            data = {'ip':ip, 'time':seconds, 'source':source, 'failed':failed}
            requests.post(url, json = data, verify = False)
    if p3.poll(1):
        print("MediaWiki Checked")
        message = f3.stdout.readline().decode().split()
        validMessage = False
        source = 'media'
        failed = True
        if (message[1] == "Failed"):
            validMessage = True
        elif (message[1] == "Successful"):
            validMessage = True
            failed = False
        if validMessage:
            ip = message[4]
            seconds = message[0]
            print(seconds)
            print(ip)
            data = {'ip':ip, 'time':seconds, 'source':source, 'failed':failed}
            requests.post(url, json = data, verify = False)
