import json
import sys
import traceback
from PyQt5.uic.properties import QtWidgets

import systemModes
from Utils import getCurrentTime
from configControl.confParser import confParser
from hostTestsRunner import hostTestsRunner
from UI.GUI.viewGui import *
import _thread
from UI.GUI.viewGui import mainWindow
from datetime import datetime
import datetime
from lecroy.verificationScriptEngine import verificationScriptEngine
from validator import *
import lecroy.lecroyMain

class ControllerPc():
    def __init__(self,conf='defaultConfiguration.json'):
        logging.info("ControllerPc started")
        logging.info("Parsing configs")
        self.preparingSystemForExecution(conf)
        self.firstGuiInit = True # preRunValidationErorrs should be displayed only if its the first GUI init
        self.currentDefaultConfigurationLoadedName = conf
        logging.info("Initiating GUI")
        self.GUIInit()

    def reload(self,conf):
        logging.info("Parsing reloading")
        logging.info("Parsing configs")
        self.preparingSystemForExecution(conf)
        logging.info("Initiating GUI")
        self.GUIInit()

    def preparingSystemForExecution(self, conf):
        self.runtimeHostPcsData = {}
        self.preRunValidationErorrs = {}
        self.configs = confParser(self).parseAll(loadConf=conf)
        validator = Validator(self)
        self.haltThreads = False
        self.currentSystemExecutionMode = self.getDefaultExeutionModeFromDefaultConfiguration()

    def createLecroyHandlerInstance(self):
        lecroyHandler = lecroy.lecroyMain.lecroyHandler(self)
        return lecroyHandler

    def startRecordingWithAnalyzer(self, lecroyHandler, SavedTraceFullPathAndName, RecordOptionFilePath, host, testLog):
        return lecroyHandler.startRecordingWithAnalyzer(RecordOptionFilePath, SavedTraceFullPathAndName, host, testLog)

    def stopRecordingWithAnalyzer(self, lecroyHandler):
        lecroyHandler.stopAnalyzerRecording()

    def loadGenerationOptionsToExerciser(self, lecroyObj, generationOptionFullPath, lecroyHandler):
        lecroyHandler.loadGenerationOptionToExerciser(lecroyObj, generationOptionFullPath)

    def startGenerationScriptWithExerciser(self,lecroyHandler,lecroyObj,generationScriptFullPathAndName,host,testLog,controllerPc):
        return lecroyHandler.startGenerationScriptOnExerciser(lecroyObj, generationScriptFullPathAndName,host,testLog,controllerPc)

    def verifyGenerationScriptOnExerciserFinished(self,lecroyHandler):
        return lecroyHandler.verifyExerciserGenerationScriptFinished()

    def threadMain(self, host):
        hostTestsRunner(self, host).runAllTests()

    def startVSE(self, traceFullPathAndName, vScriptFullPathAndName, host, testLog):
        return verificationScriptEngine().startVerificationScript(traceFullPathAndName, vScriptFullPathAndName, host, testLog, self)

    #for each hostPc we create a thread that well manage the execution of its tests
    def dispatchThreads(self):
        logging.info("dispatching Threads")
        #self.runtimeHostPcsData = {}
        hosts = getHostsDictFromDefaultConfigurationForCurrentExecutionMode(self)
        # TODO when adding the execciser mode - need to add here an if statement to check which mode i am now, and than to send to the threadMain instead of host , need to send generic host and instead of "IP" to te host need to send identifier the identifier will include IP when its host pc mdoe and maybe ID or serial number when it is excerciser mode , after that in the "hostPcTestRunner" i will get in the _init__ function the host and the indetifeir and will use it in the hostPcTestRunner, in addition in the hostPcTestRunner i will add a function that calls the controller and ask him to activate the xcerciser instead of activationg the sequcne of operation that way the class of HostPcTestRunner will support both execiser and host pc
        for host in hosts:
            if host["checked"] and host["IP"] not in self.runtimeHostPcsData:
                self.view.removeTestStatusLblFromPreviousExecution(host["groupName"])  # TODO need to figure out if this is the best soulution for erasing all the data from the prevous run
                self.runtimeHostPcsData[host["IP"]] = {"terminal": ""}
                _thread.start_new_thread(self.threadMain,(host,))

    def updateTestStatusInRunTime(self, host, test):
        self.view.updateTestStatusLblInRunTime(host, test)

    def updateUiWithHostNewStatus(self, hostWithNewState):
        self.view.updateHostPcLabels(hostWithNewState)

    def savedDefaultConfContentIntoJson(self,fileName):
        logging.info("Saving new Default Conf Content")
        defaultConfName = fileName
        with open(defaultConfName, 'w+') as fout:
            json_dumps_str = json.dumps(self.configs.defaultConfContent, indent=4)
            print(json_dumps_str, file=fout)

    def getDefaultExeutionModeFromDefaultConfiguration(self):
        if "Host Pc" in self.configs.defaultConfContent['defaultExecutionMode']:
            return systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC
        elif "Exerciser" in self.configs.defaultConfContent['defaultExecutionMode']:
            return systemModes.systemExecutionModes.LEGACY_MODE_EXCERCISER

    def isCurrentExecutionModeIsHostPcMode(self):
        if self.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC:
            return True
        return False

    def updateTerminalAndLog(self, host, testLog, update):
        currentDatetime = getCurrentTime()
        terminalAddition = currentDatetime + "    " + update.strip() + "\n"
        print (terminalAddition)
        self.runtimeHostPcsData[host["IP"]]['terminal'] += terminalAddition
        self.updateGUITerminal(host)
        if testLog is not None:
            testLog.write(terminalAddition)
            testLog.flush()

    def updateGUITerminal(self, hostPc):
        self.view.updateCurrentTernimal(hostPc)

    def updateUiSummerizeBox(self,numOfPassTests,numOffailedTests,numOfTestToRun): #TODO look at this
        self.view.updateUiSummerizeBox(numOfPassTests,numOffailedTests,numOfTestToRun)

    def GUIInit(self):
        self.app = QtWidgets.QApplication.instance()
        while self.app is None:
            try:
                self.app = QtWidgets.QApplication(sys.argv)
                break
            except:
                continue
        self.QMainWindow = QtWidgets.QMainWindow()
        self.view = mainWindow()
        self.view.setupUi(self.QMainWindow,self)
        self.QMainWindow.show()
        self.app.exec_()

    def startExecution(self):

        self.startExecutionForHostSystemMode()

    def stopExecution(self):
        self.stopExecutionForHostSystemMode()

    def startExecutionForHostSystemMode(self):
        self.haltThreads = False
        self.dispatchThreads()
        logging.info("Running tests")
        print("Running tests")

    def stopExecutionForHostSystemMode(self):
        logging.info("Stop pressed, Halting threads")
        self.haltThreads = True
        print("Stopping tests")

    def exitSystem(self):
        exit(0)

if __name__ == '__main__':
    logging.basicConfig(filename='appLog.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        controllerPc = ControllerPc()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.exception("exception on main")
        logging.shutdown()
