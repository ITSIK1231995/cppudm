import time

from operations.operation import operation

class wait(operation):
    def getKey(self):
        pass


    def runOp(self,controllerPc,hostPc,opParams):
        print (" number of seconds to wait is " , opParams[0])
        time.sleep(int(opParams[0]))
        return True

