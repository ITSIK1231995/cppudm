import socket
from operations.operation import operation

class operationWithSocket(operation):

    def getKey(self):
        pass


    def runOp(self,controllerPc,hostPc,opParams):
        pass

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        pass

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        pass
    
    def createCommunication(self,controllerPc,hostPc): #
        controllerPc.updateRunTimeState(hostPc, "\n create Communication (Socket) \n")
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']  # socket server port number
        clientSocket = socket.socket()  # instantiate
        try:
            clientSocket.connect((hostPc["IP"], port))  # connect to the server
        except socket.error as e:
            #controllerPc.updateRunTimeState(hostPc, "\n " + str(e) + "\n ")
            return False
        return clientSocket

