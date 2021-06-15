import json
import sys
import traceback
from PyQt5.uic.properties import QtWidgets

from UI.GUI.systemModes import systemExecutionModes
from configControl.confParser import confParser
from hostPcTestsRunner import hostPcTestsRunner
from UI.GUI.viewGui import *
import _thread
from UI.GUI.viewGui import mainWindow
from datetime import datetime
import datetime
from lecroy.verificationScriptEngine import verificationScriptEngine
from validator import *
import lecroy.analyzer

class ControllerPc():
    def __init__(self,conf='defaultConfiguration.json'):
        logging.info("ControllerPc started")
        logging.info("Parsing configs")
        self.runtimeHostPcsData = {}
        self.preRunValidationErorrs = {}
        self.configs = confParser(self).parseAll(loadConf=conf)
        validator = Validator(self)
        self.haltThreads = False
        self.currentSystemExecutionMode = self.getDefaultExeutionModeFromDefaultConfiguration()  #TODO  look at this
        self.firstGuiInit = True # preRunValidationErorrs should be displayed only if its the first GUI init #TODO  look at this
        logging.info("Initiating GUI")
        self.GUIInit()

    def reload(self,conf): #TODO need to put part of this code outside this function and than use the funciton in th __init_ and in the reload
        logging.info("Parsing reloading")
        logging.info("Parsing configs")
        self.runtimeHostPcsData = {}
        self.preRunValidationErorrs = {}
        self.configs = confParser(self).parseAll(loadConf=conf)
        validator = Validator(self)
        self.haltThreads = False
        self.currentSystemExecutionMode = self.getDefaultExeutionModeFromDefaultConfiguration()
        logging.info("Initiating GUI")
        self.GUIInit()

    def createAnalyzerInstance(self):  #TODO  look at this
        analyzerHandler = lecroy.analyzer.analyzerHandler(self)
        return analyzerHandler

    def startRecordingWithAnalyzer(self,analyzerHandler,SavedTraceFullPathAndName,RecordOptionFilePath,hostPc,testLog):
        return analyzerHandler.startRecordingWithAnalyzer(RecordOptionFilePath,SavedTraceFullPathAndName,hostPc,testLog)

    def stopRecordingWithAnalyzer(self, analyzerHandler):
        analyzerHandler.stopRecording()

    def threadMain(self,hostPc): #TODO  need to udnerstand when i seperate the modes here or in the dispatch thread
        hostPcTestsRunner(self, hostPc).runAllTests()

    def startVSE(self,traceFullPathAndName, vScriptFullPathAndName, hostPc,testLog):
        return verificationScriptEngine().startVerificationScript(traceFullPathAndName, vScriptFullPathAndName, hostPc, testLog, self)

    #for each hostPc we create a thread that well manage the execution of its tests
    def dispatchThreads(self):
        logging.info("dispatching Threads")
        self.runtimeHostPcsData = {}
        if self.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC:
            hosts = self.configs.defaultConfContent['hostPCs'] #TODO when adding the execciser mode - need to add here an if statement to check which mode i am now, and than to send to the threadMain instead of hostPc , need to send generic host and instead of "IP" to te host need to send identifier the identifier will include IP when its host pc mdoe and maybe ID or serial number when it is excerciser mode , after that in the "hostPcTestRunner" i will get in the _init__ function the host and the indetifeir and will use it in the hostPcTestRunner, in addition in the hostPcTestRunner i will add a function that calls the controller and ask him to activate the xcerciser instead of activationg the sequcne of operation that way the class of HostPcTestRunner will support both execiser and host pc
        if self.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_EXCERCISER:
            hosts = self.configs.defaultConfContent["Exercisers"]
        for hostPc in hosts:
            if hostPc["checked"]: #TODO  need to udnerstand when i seperate the modes here or in the dispatch thread
                self.runtimeHostPcsData[hostPc["IP"]] = {"terminal": ""}
                _thread.start_new_thread(self.threadMain,(hostPc,))

    def updateTestStatusInRunTime(self,hostPc,test):
        self.view.updateTestStatusLblInRunTime(hostPc,test)

    def updateUiWithHostNewStatus(self, hostPcWithNewState):
        self.view.updateHostPcLabels(hostPcWithNewState)

    def savedDefaultConfContentIntoJson(self,fileName):
        logging.info("Saving new Default Conf Content")
        defaultConfName = fileName  + ".json"
        with open(defaultConfName, 'w+') as fout:
            json_dumps_str = json.dumps(self.configs.defaultConfContent, indent=4)
            print(json_dumps_str, file=fout)

    def getDefaultExeutionModeFromDefaultConfiguration(self):
        if "Host Pc" in self.configs.defaultConfContent['defaultExecutionMode']:
            return systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC
        elif "Exerciser" in self.configs.defaultConfContent['defaultExecutionMode']:
            return systemModes.systemExecutionModes.LEGACY_MODE_EXCERCISER

    def updateRunTimeStateInTerminal(self, hostPc, testLog, update):
        currentDatetime = self.getCurrentTime()
        terminalAddition = currentDatetime + "    " + update.strip() + "\n"
        print (terminalAddition)
        self.runtimeHostPcsData[hostPc["IP"]]['terminal'] += terminalAddition
        self.updateguiTerminal(hostPc)
        if testLog is not None:
            testLog.write(terminalAddition)
            testLog.flush()

    def getCurrentTimeFile(self): # TODO move to utils of the backend
        return self.getCurrentTime().replace("-", "_").replace(":", "_")

    def getCurrentTime(self): # TODO move to utils of the backend
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S"))

    def updateguiTerminal(self,hostPc):
        self.view.updateCurrentTernimal(hostPc)

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
         #TODO  need to udnerstand when i seperate the modes here or in the dispatch thread
        self.startExecutionForHostPcSystemMode()

    def stopExecution(self): #TODO  need to udnerstand when i seperate the modes here or in the dispatch thread
        #TODO  look at this
        self.stopExecutionForHostPcSystemMode()

    def startExecutionForHostPcSystemMode(self): #TODO  look at this
        self.haltThreads = False
        self.dispatchThreads()
        logging.info("Running tests")
        print("Running tests")

    def stopExecutionForHostPcSystemMode(self):  #TODO  look at this
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
