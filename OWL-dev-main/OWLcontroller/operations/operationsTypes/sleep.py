import os

from operations.operation import operation
import json
PING = 'ping '
#SLEEP_COMMAND ="sleep command request from client"
SLEEP_COMMAND = 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'

class sleep(operation):
    def getKey(self):
        pass

    @staticmethod
    def runOp(hostPc,opParams):

        messegeToServer = {"operation": "sleep", "param": SLEEP_COMMAND}
        opParams.socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        pingCommand = PING + opParams.hostIP
        while (os.system(pingCommand)) == 0:
            print ("Host still alive")
        if (os.system(pingCommand)) != 0:
            print ("sleep was done")
            return True