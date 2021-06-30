import datetime
import os
import threading
from Utils import getOperationObject, getTestsByGroupDictForCurrentSystemExecutionMode
from UI.GUI.teststate import testState
import logging

#TODO when adding the execciser mode - need to add here an if statement to check which mode i am now, and than to send to the threadMain instead of hostPc , need to send generic host and instead of "IP" to te host need to send identifier the identifier will include IP when its host pc mdoe and maybe ID or serial number when it is excerciser mode , after that in the "hostPcTestRunner" i will get in the _init__ function the host and the indetifeir and will use it in the hostPcTestRunner, in addition in the hostPcTestRunner i will add a function that calls the controller and ask him to activate the xcerciser instead of activationg the sequcne of operation that way the class of HostPcTestRunner will support both execiser and host pc
class hostTestsRunner():
    def __init__(self, controllerPc, host):
        self.controllerPc = controllerPc
        self.host = host
        self.testToRun = self.getRelevantTestForHost()
        self.threadLock = threading.Lock()
        logging.info("Host worker thread " + host["IP"] + " started")

    def getRelevantTestForHost(self):
        allTests = getTestsByGroupDictForCurrentSystemExecutionMode(self.controllerPc)[self.host["groupName"]]
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

    def updateUiAndControllerWithTestStatus(self, test, numOfPass, numOfFails,repeatAmount):
        self.controllerPc.runtimeHostPcsData[self.host["IP"]][test.testname] = \
            {"testRepeatsCurrStatus": testState.RUNNING if repeatAmount > 0 else testState.TESTREPEATISZERO,
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

    def updateUiSummerizeBox(self,numOfPassTests,numOffailedTests,numOfTestToRun):
        self.controllerPc.updateUiSummerizeBox(numOfPassTests,numOffailedTests,numOfTestToRun)

    def getRecordOptionFilePath(self,test):
        return os.getcwd() + "\\" + test.recordingoptions

    def getTrainerInitScriptFullPathForExerciserFromTestConf(self, test):
        return os.getcwd() + "\\" + test.trainerinitscript

    def getTrainerScriptPathForExerciserFromTestConf(self, test):
        return os.getcwd() + "\\" + test.trainerscript

    def getSavedTraceFullPath(self):
        return os.getcwd() + "\\" + self.resultFilePath

    def getTraceFullPathAndName(self,test):
        return self.getSavedTraceFullPath() + "\\" + self.replaceSpecialCharactersWithSpaces(test.testname) + "_ " + self.getCurrentTime() +".pex"

    def getVSEFullPathAndName(self,test):
        return os.getcwd() + "\\" + test.verificationscript

    def getTotalNumOfTestsToRun(self): #TODO look at this
        TotalNumberOfTests = 0
        for test in self.testToRun:
            TotalNumberOfTests += self.host["tests"][test.testname]['repeatAmount']
        return TotalNumberOfTests

    def runAllTests(self): #TODO go over this refactor
        self.printToLog("starting running tests")
        stopOnFailure = self.host['stopOnFailure']
        totalTests = self.getTotalNumOfTestsToRun() #TODO look at this
        totalPassedTests = 0
        totalFailedTests = 0
        hostFinalStatus = testState.PASSED  # if True host final session status is pass , otherwise host final session status is fail
        for test in self.testToRun:
            numOfPass = 0
            numOfFails = 0
            repeatAmount = self.host["tests"][test.testname]['repeatAmount']
            self.updateUiAndControllerWithTestStatus(test, numOfPass, numOfFails,repeatAmount) #TODO LOOK at this repat amount addition
            self.updateUiAndContollerWithHostdata(testState.RUNNING)
            self.printToLog("starting test= " + test.testname)
            for repeat in range(repeatAmount):  # repeat tests according to repeatAmount
                self.updateUiSummerizeBox(totalPassedTests, totalFailedTests, totalTests)
                testLog = self.createLog(test)
                self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n" + test.testname + " Has started ")
                lecroyHandler = self.controllerPc.createLecroyHandlerInstance()
                self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n Lecroy's Analyzer recording procedure has started")
                traceFullPathAndName = self.getTraceFullPathAndName(test)
                lecroyObj = self.controllerPc.startRecordingWithAnalyzer(lecroyHandler, traceFullPathAndName, self.getRecordOptionFilePath(test), self.host, testLog)
                if lecroyObj is not None: #TODO Look at tihs
                    if self.controllerPc.isCurrentExecutionModeIsHostPcMode():
                        isTestExecuted = self.runSequanceOfOperations(test, testLog)
                    else:
                        isTestExecuted = self.runTestOnExcerciser(lecroyObj,test,lecroyHandler,testLog)
                    self.controllerPc.stopRecordingWithAnalyzer(lecroyHandler)
                    self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n Lecroy's Analyzer recording procedure has finished")
                    del lecroyHandler
                    del lecroyObj
                    verificationScriptResult = self.controllerPc.startVSE(traceFullPathAndName, self.getVSEFullPathAndName(test), self.host, testLog)
                else:#TODO Look at tihs
                    isTestExecuted = False#TODO Look at tihs
                    verificationScriptResult = None#TODO Look at tihs
                    self.controllerPc.updateTerminalAndLog(self.host, testLog, #TODO Look at tihs
                                                           "\n Test execution canceled since start recording has failed")
                if isTestExecuted and verificationScriptResult == 1: # verificationScriptResult == 1 is the value that Lecroy's API returns from VSE when the VSE has passed.
                    numOfPass += 1 #TODO look at this
                    totalPassedTests += 1 #TODO look at this if i add numOfPass in each iterate it will be multiple number of pass
                    self.updateUiSummerizeBox(totalPassedTests, totalFailedTests, totalTests) #TODO look at this if i add numOfPass in each iterate it will be multiple number of pass
                    self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n" + test.testname + " Has Passed")
                else: #TODO look at this
                    numOfFails += 1
                    totalFailedTests += 1  #TODO look at this if i add numOfPass in each iterate it will be multiple number of pass
                    self.updateUiSummerizeBox(totalPassedTests, totalFailedTests, totalTests)  #TODO look at this if i add numOfPass in each iterate it will be multiple number of pass
                    hostFinalStatus = testState.FAILED  # if one test has failed in the Host's session of tests its enough to mark this session for this host has a session that failed
                    self.controllerPc.updateTerminalAndLog(self.host, testLog, "\n" + test.testname + " Has Failed")
                testLog.close()
                self.updateUiAndControlleWithTestStatusrAfterEachRepat(test,numOfPass,numOfFails,repeat)
                if self.controllerPc.haltThreads:
                    break
            if stopOnFailure and numOfFails >= 1:  # Stop on failure is on
                break
            self.controllerPc.updateTerminalAndLog(self.host, None, "\n >>> Passed: " + str(numOfPass) + " Failed:" + str(numOfFails) + "\n")
            self.printToLog("Finished test= " + test.testname)
            if self.controllerPc.haltThreads:
                self.controllerPc.updateTerminalAndLog(self.host, None, "Testing Stopped")
                self.printToLog("Halting")
                break
        self.updateUiAndContollerWithHostdata(hostFinalStatus)
        del self.controllerPc.runtimeHostPcsData[self.host["IP"]] #TODO this deletion need to be moved from here to other place because if its here , when the test endes the data deletes from the runtimHostPcDAta dict and than when i switch modes (exerciser or Host mode) the data doesnt apear in the guiso we need to delete the host only in 2 conditions: 1) the host finished to run 2) we are starting a new run on the choosen hosts
        self.printToLog("Finished Running Tests")


    def runTestOnExcerciser(self, lecroyObj, test, lecroyHandler,testLog):
        self.controllerPc.updateTerminalAndLog(self.host, testLog, "Loading Generation Options")
        self.controllerPc.loadGenerationOptionsToExerciser(lecroyObj,os.getcwd() + "\\" + test.generationoptions,lecroyHandler)
        self.controllerPc.updateTerminalAndLog(self.host, testLog, test.generationoptions + " has been loaded")
        self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Init Script Started")
        result = self.controllerPc.startGenerationScriptWithExerciser(lecroyHandler, lecroyObj, self.getTrainerInitScriptFullPathForExerciserFromTestConf(test), self.host, testLog, self.controllerPc)
        if not result: #TODO look at this
            return False
        if self.controllerPc.verifyGenerationScriptOnExerciserFinished(lecroyHandler):
            self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Init Script Finished")
            self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Script Started")
            result = self.controllerPc.startGenerationScriptWithExerciser(lecroyHandler, lecroyObj, self.getTrainerScriptPathForExerciserFromTestConf(test), self.host, testLog, self.controllerPc)
            if not result: #TODO look at this
                return False
            if self.controllerPc.verifyGenerationScriptOnExerciserFinished(lecroyHandler):
                self.controllerPc.updateTerminalAndLog(self.host, testLog, "Trainer Script Finished")
                return True

    def runSequanceOfOperations(self, test, testLog):
        for operation in test.flowoperations:
            self.printToLog("starting Operations= " + operation['name'])
            operationOutPut = getOperationObject(operation).opraionObj.runOp(self, self.controllerPc, self.host, testLog, operation['params'] if isinstance(operation, dict) else [])
            if not operationOutPut:
                self.controllerPc.updateTerminalAndLog(self.host, testLog, (operation['name'] + " Op failed"))
                self.printToLog("finished Operations= " + operation['name'] + ", Op failed")
                return False
            self.printToLog("finished Operations= " + operation['name'] + ", Op succeeded")
        return True
