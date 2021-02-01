import os
CMD_COMMAND = 'cmd /k '

class shutdown(object):
    def __init__(self):
        pass

    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def runOp(hostPcServerRef,socket,parm):
        os.system("shutdown /s /t 1")