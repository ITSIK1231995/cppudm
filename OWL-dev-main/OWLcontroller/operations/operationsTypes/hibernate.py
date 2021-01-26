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
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        socket = operationWithSocket.createCommunication(self, hostPc["IP"], port)

        messegeToServer = {"operation": "hibernate", "param": HIBERNATE_COMMAND}
        socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        socket.close()

        hostPcIsOn = operation.checkIfPcisOn(self, controllerPc, hostPc) # Verify the host is down
        return not hostPcIsOn