from datetime import time
import time
from operations.operation import operation
import json

from operations.operationWithSocket import operationWithSocket


class runCommandViaCmd(operationWithSocket):
    def getKey(self):
        ''' Returns operation's name '''
        return type(self).__name__

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return True

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return True

    def runOp(self,controllerPc,hostPc,opParams):
        controllerPc.updateRunTimeState(hostPc, " \n run Command Via Cmd started \n ")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self,controllerPc,hostPc)
        if socket == False:
            return False
        df1 = {"operation": "runCommandViaCmd", "param": opParams[0]}
        socket.sendall(json.dumps(df1).encode('utf-8'))  # encode the dict to JSON
        data = socket.recv(1024).decode()  # receive response from the server
        socket.close()
        controllerPc.updateRunTimeState(hostPc, "run command via cmd has done with the following data: \n " +data) # show the response in terminal
        return data != ""



        #message = input(" -> ")  # again send a messege to the server

