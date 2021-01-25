import os
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

    @staticmethod
    def runOp(hostPc,opParams):
        os.system("echo " + powerOnWithClicker.CLICKER_CHANNEL_COMMANDS[hostPc['clicker']['chanel']][0] +
                  " > " + hostPc['clicker']['COM'])
        time.sleep(0.5)
        os.system("echo " + powerOnWithClicker.CLICKER_CHANNEL_COMMANDS[hostPc['clicker']['chanel']][1] +
                  " > " + hostPc['clicker']['COM'])

        #check if the host turned on
        pingCommand = PING + hostPc["IP"]
        while (os.system(pingCommand)) != 0:
            print ("Host is not  alive")
        if (os.system(pingCommand)) == 0:
            print ("host is up")

        return True
# powerOnWithClicker.runOp('COM4', 1)
# powerOnWithClicker.runOp('COM4', 2)
# powerOnWithClicker.runOp('COM4', 3)
# powerOnWithClicker.runOp('COM4', 4)

