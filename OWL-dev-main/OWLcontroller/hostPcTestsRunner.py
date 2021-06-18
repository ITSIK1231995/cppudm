import datetime
import os
import threading
import time
from collections import namedtuple
import pythoncom
import win32com.client

from UI.GUI.systemModes import systemExecutionModes
from UI.GUI.teststate import testState
from operations.allOperations import allOperations
import logging
#TODO when adding the execciser mode - need to add here an if statement to check which mode i am now, and than to send to the threadMain instead of hostPc , need to send generic host and instead of "IP" to te host need to send identifier the identifier will include IP when its host pc mdoe and maybe ID or serial number when it is excerciser mode , after that in the "hostPcTestRunner" i will get in the _init__ function the host and the indetifeir and will use it in the hostPcTestRunner, in addition in the hostPcTestRunner i will add a function that calls the controller and ask him to activate the xcerciser instead of activationg the sequcne of operation that way the class of HostPcTestRunner will support both execiser and host pc
class hostPcTestsRunner():
    def __init__(self, controllerPc, hostPc):
        self.controllerPc = controllerPc
        self.host = hostPc
        self.testToRun = self.getRelevantTestForHostPc()  #TODO  look at this
        self.threadLock = threading.Lock()
        logging.info("HostPc worker thread " + hostPc["IP"] + " started")

    def getRelevantTestForHostPc(self):  #TODO  look at this
        if self.controllerPc.isCurrentExecutionModeIsHostPcMode():
            allTests = self.controllerPc.configs.legacyMode.legacyFlowOperationsTestsByGroups[self.host["groupName"]]
        else:
            allTests = self.controllerPc.configs.legacyMode.legacyTestsByGroup[self.host["groupName"]]
        relevantTests = []
        for test in allTests:
            if test.testname in self.host["tests"].keys() and \
                    self.host["tests"][test.testname]['checked']:
                relevantTests.append(test)
        return relevantTests

    def printToLog(self, text):
        logging.info(("worker thread", self.host["IP"], text))

    def getCurrentTime(self):
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S").replace("-", "_").replace(":", "_"))

    def createLog(self, test):
        self.threadLock.acquire()
        fileName = self.createLogRelativePathAndName(test)
        if not os.path.exists(fileName):
            os.makedirs(self.resultFilePath)
            logObj = open(fileName, "w")
        else:
            logObj = open(fileName, "a")
        self.threadLock.release()
        return logObj

    def createLogRelativePathAndName(self, test):
        timeStamp = self.getCurrentTime()
        logPath = self.controllerPc.configs.defaultConfContent["resultPath"] + "\\" + test.results[:-1]\
            if self.controllerPc.isCurrentExecutionModeIsHostPcMode()\
            else self.controllerPc.configs.defaultConfContent["resultPath"]
        self.resultFilePath = logPath + "\\" + self.replaceSpecialCharactersWithSpaces(test.testname) + "__" + self.host["IP"] + "__" + timeStamp
        return self.resultFilePath + "\\" + "terminal.log"

    def replaceSpecialCharactersWithSpaces(self, testName):
        return testName.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})


    def updateUiAndControllerWithTestStatuses(self,test,numOfPass,numOfFails):
        self.controllerPc.runtimeHostPcsData[self.host["IP"]][test.testname] = \
            {"testRepeatsCurrStatus": testState.RUNNING,
             "testRepeatsSummary": {testState.PASSED: numOfPass, testState.FAILED: numOfFails}}
        self.controllerPc.updateTestStatusInRunTime(self.host, test)

    def updateUiAndControlleWithTestStatusrAfterEachRepat(self,test,numOfPass,numOfFails,repeat):
        self.controllerPc.runtimeHostPcsData[self.host["IP"]][test.testname] = \
            {"testRepeatsCurrStatus": testState.RUNNING if repeat < self.host["tests"][test.testname]['repeatAmount'] - 1 else testState.FINISHED,
             # if we did not finished all the repeats we the state will be running otherwise it'll be according to the results
             "testRepeatsSummary": {testState.PASSED: numOfPass, testState.FAILED: numOfFails}}
        self.controllerPc.updateTestStatusInRunTime(self.host, test)

    def updateUiAndContollerWithHostdata(self,hostCurrState):
        self.controllerPc.runtimeHostPcsData[self.host["IP"]]["hostPcLblColor"] = hostCurrState
        self.controllerPc.updateUiWithHostNewStatus(self.host)

    def getRecordOptionFilePath(self,test):
        return os.getcwd() + "\\" + test.recordingoptions

    def getTrainerInitScriptFullPathAndNameForExerciser(self,test):
        return os.getcwd() + "\\" + test.trainerinitscript

    def getTrainerScriptForExerciser(self,test):
        return os.getcwd() + "\\" + test.trainerscript

    def getSavedTraceFullPath(self):
        return os.getcwd() + "\\" + self.resultFilePath

    def getTraceFullPathAndName(self,test):
        return self.getSavedTraceFullPath() + "\\" + self.replaceSpecialCharactersWithSpaces(test.testname) + "_ " + self.getCurrentTime() +".pex"

    def getVSEFullPathAndName(self,test):
        return os.getcwd() + "\\" + test.verificationscript

    def runAllTests(self): #TODO go over this refactor
        self.printToLog("starting running tests")
        stopOnFailure = self.host['stopOnFailure']
        hostFinalStatus = testState.PASSED  # if True host final session status is pass , otherwise host final session status is fail
        for test in self.testToRun:
            numOfPass = 0
            numOfFails = 0
            self.updateUiAndControllerWithTestStatuses(test,numOfPass,numOfFails)
            self.updateUiAndContollerWithHostdata(testState.RUNNING)
            self.printToLog("starting test= " + test.testname)
            for repeat in range(self.host["tests"][test.testname]['repeatAmount']):  # repeat tests according to repeatAmount
                testLog = self.createLog(test)
                self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n" + test.testname + " Has started ")
                lecroyHandler = self.controllerPc.createLecroyHandlerInstance()
                self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n Lecroy's Analyzer recording procedure has started")
                traceFullPathAndName = self.getTraceFullPathAndName(test)
                lecroyObj = self.controllerPc.startRecordingWithAnalyzer(lecroyHandler, traceFullPathAndName, self.getRecordOptionFilePath(test), self.host, testLog)
                if self.controllerPc.currentSystemExecutionMode == systemExecutionModes.LEGACY_MODE_HOST_PC:
                    isTestEnded = self.runSequanceOfOperations(test, testLog)
                if self.controllerPc.currentSystemExecutionMode == systemExecutionModes.LEGACY_MODE_EXCERCISER:
                    isTestEnded = self.runTestOnExcerciser(lecroyObj,test,lecroyHandler,testLog)
                self.controllerPc.stopRecordingWithAnalyzer(lecroyHandler)
                self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n Lecroy's Analyzer recording procedure has finished")
                del lecroyHandler
                del lecroyObj
                verificationScriptResult = self.controllerPc.startVSE(traceFullPathAndName, self.getVSEFullPathAndName(test), self.host, testLog)
                if isTestEnded and verificationScriptResult == 1: # verificationScriptResult == 1 is the value that Lecroy's API returns from VSE when the VSE has passed.
                    numOfPass += 1
                    self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n" + test.testname + " Has Passed")
                else:
                    numOfFails += 1
                    hostFinalStatus = testState.FAILED  # if one test has failed in the Host's session of tests its enough to mark this session for this host has a session that failed
                    self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n" + test.testname + " Has Failed")
                testLog.close()
                self.updateUiAndControlleWithTestStatusrAfterEachRepat(test,numOfPass,numOfFails,repeat)
                if self.controllerPc.haltThreads:
                    break
            if stopOnFailure and numOfFails >= 1:  # Stop on failure is on
                break
            self.controllerPc.updateTerminalAndLog(self.host, None, "\n >>> Passed: " + str(numOfPass) + " Failed:" + str(numOfFails) + "\n")
            self.printToLog("finished test= " + test.testname)
            if self.controllerPc.haltThreads:
                self.controllerPc.updateTerminalAndLog(self.host, None, "Testing stopped")
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

    def runTestOnExcerciser(self, lecroyObj, test, lecroyHandler,testLog): #TODO need to move all the content here to lecroy class
        self.controllerPc.updateTerminalAndLog(self.host, testLog, "Loading Generation Options")
        self.controllerPc.loadGenerationOptionsToExerciser(lecroyObj,os.getcwd() + "\\" + test.generationoptions,lecroyHandler)
        self.controllerPc.updateTerminalAndLog(self.host, testLog, test.generationoptions + " has been loaded")
        self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Init Script Started")
        result = self.controllerPc.startGenerationScriptWithExerciser(lecroyHandler,lecroyObj,self.getTrainerInitScriptFullPathAndNameForExerciser(test))
        if self.controllerPc.verifyGenerationScriptOnExerciserFinished(lecroyHandler):
            self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Init Script Finished")
            self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Script Started")
            self.controllerPc.startGenerationScriptWithExerciser(lecroyHandler, lecroyObj, self.getTrainerScriptForExerciser(test))
            if self.controllerPc.verifyGenerationScriptOnExerciserFinished(lecroyHandler):
                self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Script Finished")
                return True

    def runSequanceOfOperations(self, test, testLog):
        for operation in test.flowoperations:
            self.printToLog("starting Operations= " + operation['name'])
            operationOutPut = self.getOprationObject(operation).opraionObj.runOp(self, self.controllerPc, self.host, testLog, operation['params'] if isinstance(operation, dict) else [])
            if not operationOutPut:
                self.controllerPc.updateTerminalAndLog(self.host, testLog, (operation['name'] + " Op failed"))
                self.printToLog("finished Operations= " + operation['name'] + ", Op failed")
                return False
            self.printToLog("finished Operations= " + operation['name'] + ", Op succeeded")
        return True
