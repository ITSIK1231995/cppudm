import json
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
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nDrive Master operation has started \n ")
        socket = operationWithSocket.createCommunication(self, controllerPc,hostPc,testLog)
        if (socket == False):
            return False
        messegeToServer = {"operation": "runDM", "param": opParams[0]}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog,"\nDrive Master request has been sent to the System Under Test")
        messegeFromServer = socket.recv(1024).decode()  # receive response from the server
        socket.close()
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n Message from server:\n" + "\n" + messegeFromServer + "\n")
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nDrive Master operation has ended")
        return True



