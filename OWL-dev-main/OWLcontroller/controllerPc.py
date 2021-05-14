import json
import sys
import time
import traceback
from PyQt5.uic.properties import QtWidgets
from configControl.confParser import confParser
from hostPcTestsRunner import hostPcTestsRunner
from UI.GUI.viewGui import *
import _thread
from UI.GUI.viewGui import mainWindow
from datetime import datetime
import datetime
from lecroy.VSE import VSE
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
        logging.info("Initiating GUI")
        self.GUIInit()

    def reload(self,conf):
        logging.info("Parsing reloading")
        logging.info("Parsing configs")
        self.runtimeHostPcsData = {}
        self.preRunValidationErorrs = {}
        self.configs = confParser(self).parseAll(loadConf=conf)
        validator = Validator(self)
        self.haltThreads = False
        logging.info("Initiating GUI")
        self.GUIInit()

    def createAnalyzerInstance(self):
        analyzerHandler = lecroy.analyzer.analyzerHandler(self)
        return analyzerHandler

    def startRecordingWithAnalyzer(self,analyzerHandler,test,SavedTraceFullPath,RecordOptionFilePath,hostPc,testLog):
        analyzerHandler.startRecordingWithAnalyzer(RecordOptionFilePath,SavedTraceFullPath,test.testname,hostPc,testLog)

    def stopRecordingWithAnalyzer(self, analyzerHandler):
        analyzerHandler.stopRecording()

    def threadMain(self,hostPc):
        hostPcTestsRunner(self, hostPc).runAllTests()

    def startVSE(self,traceFullPathAndName, vScriptFullPathAndName, hostPc,testLog):
        VSE().startVerificationScriptEngine(traceFullPathAndName, vScriptFullPathAndName,hostPc,testLog,self)

    #for each hostPc we create a thread that well manage the execution of its tests
    def dispatchThreads(self):
        logging.info("dispatching Threads")
        self.runtimeHostPcsData = {}
        hostPcs = self.configs.defaultConfContent['hostPCs']
        for hostPc in hostPcs:
            if hostPc["checked"]:
                self.runtimeHostPcsData[hostPc["IP"]] = {"terminal": ""}
                _thread.start_new_thread(self.threadMain,(hostPc,))

    def updateTestStatusInRunTime(self,hostPc,test):
        self.view.updateTestStatusLblInRunTime(hostPc,test)

    def updateUiWithHostNewStatus(self, hostPcWithNewState):
        self.view.updateHostPcLabels(hostPcWithNewState)

    def savedDefaultConfContentIntoJson(self):
        logging.info("Saving new Default Conf Content")
        currTime = self.getCurrentTimeFile()
        defaultConfName = 'defaultConfiguration_New_' + currTime + ".json"
        with open(defaultConfName, 'w+') as fout:
            json_dumps_str = json.dumps(self.configs.defaultConfContent, indent=4)
            print(json_dumps_str, file=fout)

    def updateRunTimeStateInTerminal(self, hostPc, testLog, update):
        currentDatetime = self.getCurrentTime()
        terminalAddition = currentDatetime + "    " + update.strip() + "\n"
        print (terminalAddition)
        self.runtimeHostPcsData[hostPc["IP"]]['terminal'] += terminalAddition
        self.updateguiTerminal(hostPc)
        if testLog is not None:
            testLog.write(terminalAddition)
            testLog.flush()

    def getCurrentTimeFile(self):
        return self.getCurrentTime().replace("-", "_").replace(":", "_")

    def getCurrentTime(self):
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S"))

    def updateguiTerminal(self,hostPc):
        self.view.updateCurrentTernimal(hostPc)

    def GUIInit(self):
        self.app = QtWidgets.QApplication.instance()
        while self.app is None: # TODO : remove this
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
        self.haltThreads = False
        self.dispatchThreads()
        logging.info("Running tests")
        print("Running tests")

    def stopExecution(self):
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
