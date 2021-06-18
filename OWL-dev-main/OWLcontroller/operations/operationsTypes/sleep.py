from operations.operation import operation
import json
from operations.operationWithSocket import operationWithSocket
PING = 'ping '

class sleep(operationWithSocket):
    def getKey(self):
        pass

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return False

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return True

    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Sleep command has started")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self,controllerPc,hostPc,testLog)
        if not socket:
            print ("\n Sleep could not being made as socket creating has failed")
            return False
        messegeToServer = {"operation": "sleep"}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        socket.close()
        hostPcIsOff = operation.waitForPcToTurnOff(self, controllerPc, hostPc,testLog) # Verify the host is down
        controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Sleep command has ended")
        return hostPcIsOff