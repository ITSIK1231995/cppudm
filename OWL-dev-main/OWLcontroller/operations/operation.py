import socket


class operation(object):

    def getKey(self):
        pass

    @staticmethod
    def runOp(controllerPc,hostPc,opParams):
        pass


    def checkIfPcisOn(self,controllerPc,hostPc):
        clientSocket = socket.socket()  # instantiate
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        i = 0
        while True:
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
            except socket.error as e:
                if i < attempsToConnectSocket:
                    i += 1
                    continue
                else:
                    return False
            break
        clientSocket.close()
        return True

        # try:
        #     clientSocket.connect((hostPc["IP"], port))  # connect to the server
        # except socket.error as e:
        #     return False
        # clientSocket.close()
        # return True



#todo : make a calss (in a diffrent folder) opration with socket that inherents from opration and includes all functions that manage sockets
#todo : make all oprations use hostPC as the data provider
#todo : use sockets in order to test if computer is on
#todo : make all oprations inherent from opration or oprationWithSucket