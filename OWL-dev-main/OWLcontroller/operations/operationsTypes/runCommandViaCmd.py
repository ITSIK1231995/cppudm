from datetime import time
import time
from operations.operation import operation
import json

from operations.operationWithSocket import operationWithSocket


class runCommandViaCmd(operationWithSocket):
    def getKey(self):
        ''' Returns operation's name '''
        return type(self).__name__


    def runOp(self,controllerPc,hostPc,opParams):
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self, hostPc["IP"], port)
        if socket == False:
            return False
        df1 = {"operation": "runCommandViaCmd", "param": opParams[0]}
        socket.sendall(json.dumps(df1).encode('utf-8'))  # encode the dict to JSON
        data = socket.recv(1024).decode()  # receive response from the server
        socket.close()
        print ("done",data)
        return data != ""  # show the response in terminal



        #message = input(" -> ")  # again send a messege to the server

