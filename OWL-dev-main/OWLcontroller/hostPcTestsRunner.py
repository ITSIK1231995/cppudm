import datetime
import os
import threading
from UI.GUI.state import state
from operations.allOperations import allOperations
import logging


class hostPcTestsRunner():

    def __init__(self, controllerPc, hostPc):
        self.controllerPc = controllerPc
        self.hostPc = hostPc
        self.testToRun = self.getRelevantTestForHostPc()
        self.threadLock = threading.Lock()
        logging.info("HostPc worker thread " + hostPc["IP"] + " started")

    def getRelevantTestForHostPc(self):
        allTests = self.controllerPc.configs.legacyMode.legacyFlowOperationsTestsByGroups[self.hostPc["groupName"]]
        relevantTests = []
        for test in allTests:
            if test.testname in self.hostPc["tests"].keys() and \
                    self.hostPc["tests"][test.testname]['checked']:
                relevantTests.append(test)
        return relevantTests

    def printToLog(self, text):
        logging.info(("worker thread", self.hostPc["IP"], text))

    def getCurrentTime(self):
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S").replace("-", "_").replace(":", "_"))

    def createLog(self, test):
        self.threadLock.acquire()
        timeStamp = self.getCurrentTime()
        logPath = self.controllerPc.configs.defaultConfContent["resultPath"] + "\\" + test.results[:-1]
        filePath = logPath + "\\" + test.testname + "__" + self.hostPc["IP"] + "__" + timeStamp
        fileName = filePath + "\\" + "terminal.log"
        if not os.path.exists(fileName):
            os.makedirs(filePath)
            logObj = open(fileName, "w")
        else:
            logObj = open(fileName, "a")
        self.threadLock.release()
        return logObj

    def runAllTests(self):
        self.printToLog("starting running tests")
        stopOnFailure = self.hostPc['stopOnFailure']
        hostFinalStatus = state.PASSED  # if True host final session status is pass , otherwise fail
        for test in self.testToRun:
            numOfPass = 0
            numOfFails = 0

            self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]][test.testname] = \
                {"testRepeatsCurrStatus": state.RUNNING,
                 "testRepeatsSummary": {state.PASSED: numOfPass, state.FAILED: numOfFails}}
            self.controllerPc.updateTestStatusInRunTime(self.hostPc, test)

            self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]]["hostPcLblColor"] = state.RUNNING
            self.controllerPc.updateUiWithHostNewStatus(self.hostPc)
            self.printToLog("starting test= " + test.testname)
            for x in range(self.hostPc["tests"][test.testname]['repeatAmount']):  # repeat tests according to repeatAmount
                testLog = self.createLog(test)
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, "\n" + test.testname + " Has started ")

#TODO need to start and stop recording with analyzer
                analyzerInfo = self.controllerPc.analyzer.startAnalyzerRecord(os.getcwd() + "\\" +test.recordingoptions,r"C:\cppudm\OWL-dev-main\OWLcontroller", "newTrace")

                testResult = self.runSequanceOfOperations(test, self.controllerPc, testLog)

                self.controllerPc.analyzer.stopAnalyzerRecording(analyzerInfo)

                if (testResult):
                    numOfPass += 1
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, "\n" + test.testname + " Has Passed")
                else:
                    numOfFails += 1
                    hostFinalStatus = state.FAILED  # if one test has failed in the Host's session of tests its enough to mark this session for this host has a session that failed
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, "\n" + test.testname + " Has Failed")
                testLog.close()

                self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]][test.testname] = \
                    {"testRepeatsCurrStatus": state.RUNNING if x < self.hostPc["tests"][test.testname]['repeatAmount']-1 else state.FINISHED, # if we did not finished all the repeats we the state will be running otherwise it'll be according to the results
                     "testRepeatsSummary": {state.PASSED: numOfPass, state.FAILED: numOfFails}}
                self.controllerPc.updateTestStatusInRunTime(self.hostPc, test)

                if self.controllerPc.haltThreads:
                    break

            if stopOnFailure and numOfFails >= 1:  # Stop on failure is on
                break

            self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, None,
                                                 "\n >>> Passed: " + str(numOfPass) + " Failed:" + str(
                                                     numOfFails) + "\n")
            self.printToLog("finished test= " + test.testname)

            if self.controllerPc.haltThreads:
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, None, "Testing stopped")
                self.printToLog("halting")
                break
        self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]]["hostPcLblColor"] = hostFinalStatus
        self.controllerPc.updateUiWithHostNewStatus(self.hostPc)
        self.printToLog("Finished running tests")

    # TODO: change implementation to somthing like in the validator : validateflowOps ( use getOprationObject )
    def runSequanceOfOperations(self, test, controllPc, testLog):
        mappedOperations = allOperations()
        for operation in test.flowoperations:
            if isinstance(operation, dict):
                self.printToLog("starting Operations= " + operation['name'])
                operationOutPut = mappedOperations.operationsImplementation[operation['name']].runOp(self,
                                                                                                     self.controllerPc,
                                                                                                     self.hostPc,
                                                                                                     testLog, operation[
                                                                                                         'params'])
                if operationOutPut == False:
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, (operation['name'] + " op failed"))
                    self.printToLog("finished Operations= " + operation['name'] + ", op failed")
                    return False

                self.printToLog("finished Operations= " + operation['name'] + ", op succeeded")

            elif isinstance(operation, str):
                self.printToLog("starting Operations= " + operation)
                operationOutPut = mappedOperations.operationsImplementation[operation].runOp(self, self.controllerPc,
                                                                                             self.hostPc, testLog, [])
                if operationOutPut == False:
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, (operation + " op failed"))
                    self.printToLog("finished Operations= " + operation + ", op failed")
                    return False
                self.printToLog("finished Operations= " + operation + ", op succeeded")
        return True
