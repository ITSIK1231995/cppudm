import os

SLEEP_COMMAND = 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'

class sleep(object):
    def getKey(self):
        return (type(self).__name__)

    @staticmethod
    def runOp(hostPcServerRef,socket,parm):
        os.system(SLEEP_COMMAND)