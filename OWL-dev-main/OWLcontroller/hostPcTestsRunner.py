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
        self.hostPc = hostPc
        self.testToRun = self.getRelevantTestForHostPc()  #TODO  look at this
        self.threadLock = threading.Lock()
        logging.info("HostPc worker thread " + hostPc["IP"] + " started")

    def getRelevantTestForHostPc(self):  #TODO  look at this
        if self.controllerPc.currentSystemExecutionMode == systemExecutionModes.LEGACY_MODE_HOST_PC:
            allTests = self.controllerPc.configs.legacyMode.legacyFlowOperationsTestsByGroups[self.hostPc["groupName"]]
        if self.controllerPc.currentSystemExecutionMode == systemExecutionModes.LEGACY_MODE_EXCERCISER:
            allTests = self.controllerPc.configs.legacyMode.legacyTestsByGroup[self.hostPc["groupName"]]
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
        fileName = self.createLogRelativePathAndName(test) #TODO go over this
        if not os.path.exists(fileName):
            os.makedirs(self.resultFilePath)
            logObj = open(fileName, "w")
        else:
            logObj = open(fileName, "a")
        self.threadLock.release()
        return logObj

    def createLogRelativePathAndName(self, test): #TODO go over this
        timeStamp = self.getCurrentTime()
        logPath = self.controllerPc.configs.defaultConfContent["resultPath"] + "\\" + test.results[:-1]\
            if self.controllerPc.currentSystemExecutionMode == systemExecutionModes.LEGACY_MODE_HOST_PC\
            else self.controllerPc.configs.defaultConfContent["resultPath"]
        self.resultFilePath = logPath + "\\" + test.testname + "__" + self.hostPc["IP"] + "__" + timeStamp
        return self.resultFilePath + "\\" + "terminal.log"

    def updateUiAndControllerWithTestStatuses(self,test,numOfPass,numOfFails):
        self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]][test.testname] = \
            {"testRepeatsCurrStatus": testState.RUNNING,
             "testRepeatsSummary": {testState.PASSED: numOfPass, testState.FAILED: numOfFails}}
        self.controllerPc.updateTestStatusInRunTime(self.hostPc, test)

    def updateUiAndControlleWithTestStatusrAfterEachRepat(self,test,numOfPass,numOfFails,repeat):
        self.controllerPc.runtimeHostPcsData[self.hostPc["IP"]][test.testname] = \
            {"testRepeatsCurrStatus": testState.RUNNING if repeat < self.hostPc["tests"][test.testname]['repeatAmount'] - 1 else testState.FINISHED,
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
        return self.getSavedTraceFullPath() + "\\" + test.testname + "_ " + self.getCurrentTime() +".pex"

    def getVSEFullPathAndName(self,test):
        return os.getcwd() + "\\" + test.verificationscript

    def runAllTests(self):
        self.printToLog("starting running tests")
        stopOnFailure = self.hostPc['stopOnFailure']
        hostFinalStatus = testState.PASSED  # if True host final session status is pass , otherwise host final session status is fail
        for test in self.testToRun:
            numOfPass = 0
            numOfFails = 0
            self.updateUiAndControllerWithTestStatuses(test,numOfPass,numOfFails)
            self.updateUiAndContollerWithHostdata(testState.RUNNING)
            self.printToLog("starting test= " + test.testname)
            for repeat in range(self.hostPc["tests"][test.testname]['repeatAmount']):  # repeat tests according to repeatAmount
                testLog = self.createLog(test)
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog, "\n" + test.testname + " Has started ")
                analyzerHandler = self.controllerPc.createAnalyzerInstance()
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog,"\n Lecroy's Analyzer recording procedure has started")
                traceFullPathAndName = self.getTraceFullPathAndName(test)
                analyzerObj = self.controllerPc.startRecordingWithAnalyzer(analyzerHandler, traceFullPathAndName,self.getRecordOptionFilePath(test),self.hostPc, testLog)
                if self.controllerPc.currentSystemExecutionMode == systemExecutionModes.LEGACY_MODE_HOST_PC:
                    sequenceOfOperationsIsDone = self.runSequanceOfOperations(test, self.controllerPc, testLog)
                if self.controllerPc.currentSystemExecutionMode == systemExecutionModes.LEGACY_MODE_EXCERCISER:
                    sequenceOfOperationsIsDone = self.runTestOnExcerciser(analyzerObj,test,analyzerHandler)
                self.controllerPc.stopRecordingWithAnalyzer(analyzerHandler)
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog,"\n Lecroy's Analyzer recording procedure has finished")
                del analyzerHandler
                del analyzerObj
                verificationScriptResult = self.controllerPc.startVSE(traceFullPathAndName, self.getVSEFullPathAndName(test),self.hostPc, testLog)
                if sequenceOfOperationsIsDone and verificationScriptResult == 1: # verificationScriptResult == 1 is the value that Lecroy's API returns from VSE when the VSE has passed.
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
            self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, None,"\n >>> Passed: " + str(numOfPass) + " Failed:" + str(numOfFails) + "\n")
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

    def runTestOnExcerciser(self,analyzerObj,test,analyzerHandler):
        # analyzerObjNew = win32com.client.Dispatch("CATC.PETracer")
        print ("\nload generation option")
        analyzerObj.GetGenerationOptions().Load(os.getcwd() + "\\" +  test.generationoptions)
        print("\nend generation option")
        print("\nStart trainer init ")
        result = analyzerObj.StartGeneration(os.getcwd() + "\\" + test.trainerinitscript, 0, 0)
        while analyzerHandler.getGenerationState() != 1:
            time.sleep(0.2)
            pythoncom.PumpWaitingMessages()
            print("PumpWaitingMessages")
        analyzerHandler.generationStateToZero()
        print(" Start  generation script begin")
        analyzerObj.StartGeneration(os.getcwd() + "\\" + test.trainerscript, 0, 0)
        return True

    def runSequanceOfOperations(self, test, controllPc, testLog):  # TODO need to remove ControlPC and  #TODO  look at this
        for operation in test.flowoperations:
            self.printToLog("starting Operations= " + operation['name'])
            operationOutPut = self.getOprationObject(operation).opraionObj.runOp(self, self.controllerPc,self.hostPc, testLog,operation['params'] if isinstance(operation,dict) else [])
            if not operationOutPut:
                self.controllerPc.updateRunTimeStateInTerminal(self.hostPc, testLog,
                                                                   (operation['name'] + " Op failed"))
                self.printToLog("finished Operations= " + operation['name'] + ", Op failed")
                return False
            self.printToLog("finished Operations= " + operation['name'] + ", Op succeeded")
        return True
