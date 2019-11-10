import pyinotify, subprocess, select, re, requests, datetime
from subprocess import Popen, PIPE
from time import strptime

def newMessage(arg):
    f = subprocess.Popen(['tail', '-F', '/var/log/auth.log'],\
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    url = 'localhost:9000/failed_login'

    while True:
        if p.poll(1):
            message = f.stdout.readline().decode().split()
            if (re.search("^sshd.", message[4])):
                validMessage = False
                if (message[5] == "Failed"):
                    ip = message[10]
                    validMessage = True
                elif (message[5] + message[6] == "Connectionreset"):
                    ip = message[11]
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

watchManager = pyinotify.WatchManager()
watchManager.add_watch('/var/log/auth.log', pyinotify.IN_MODIFY, newMessage)

eventNotifier = pyinotify.Notifier(watchManager)
eventNotifier.loop()
