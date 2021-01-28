import os

from operations.operation import operation
import json

from operations.operationWithSocket import operationWithSocket

PING = 'ping '
#SLEEP_COMMAND ="hibernate command request from client new"
HIBERNATE_COMMAND = 'shutdown /h'

class hibernate(operationWithSocket):
    def getKey(self):
        pass


    def runOp(self,controllerPc,hostPc,opParams):
        controllerPc.updateRunTimeState(hostPc, " \n hibernate operation has started \n ")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self,controllerPc,hostPc)
        if not socket:
            #controllerPc.updateRunTimeState(hostPc, "\nhibernate could not being made as socket creating has failed")
            return False
        controllerPc.updateRunTimeState(hostPc, "\n Socket has been created")
        messegeToServer = {"operation": "hibernate"}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        controllerPc.updateRunTimeState(hostPc, "\n hibernate msg has been sent to server")
        socket.close()
        controllerPc.updateRunTimeState(hostPc, "\n Socket has been closed")
        hostPcIsOff = operation.waitForPcToTurnOff(self, controllerPc, hostPc) # Verify the host is down
        if hostPcIsOff:
            controllerPc.updateRunTimeState(hostPc, "\n hibernate done successfully ! ")
        else:
            controllerPc.updateRunTimeState(hostPc, "\n hibernate operation has failed ! ")
        return hostPcIsOff