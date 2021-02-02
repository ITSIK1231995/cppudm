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

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return True

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return False

    #TODO : add first line from matan script
    def runOp(self,controllerPc,hostPc,opParams):
        controllerPc.updateRunTimeState(hostPc,"\n Power on with clicker has started \n")
        controllerPc.updateRunTimeState(hostPc, "\nActivate Clicker\n" )
        os.system("mode " + hostPc['clicker']['COM'] + " BAUD=9600 PARITY=n DATA=8")
        os.system("echo " + powerOnWithClicker.CLICKER_CHANNEL_COMMANDS[hostPc['clicker']['chanel']][0] +
                  " > " + hostPc['clicker']['COM'])
        time.sleep(0.5)
        os.system("echo " + powerOnWithClicker.CLICKER_CHANNEL_COMMANDS[hostPc['clicker']['chanel']][1] +
                  " > " + hostPc['clicker']['COM'])

        # check if the host is on
        hostPcIsOn = operation.waitForPcToTurnOn(self,controllerPc,hostPc)

        if hostPcIsOn:
            controllerPc.updateRunTimeState(hostPc, "\n Host Pc is On\n power On With Clicker done successfully ! ")
        else:
            controllerPc.updateRunTimeState(hostPc, "\n Host Pc is Off\n power On With Clicker Failed ! ")

        controllerPc.updateRunTimeState(hostPc, "\n Power on with clicker has ended \n")
        return hostPcIsOn # if the host is up the clicker done well, and should return True



