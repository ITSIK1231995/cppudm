import time

from operations.operation import operation

class wait(operation):
    def getKey(self):
        pass

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return True

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return True

    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateRunTimeState(hostPc,testLog, "\n number of seconds to wait is " + str(opParams))
        time.sleep(int(opParams))
        controllerPc.updateRunTimeState(hostPc,testLog, "\n number of seconds to wait is " + str(opParams))
        return True

