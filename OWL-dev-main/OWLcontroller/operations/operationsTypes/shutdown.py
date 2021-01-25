import errno
import os
import socket
from collections import namedtuple
from ssl import socket_error

from operations.operation import operation
import json
PING = 'ping '
#SHUTDOWN_COMMAND = "shutdown command request from client"
SHUTDOWN_COMMAND = "shutdown /s /t 1"
class shutdown(operation):
    def getKey(self):
        pass



    @staticmethod
    def runOp(hostPc,opParams):

        messegeToServer = {"operation": "shutdown", "param": SHUTDOWN_COMMAND}
        opParams.socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        opParams.socket.close()

        # # Verify the host is down
        # clientSocket = opParams.socket.socket()  # instantiate
        # try:
        #     clientSocket.connect((opParams.hostIp, opParams.port))  # connect to the server
        # except opParams.socket.error as e:
        #     print(e)
        #     return False

        # Verify the host is down
        clientSocket = socket.socket()  # instantiate
        try:
            clientSocket.connect((opParams.hostIP, opParams.port))  # connect to the server
        except socket.error as e:
            return True # No socket as PC is down as expected


