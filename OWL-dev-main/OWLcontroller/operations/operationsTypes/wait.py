import time

from operations.operation import operation

class wait(object):
    def getKey(self):
        pass

    @staticmethod
    def runOp(client_socket, host):
        print (" number of seconds to wait is " , host)
        time.sleep(int(host))
        return 'waiting ended'

