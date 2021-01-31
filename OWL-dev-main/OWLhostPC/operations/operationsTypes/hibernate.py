import os
CMD_COMMAND = 'cmd /k '
HIBERNATE_COMMAND = 'shutdown /h'

class hibernate(object):
    def __init__(self):
        pass

    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def runOp(socket,parm):
        os.system(CMD_COMMAND + HIBERNATE_COMMAND)