import socket
from operations.operation import operation

class operationWithSocket(operation):

    def getKey(self):
        pass


    def runOp(self,controllerPc,hostPc,testLog,opParams):
        pass

    def createCommunication(self,controllerPc,hostPc, testLog): #
        controllerPc.updateRunTimeState(hostPc,testLog, "\n create Communication")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']  # socket server port number
        clientSocket = socket.socket()  # instantiate
        try:
            clientSocket.connect((hostPc["IP"], port))  # connect to the server
        except socket.error as e:
            #controllerPc.updateRunTimeState(hostPc, "\n " + str(e) + "\n ")
            return False
        return clientSocket

