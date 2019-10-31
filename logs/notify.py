import pyinotify
from subprocess import Popen, PIPE

def newMessage(arg):
    proc = Popen(['tail', '-5', '/var/log/auth.log'], stdout=PIPE)
    res = proc.communicate()
    print(res[0].decode())

watchManager = pyinotify.WatchManager()
watchManager.add_watch('/var/log/auth.log', pyinotify.IN_MODIFY, newMessage)

eventNotifier = pyinotify.Notifier(watchManager)
eventNotifier.loop()
