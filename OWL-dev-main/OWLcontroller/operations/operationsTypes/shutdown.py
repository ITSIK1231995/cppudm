import errno
import os
import socket
from collections import namedtuple
from ssl import socket_error

from operations.operation import operation
import json

from operations.operationWithSocket import operationWithSocket

PING = 'ping '
#SHUTDOWN_COMMAND = "shutdown command request from client"
SHUTDOWN_COMMAND = "shutdown /s /t 1"
class shutdown(operationWithSocket):
    def getKey(self):
        pass




    def runOp(self,controllerPc,hostPc,opParams):
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self, hostPc["IP"], port)

        messegeToServer = {"operation": "shutdown", "param": SHUTDOWN_COMMAND}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        socket.close()

        # Verify the host is down
        hostPcIsOn = operation.checkIfPcisOn(self,controllerPc,hostPc)
        return not hostPcIsOn



