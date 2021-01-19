import socket
from collections import namedtuple

from operations.allOperations import allOperations


class hostPcTestEnvClient():

    def createCommunication(self):
        CommunicationInfo = namedtuple('CommunicationInfo' , ['socket', 'hostIP'])
        host = socket.gethostname()  # as both code is running on same pc
        port = 5000  # socket server port number
        clientSocket = socket.socket()  # instantiate
        clientSocket.connect((host, port))  # connect to the server
        CommunicationInfo.socket =clientSocket
        CommunicationInfo.hostIP = host
        return CommunicationInfo

    def closeCommunication(self, client_socket):
        client_socket.close()  # close the connection

    # def runSequanceOfOperations(self, operations):
    #     ' This method gets a list from the ControlPC which conatins  operations names, if the operation needs sspecific params, it will be saved in the list as a dict (key = operation name, value = operation parameters) '
    #
    #     client_socket = self.createCommunication()
    #     message = input(" -> ")  # The messege to the server
    #
    #     while message.lower().strip() != 'bye':
    #         client_socket.send(message.encode())  # send message
    #         data = client_socket.recv(1024).decode()  # receive response from the server
    #
    #         print('Received from server: ' + data)  # show the response in terminal
    #
    #         message = input(" -> ")  # again send a messege to the server
    #
    #     self.closeCommunication(client_socket)


    def runSequanceOfOperations(self, operations):
        ' This method gets a list from the ControlPC which conatins  operations names, if the operation needs sspecific params, it will be saved in the list as a dict (key = operation name, value = operation parameters) '

        # clientSocket = self.createCommunication()

        for operation in operations:
            CommunicationInfo = self.createCommunication()
            clientSocket = CommunicationInfo.socket
            message = operation  # The messege to the server

            if isinstance(operation, dict):
                mappedOperations = allOperations()
                operationOutPut = mappedOperations.operationsImplement[operation['operation']].runOp(clientSocket, operation['param'])
                print (operationOutPut)

            elif isinstance(operation, str):
                mappedOperations = allOperations()
                operationOutPut = mappedOperations.operationsImplement[operation].runOp(clientSocket, CommunicationInfo.hostIP)
                print(operationOutPut)

            self.closeCommunication(clientSocket)


if __name__ == '__main__':
    # example for Control Pc request to run a sequance of commands
    exampleListOfOperationsFromConfigfile = [{'operation': 'runCommandViaCmd', 'param': "ipconfig"}
                                             , 'shutdown', 'sleep', 'hibernate',
                                             {'operation': 'wait', 'param': "5"}]

    hostPcTestEnvClient().runSequanceOfOperations(exampleListOfOperationsFromConfigfile)


