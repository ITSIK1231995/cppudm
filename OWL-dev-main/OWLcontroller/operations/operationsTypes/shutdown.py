from operations.operation import operation
import json
from operations.operationWithSocket import operationWithSocket

class shutdown(operationWithSocket):
    def getKey(self):
        pass

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return False

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return True

    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n shutdown command has started")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self,controllerPc,hostPc,testLog)
        if not socket:
            controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n shutdown could not being made as socket creating has failed")
            return False
        messegeToServer = {"operation": "shutdown"}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        socket.close()
        # Verify the host is down
        hostPcIsOFf = operation.waitForPcToTurnOff(self,controllerPc,hostPc,testLog)
        if hostPcIsOFf:
            controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n shutdown command has ended successfully")
        else:
            controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n shutdown command has Failed")
        return hostPcIsOFf



