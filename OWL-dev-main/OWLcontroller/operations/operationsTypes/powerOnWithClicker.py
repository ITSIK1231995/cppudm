import os
import subprocess
import time

from operations.operationsTypes.runCommandViaCmd import runCommandViaCmd
CMD_COMMAND = 'cmd /k '

class powerOnWithClicker():
    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)
    @staticmethod
    def runOp():
        # os.system(CMD_COMMAND + 'mode COM4 BAUD=9600 PARITY=n DATA=8')

        # time.sleep(1)
        #os.system(CMD_COMMAND + 'echo 1 > COM4')
        # # os.system(CMD_COMMAND + 'ipconfig')
        #os.system(CMD_COMMAND + 'echo q > COM4')
        print("done")
        #os.system(CMD_COMMAND + 'timeout 1')
        # os.system("start /B start cmd.exe @cmd /k echo 1 > COM4")
        # os.system("start /B start cmd.exe @cmd /k echo q > COM4")

print (powerOnWithClicker.runOp())


#
# mode COM4 BAUD=9600 PARITY=n DATA=8
# echo 1 > COM4
# timeout 1
# echo q > COM4
# timeout 1




