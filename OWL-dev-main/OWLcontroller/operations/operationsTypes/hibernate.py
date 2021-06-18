from operations.operation import operation
import json
from operations.operationWithSocket import operationWithSocket
PING = 'ping '
HIBERNATE_COMMAND = 'shutdown /h'

class hibernate(operationWithSocket):
    def getKey(self):
        pass

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return True

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return False


    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateTerminalAndLog(hostPc, testLog, " \n Hibernate operation has started \n ")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self,controllerPc,hostPc,testLog)
        if not socket:
            #controllerPc.updateRunTimeState(hostPc, "\nhibernate could not being made as socket creating has failed")
            return False
        controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Communication has been created")
        messegeToServer = {"operation": "hibernate"}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Hibernate request has been sent to server")
        socket.close()
        controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Communication has been closed")
        hostPcIsOff = operation.waitForPcToTurnOff(self, controllerPc, hostPc, testLog) # Verify the host is down
        if hostPcIsOff:
            controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Hibernate done successfully")
        else:
            controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Hibernate operation has failed")
        return hostPcIsOff