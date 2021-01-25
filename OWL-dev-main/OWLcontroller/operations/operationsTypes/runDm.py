import json
import time

from operations.operation import operation

class runDM(object):
    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def runOp(hostPc,opParams):
        messegeToServer = {"operation": "shutdown", "param": opParams.paramForOperation}
        opParams.socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        #messegeFromServer = opParams.socket.recv(1024).decode()  # receive response from the server

# TODO implement runDM


