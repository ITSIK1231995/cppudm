import datetime
import os
import subprocess
import threading
import time
from collections import namedtuple
from UI.GUI.teststate import testState
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
        self.resultFilePath = logPath + "\\" + test.testname + "__" + self.hostPc["IP"] + "__" + timeStamp
        fileName = self.resultFilePath + "\\" + "terminal.log"
        if not os.path.exists(fileName):
            os.makedirs(self.resultFilePath)
            logObj = open(fileName, "w")
        else:
            logObj = open(fileName, "a")
        self.threadLock.release()
        return logObj

    def updateUiAndControllerWithTestStatuses(self,test,numOfPass,numOfFails):
        self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]][test.testname] = \
            {"testRepeatsCurrStatus": testState.RUNNING,
             "testRepeatsSummary": {testState.PASSED: numOfPass, testState.FAILED: numOfFails}}
        self.controllerPc.updateTestStatusInRunTime(self.hostPc, test)

    def updateUiAndControlleWithTestStatusrAfterEachRepat(self,test,numOfPass,numOfFails,repeat):
        self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]][test.testname] = \
            {"testRepeatsCurrStatus": testState.RUNNING if repeat < self.hostPc["tests"][test.testname][
                'repeatAmount'] - 1 else testState.FINISHED,
             # if we did not finished all the repeats we the state will be running otherwise it'll be according to the results
             "testRepeatsSummary": {testState.PASSED: numOfPass, testState.FAILED: numOfFails}}
        self.controllerPc.updateTestStatusInRunTime(self.hostPc, test)

    def updateUiAndContollerWithHostdata(self,hostCurrState):
        self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]]["hostPcLblColor"] = hostCurrState
        self.controllerPc.updateUiWithHostNewStatus(self.hostPc)

    def getRecordOptionFilePath(self,test):
        return os.getcwd() + "\\" + test.recordingoptions

    def getSavedTraceFullPath(self):
        return os.getcwd() + "\\" + self.resultFilePath

    def getTraceFullPathAndName(self,test):
        return self.getSavedTraceFullPath() + "\\" + test.testname + ".pex"

    def getVSEFullPathAndName(self,test):
        return os.getcwd() + "\\" + test.verificationscript

    def runAllTests(self):
        self.printToLog("starting running tests")
        stopOnFailure = self.hostPc['stopOnFailure']
        hostFinalStatus = testState.PASSED  # if True host final session status is pass , otherwise fail
        for test in self.testToRun:
            numOfPass = 0
            numOfFails = 0
            self.updateUiAndControllerWithTestStatuses(test,numOfPass,numOfFails)
            self.updateUiAndContollerWithHostdata(testState.RUNNING)
            self.printToLog("starting test= " + test.testname)
            for repeat in range(self.hostPc["tests"][test.testname]['repeatAmount']):  # repeat tests according to repeatAmount
                testLog = self.createLog(test)
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, "\n" + test.testname + " Has started ")
                analyzer = self.controllerPc.createAnalyzerInstance()
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog,"\n Analyzer recording has started for the following test: "+ test.testname)
                self.controllerPc.startRecordingWithAnalyzer(analyzer, test, self.getSavedTraceFullPath(),self.getRecordOptionFilePath(test))
                testResult = self.runSequanceOfOperations(test, self.controllerPc, testLog)
                while not self.controllerPc.isAnalyzerHandleEnded(analyzer):
                    time.sleep(1)
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog,"\n Analyzer recording has stopped for the following test: " + test.testname)
                verificationScriptOutPut = subprocess.getoutput(self.controllerPc.startVSE(self.getTraceFullPathAndName(test), self.getVSEFullPathAndName(test)))
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, verificationScriptOutPut)
                if testResult:
                    numOfPass += 1
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, "\n" + test.testname + " Has Passed")
                else:
                    numOfFails += 1
                    hostFinalStatus = testState.FAILED  # if one test has failed in the Host's session of tests its enough to mark this session for this host has a session that failed
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, "\n" + test.testname + " Has Failed")
                testLog.close()
                self.updateUiAndControlleWithTestStatusrAfterEachRepat(test,numOfPass,numOfFails,repeat)
                if self.controllerPc.haltThreads:
                    break
            if stopOnFailure and numOfFails >= 1:  # Stop on failure is on
                break
            self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, None,"\n >>> Passed: " + str(numOfPass) + "Failed:" + str(numOfFails) + "\n")
            self.printToLog("finished test= " + test.testname)
            if self.controllerPc.haltThreads:
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, None, "Testing stopped")
                self.printToLog("Halting")
                break
        self.updateUiAndContollerWithHostdata(hostFinalStatus)
        self.printToLog("Finished running tests")

    def getOprationObject(self,operation): #TODO need to put this function and the same one from validator in one place for not duplicating the code
        opraion = namedtuple('opraion', ['name', 'opraionObj'])
        mappedOperations = allOperations()
        if isinstance(operation, dict):
            return opraion(operation['name'], mappedOperations.operationsImplementation[operation['name']])
        if isinstance(operation, str):
            return opraion(operation, mappedOperations.operationsImplementation[operation])

    def runSequanceOfOperations(self, test, controllPc, testLog):
        for operation in test.flowoperations:
            if isinstance(operation, dict):
                self.printToLog("starting Operations= " + operation['name'])
                operationOutPut = self.getOprationObject(operation).opraionObj.runOp(self,self.controllerPc,self.hostPc,testLog, operation['params'])
                if operationOutPut == False:
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, (operation['name'] + " op failed"))
                    self.printToLog("finished Operations= " + operation['name'] + ", op failed")
                    return False
                self.printToLog("finished Operations= " + operation['name'] + ", op succeeded")
            elif isinstance(operation, str):
                self.printToLog("starting Operations= " + operation)
                operationOutPut = self.getOprationObject(operation).opraionObj.runOp(self, self.controllerPc,self.hostPc, testLog, [])
                if operationOutPut == False:
                    self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, (operation + " op failed"))
                    self.printToLog("finished Operations= " + operation + ", op failed")
                    return False
                self.printToLog("finished Operations= " + operation + ", op succeeded")
        return True
