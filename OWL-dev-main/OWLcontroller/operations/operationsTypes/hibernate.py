import os

from operations.operation import operation
import json
PING = 'ping '
#SLEEP_COMMAND ="hibernate command request from client new"
SLEEP_COMMAND = 'shutdown /h'

class hibernate(operation):
    def getKey(self):
        pass

    @staticmethod
    def runOp(hostPc,opParams):

        messegeToServer = {"operation": "hibernate", "param": SLEEP_COMMAND}
        opParams.socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        messegeFromServer = opParams.socket.recv(1024).decode()  # receive response from the server
        opParams.socket.close()

        # sending a ping in order to verify the shutdown
        pingCommand = PING + opParams.hostIP
        while (os.system(pingCommand)) == 0:
            print ("Host still alive")
        if (os.system(pingCommand)) != 0:
            print ("hibernate was done")
            return True