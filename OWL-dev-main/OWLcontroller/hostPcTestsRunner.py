import socket
from collections import namedtuple

from operations.allOperations import allOperations

class hostPcTestsRunner():


    def __init__(self, controllerPc,hostPc):
        self.controllerPc = controllerPc
        self.hostPc = hostPc
        self.testToRun = self.getRelevantTestForHostPc()

    def getRelevantTestForHostPc(self):
        allTests = self.controllerPc.configs.legacyMode.legacyFlowOperationsTestsByGroups[self.hostPc["groupName"]]
        relevantTests=[]
        for test in allTests:
            if  test.testname in self.hostPc["tests"].keys() and \
                    self.hostPc["tests"][test.testname]['checked']:
                relevantTests.append(test)
        return relevantTests

    def runAllTests(self):
        for test in self.testToRun:
            for x in range(self.hostPc["tests"][test.testname]['repeatAmount']): #repeat tests acurding to repeatAmount
                self.runSequanceOfOperations(test)

            # todo : add stop on failure here



    def createCommunication(self, hostIp, hostPort): #TODO : move  to oprationWithSocet
        CommunicationInfo = namedtuple('CommunicationInfo' , ['socket', 'hostIP'])
        port = hostPort  # socket server port number
        clientSocket = socket.socket()  # instantiate
        try:
            clientSocket.connect((hostIp, port))  # connect to the server
        except socket.error as e:
            print(e)
            return False
        CommunicationInfo.socket =clientSocket
        CommunicationInfo.hostIP = hostIp
        return CommunicationInfo


    def closeCommunication(self, client_socket): #TODO : move  to oprationWithSocet
        client_socket.close()  # close the connection



    def runSequanceOfOperations(self, test):
        mappedOperations = allOperations()
        for operation in test.flowoperations:
            if isinstance(operation, dict):
                operationOutPut = mappedOperations.operationsImplementation[operation['name']].runOp(self.hostPc,operation['params'])
                if operationOutPut == False:
                    print("op failed") #todo : update GUI
            elif isinstance(operation, str):
                operationOutPut = mappedOperations.operationsImplementation[operation].runOp(self.hostPc,[])
                if operationOutPut == False:
                    print("op failed") #todo : update GUI



