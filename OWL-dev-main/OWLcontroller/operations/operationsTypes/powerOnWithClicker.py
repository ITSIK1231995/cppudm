import os
import socket
import time
from operations.operation import operation
PING = 'ping '
#SHUTDOWN_COMMAND = "shutdown command request from client"
SHUTDOWN_COMMAND = "shutdown /s /t 1"

class powerOnWithClicker(operation):
    CLICKER_CHANNEL_COMMANDS ={1 : ('1', 'q'),
                             2 : ('2', 'w'),
                             3 : ('3', 'e'),
                             4 : ('4', 'r')}
    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    # @staticmethod
    # def checkIfPcisOn(self,controllerPc,hostPc):
    #     clientSocket = socket.socket()  # instantiate
    #     port = controllerPc.configs.defaultConfContent['hostPcServerPort']
    #     try:
    #         clientSocket.connect((hostPc["IP"], port))  # connect to the server
    #     except socket.error as e:
    #         print(e)
    #         return False
    #     return clientSocket


    def runOp(self,controllerPc,hostPc,opParams):
        os.system("echo " + powerOnWithClicker.CLICKER_CHANNEL_COMMANDS[hostPc['clicker']['chanel']][0] +
                  " > " + hostPc['clicker']['COM'])
        time.sleep(0.5)
        os.system("echo " + powerOnWithClicker.CLICKER_CHANNEL_COMMANDS[hostPc['clicker']['chanel']][1] +
                  " > " + hostPc['clicker']['COM'])

        # check if the host is on
        hostStatus = operation.checkIfPcisOn(self,controllerPc,hostPc)
        return hostStatus # if the host is up the clicker done well, and should return True



