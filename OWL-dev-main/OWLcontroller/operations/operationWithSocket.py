import socket
from operations.operation import operation

class operationWithSocket(operation):

    def getKey(self):
        pass


    def runOp(self,controllerPc,hostPc,opParams):
        pass

    def createCommunication(self, hostIp, hostPort): #TODO : move  to oprationWithSocet - Done
        port = hostPort  # socket server port number
        clientSocket = socket.socket()  # instantiate
        try:
            clientSocket.connect((hostIp, port))  # connect to the server
        except socket.error as e:
            print(e)
            return False
        return clientSocket

