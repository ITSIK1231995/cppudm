import json
from operations.operationWithSocket import operationWithSocket

class runCommandViaCmd(operationWithSocket):
    def getKey(self):
        ''' Returns operation's name '''
        return type(self).__name__

    @staticmethod
    def PCOnAfterTest():#Will the pc be on after test finishes
        return True

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc will be on before running
        return True

    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateTerminalAndLog(hostPc, testLog, " \n Run Command Via Cmd started \n ")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self,controllerPc,hostPc,testLog)
        if socket == False:
            return False
        df1 = {"operation": "runCommandViaCmd", "param": opParams[0]}
        socket.sendall(json.dumps(df1).encode('utf-8'))  # encode the dict to JSON
        data = socket.recv(1024).decode()  # receive response from the server
        socket.close()
        controllerPc.updateTerminalAndLog(hostPc, testLog, "run command via cmd has done with the following data: \n " + data) # show the response in terminal
        return data != ""

