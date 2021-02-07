import json
import time

from operations.operation import operation
from operations.operationWithSocket import operationWithSocket


class runDM(operationWithSocket):
    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return True

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return True


    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateRunTimeState(hostPc,testLog, "\n Run Dm command has started \n ")
        socket = operationWithSocket.createCommunication(self, controllerPc,hostPc,testLog)
        if (socket == False):
            return False
        messegeToServer = {"operation": "runDM", "param": opParams[0]}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        messegeFromServer = socket.recv(1024).decode()  # receive response from the server
        socket.close()
        controllerPc.updateRunTimeState(hostPc,testLog, "\n message from server:\n" +messegeFromServer)
        controllerPc.updateRunTimeState(hostPc,testLog, "\n Run Dm command has ended")

# TODO implement runDM - bug  after 3 times in a row of running this with the server socket is failling


