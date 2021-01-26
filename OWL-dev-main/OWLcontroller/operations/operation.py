import socket


class operation(object):

    def getKey(self):
        pass

    @staticmethod
    def runOp(controllerPc,hostPc,opParams):
        pass


    #todo: if expacting pc to turnOff - test conection untill pc is off or threashhold exceded then return true
    #todo: if expacting pc to turnOn - test conection untill pc is ON or threashhold exceded then return true
    def waitForPcToTurnOn(self,controllerPc,hostPc): # when PC is ON output is True
        clientSocket = socket.socket()
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        for i in range(attempsToConnectSocket):
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
                clientSocket.send("Test".encode())
                clientSocket.close()
                print("waitForPcToTurnOn - PC is ON")
                return True
            except socket.error as e:
                print("waitForPcToTurnOn - PC is OFF atempt "+ str(i))
                pass
        return False

    def waitForPcToTurnOff(self,controllerPc,hostPc): # when PC is off output is True
        clientSocket = socket.socket()
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        for i in range(attempsToConnectSocket):
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
                clientSocket.send("Test".encode())
                clientSocket.close()
                print("waitForPcToTurnOff - PC is ON atempt "+ str(i))
            except socket.error as e:
                print("waitForPcToTurnOff - PC is OFF")
                return True
        return False


    def checkIfPcisOn(self,controllerPc,hostPc):
        clientSocket = socket.socket()  # instantiate
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        i = 0
        while True:
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
                clientSocket.send("Test".encode())
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