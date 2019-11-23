import pyinotify, subprocess, select, re, requests, datetime
from subprocess import Popen, PIPE
from time import strptime

def authLogNewMessage(arg):
    f = subprocess.Popen(['tail', '-F', '/var/log/auth.log'],\
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    url = 'http://localhost:9000/failed_login'

    while True:
        if p.poll(1):
            message = f.stdout.readline().decode().split()
            validMessage = False
            if (re.search("^sshd.", message[4])):
                if (message[5] == "Failed"):
                    ip = message[10]
                    validMessage = True
                elif (message[5] == "Connection" and (message[6] == "reset" or message[6] == "closed")):
                    ip = message[11]
                    validMessage = True
            elif (re.search("^phpMyAdmin.", message[4])):
                if (message[5] + message[6] == "userdenied:"):
                    ip = message[10]
                    validMessage = True
            if validMessage:
                month = strptime(message[0], '%b').tm_mon
                day = int(message[1])
                time = message[2].split(':')
                seconds = datetime.datetime(2019, month, day, int(time[0]), int(time[1]), int(time[2])).timestamp()
                print(seconds)
                print(ip)
                data = {'ip':ip, 'time':seconds}
                requests.post(url, json = data)

def sysLogNewMessage(arg):
    f = subprocess.Popen(['tail', '-F', '/var/log/syslog'],\
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    url = 'http://localhost:9000/failed_login'

    while True:
        if p.poll(1):
            message = f.stdout.readline().decode().split()
            if (re.search("^drupal.", message[4])):
                if (message[7] == "failed"):
                    ip = message[9]
                    month = strptime(message[0], '%b').tm_mon
                    day = int(message[1])
                    time = message[2].split(':')
                    seconds = datetime.datetime(2019, month, day, int(time[0]), int(time[1]), int(time[2])).timestamp()
                    print(seconds)
                    print(ip)
                    data = {'ip':ip, 'time':seconds}
                    requests.post(url, json = data)


watchManager = pyinotify.WatchManager()
watchManager.add_watch('/var/log/auth.log', pyinotify.IN_MODIFY, authLogNewMessage)
watchManager.add_watch('/var/log/syslog', pyinotify.IN_MODIFY, sysLogNewMessage)

eventNotifier = pyinotify.Notifier(watchManager)
print("Awaiting new messages...")
eventNotifier.loop()
