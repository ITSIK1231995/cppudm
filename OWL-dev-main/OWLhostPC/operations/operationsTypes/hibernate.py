import os
import sys

CMD_COMMAND = 'cmd /k '
HIBERNATE_COMMAND = 'shutdown /h'

class hibernate(object):
    def __init__(self):
        pass

    def getKey(self):
        return (type(self).__name__)

    @staticmethod
    def runOp(hostPcServerRef,socket,parm):
        socket.close()
        hostPcServerRef.reliseServerScoket()
        os.system(CMD_COMMAND + HIBERNATE_COMMAND)
