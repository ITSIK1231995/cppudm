import time

from operations.operation import operation

class wait(object):
    def getKey(self):
        pass

    @staticmethod
    def runOp(hostPc,opParams):
        print (" number of seconds to wait is " , opParams.paramForOperation)
        time.sleep(int(opParams.paramForOperation))
        return True

