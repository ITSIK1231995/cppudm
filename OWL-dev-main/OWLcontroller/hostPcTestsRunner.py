import socket
from collections import namedtuple

from operations.allOperations import allOperations
import logging


class hostPcTestsRunner():

    def __init__(self, controllerPc, hostPc):
        self.controllerPc = controllerPc
        self.hostPc = hostPc
        self.testToRun = self.getRelevantTestForHostPc()
        logging.info("hostPc worker thread "+hostPc["IP"]+" started")


    def getRelevantTestForHostPc(self):
        allTests = self.controllerPc.configs.legacyMode.legacyFlowOperationsTestsByGroups[self.hostPc["groupName"]]
        relevantTests = []
        for test in allTests:
            if test.testname in self.hostPc["tests"].keys() and \
                    self.hostPc["tests"][test.testname]['checked']:
                relevantTests.append(test)
        return relevantTests

    def printToLog(self,text):
        logging.info(("worker thread",self.hostPc["IP"],text))


    def runAllTests(self):
        self.printToLog("starting running tests")
        stopOnFailure = self.hostPc['stopOnFailure']
        for test in self.testToRun:
            self.controllerPc.updateTestStatusInRunTime(self.hostPc,test,"Running")
            self.printToLog("starting test= " + test.testname)
            numOfPass = 0
            numOfFails = 0
            for x in range(self.hostPc["tests"][test.testname]['repeatAmount']):  # repeat tests acurding to repeatAmount
                self.controllerPc.updateRunTimeState(self.hostPc, "\n" + test.testname + " Has started !!! \n")
                testResult = self.runSequanceOfOperations(test, self.controllerPc)
                if (testResult):
                    numOfPass += 1
                    self.controllerPc.updateRunTimeState(self.hostPc, "\n" + test.testname + " Has Passed !!! \n")
                else:
                    numOfFails += 1
                    self.controllerPc.updateRunTimeState(self.hostPc, "\n" + test.testname + " Has Failed !!! \n")
                self.controllerPc.updateTestStatusInRunTime(self.hostPc, test, " Passed: " + str(numOfPass) + " Failed: " + str(numOfFails))

                if self.controllerPc.haltThreads:
                    break

            if stopOnFailure and numOfFails >= 1:  # Stop on failure is on
                break

            self.controllerPc.updateRunTimeState(self.hostPc, "\n >>> Passed: " + str(numOfPass) + " Failed:" + str(
                numOfFails) + "\n")
            self.printToLog("finished test= " + test.testname)

            if self.controllerPc.haltThreads:
                self.controllerPc.updateRunTimeState(self.hostPc, "testing stopped")
                self.printToLog("halting")
                break

        self.printToLog("finished running tests")



    def createCommunication(self, hostIp, hostPort):  # TODO : move  to oprationWithSocet
        CommunicationInfo = namedtuple('CommunicationInfo', ['socket', 'hostIP'])
        port = hostPort  # socket server port number
        clientSocket = socket.socket()  # instantiate
        try:
            clientSocket.connect((hostIp, port))  # connect to the server
        except socket.error as e:
            print(e)
            return False
        CommunicationInfo.socket = clientSocket
        CommunicationInfo.hostIP = hostIp
        return CommunicationInfo

    def closeCommunication(self, client_socket):  # TODO : move  to oprationWithSocet
        client_socket.close()  # close the connection

    def runSequanceOfOperations(self, test, controllPc):
        mappedOperations = allOperations()
        for operation in test.flowoperations:
            if isinstance(operation, dict):
                self.printToLog("starting Operations= " + operation['name'])
                operationOutPut = mappedOperations.operationsImplementation[operation['name']].runOp(self,
                                                                                                     self.controllerPc,
                                                                                                     self.hostPc,
                                                                                                     operation[
                                                                                                         'params'])
                if operationOutPut == False:
                    self.controllerPc.updateRunTimeState(self.hostPc,(operation['name'] + " op failed"))  # todo : update GUI
                    self.printToLog("finished Operations= " + operation['name'] + ", op failed")
                    return False

                self.printToLog("finished Operations= " + operation['name']+ ", op succeeded")

            elif isinstance(operation, str):
                self.printToLog("starting Operations= " + operation)
                operationOutPut = mappedOperations.operationsImplementation[operation].runOp(self, self.controllerPc,
                                                                                             self.hostPc, [])
                if operationOutPut == False:
                    self.controllerPc.updateRunTimeState(self.hostPc, (operation + " op failed"))  # todo : update GUI
                    print(operation + " op failed")
                    self.printToLog("finished Operations= " + operation + ", op failed")
                    return False
                self.printToLog("finished Operations= " + operation + ", op succeeded")


        return True
