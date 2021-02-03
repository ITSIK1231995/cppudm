import errno
import os
import socket
from collections import namedtuple
from ssl import socket_error

from operations.operation import operation
import json

from operations.operationWithSocket import operationWithSocket

# PING = 'ping '
#SHUTDOWN_COMMAND = "shutdown command request from client"
# SHUTDOWN_COMMAND = "shutdown /s /t 1"
class shutdown(operationWithSocket):
    def getKey(self):
        pass




    def runOp(self,controllerPc,hostPc,opParams):
        controllerPc.updateRunTimeState(hostPc, "\n shutdown command has started")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self,controllerPc,hostPc)
        if not socket:
            controllerPc.updateRunTimeState(hostPc, "\n shutdown could not being made as socket creating has failed")
            return False
        messegeToServer = {"operation": "shutdown"}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        socket.close()

        # Verify the host is down
        hostPcIsOFf = operation.waitForPcToTurnOff(self,controllerPc,hostPc)
        if hostPcIsOFf:
            controllerPc.updateRunTimeState(hostPc, "\n shutdown command has ended successfully")
        else:
            controllerPc.updateRunTimeState(hostPc, "\n shutdown command has Failed")
        return hostPcIsOFf



