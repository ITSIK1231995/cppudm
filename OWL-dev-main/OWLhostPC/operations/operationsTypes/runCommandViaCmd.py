import subprocess # CMD commands and outputs
import os
CMD_COMMAND = 'cmd /k '

class runCommandViaCMD(object):
    def __init__(self):
        pass

    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def runOp(userCommand):
        return subprocess.run([userCommand], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # os.system("shutdown /s /t 1")