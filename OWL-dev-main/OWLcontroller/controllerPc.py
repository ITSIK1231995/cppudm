import json
import sys
import traceback
from PyQt5.uic.properties import QtWidgets
from configControl.confParser import confParser
from hostPcTestsRunner import hostPcTestsRunner
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
        self.runtimeHostPcsData = {}
        self.preRunValidationErorrs = {}
        self.currentDefaultConfigurationLoadedName = conf[:-5] #TODO need to think about the .json things
        self.configs = confParser(self).parseAll(loadConf=conf)
        validator = Validator(self)
        self.haltThreads = False
        self.currentSystemExecutionMode = self.getDefaultExeutionModeFromDefaultConfiguration()
        self.firstGuiInit = True # preRunValidationErorrs should be displayed only if its the first GUI init
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

    def createLecroyHandlerInstance(self):  #TODO  look at this
        lecroyHandler = lecroy.lecroyMain.lecroyHandler(self) #TODO need to change lecroyMain.py to lecroyMain.py
        return lecroyHandler

    def startRecordingWithAnalyzer(self, lecroyHandler, SavedTraceFullPathAndName, RecordOptionFilePath, hostPc, testLog):
        return lecroyHandler.startRecordingWithAnalyzer(RecordOptionFilePath, SavedTraceFullPathAndName, hostPc, testLog)

    def stopRecordingWithAnalyzer(self, lecroyHandler):
        lecroyHandler.stopAnalyzerRecording()

    def loadGenerationOptionsToExerciser(self, lecroyObj, generationOptionFullPath, lecroyHandler):
        lecroyHandler.loadGenerationOptionToExerciser(lecroyObj, generationOptionFullPath)

    def startGenerationScriptWithExerciser(self,lecroyHandler,lecroyObj,generationScriptFullPathAndName):
        return lecroyHandler.startGenerationScriptOnExerciser(lecroyObj, generationScriptFullPathAndName)

    def verifyGenerationScriptOnExerciserFinished(self,lecroyHandler):
        return lecroyHandler.verifyExerciserGenerationScriptFinished()

    def threadMain(self,hostPc):
        hostPcTestsRunner(self, hostPc).runAllTests()

    def startVSE(self,traceFullPathAndName, vScriptFullPathAndName, hostPc,testLog):
        return verificationScriptEngine().startVerificationScript(traceFullPathAndName, vScriptFullPathAndName, hostPc, testLog, self)

    #for each hostPc we create a thread that well manage the execution of its tests
    def dispatchThreads(self):
        logging.info("dispatching Threads")
        self.runtimeHostPcsData = {}
        if self.isCurrentExecutionModeIsHostPcMode(): #TODO this function duplicated need to put in a common place to all of this - some utils to all system
            hosts = self.configs.defaultConfContent['hostPCs'] #TODO when adding the execciser mode - need to add here an if statement to check which mode i am now, and than to send to the threadMain instead of hostPc , need to send generic host and instead of "IP" to te host need to send identifier the identifier will include IP when its host pc mdoe and maybe ID or serial number when it is excerciser mode , after that in the "hostPcTestRunner" i will get in the _init__ function the host and the indetifeir and will use it in the hostPcTestRunner, in addition in the hostPcTestRunner i will add a function that calls the controller and ask him to activate the xcerciser instead of activationg the sequcne of operation that way the class of HostPcTestRunner will support both execiser and host pc
        else:
            hosts = self.configs.defaultConfContent["Exercisers"]
        for hostPc in hosts:
            if hostPc["checked"]:
                self.runtimeHostPcsData[hostPc["IP"]] = {"terminal": ""}
                _thread.start_new_thread(self.threadMain,(hostPc,))

    def updateTestStatusInRunTime(self,hostPc,test):
        self.view.updateTestStatusLblInRunTime(hostPc,test)

    def updateUiWithHostNewStatus(self, hostPcWithNewState):
        self.view.updateHostPcLabels(hostPcWithNewState)

    def savedDefaultConfContentIntoJson(self,fileName):
        logging.info("Saving new Default Conf Content")
        defaultConfName = fileName  + ".json"  #TODO go over this after loading a file the currentfilename on the self has .json in the end so in that case we dont need to add a .json to the file name
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
        currentDatetime = self.getCurrentTime()
        terminalAddition = currentDatetime + "    " + update.strip() + "\n"
        print (terminalAddition)
        self.runtimeHostPcsData[host["IP"]]['terminal'] += terminalAddition
        self.updateguiTerminal(host)
        if testLog is not None:
            testLog.write(terminalAddition)
            testLog.flush()

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
        self.startExecutionForHostPcSystemMode()

    def stopExecution(self):
        self.stopExecutionForHostPcSystemMode()

    def startExecutionForHostPcSystemMode(self):
        self.haltThreads = False
        self.dispatchThreads()
        logging.info("Running tests")
        print("Running tests")

    def stopExecutionForHostPcSystemMode(self):
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
