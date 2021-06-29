import time
from operations.operation import operation

class wait(operation):
    def getKey(self):
        pass

    @staticmethod
    def PCOnAfterTest():# wwill the pc be on after test finishes
        return True

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc will be on before running
        return True

    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Wait operation has started, Number of seconds to wait is " + str(opParams[0]))
        time.sleep(int(opParams[0]))
        controllerPc.updateTerminalAndLog(hostPc, testLog, "\n Number of seconds to wait is " + str(opParams[0]))
        return True

