import subprocess # CMD commands and outputs
import time
CMD_COMMAND = 'cmd /k '

class runCommandViaCMD(object):
    def __init__(self):
        pass

    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def runOp(hostPcServerRef,socket,parm):
        data = subprocess.run([parm], stdout=subprocess.PIPE).stdout.decode('utf-8')
        time.sleep(5)
        socket.send(data.encode())  # send data to the client
