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

    def runOp(self,controllerPc,hostPc,opParams):
        controllerPc.updateRunTimeState(hostPc, ("\n number of seconds to wait is " , opParams[0]))
        time.sleep(int(opParams[0]))
        controllerPc.updateRunTimeState(hostPc, ("\n wait command has ended \n ", opParams[0]))
        return True

