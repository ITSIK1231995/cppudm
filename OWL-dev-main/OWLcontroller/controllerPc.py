import configparser
import datetime
import json

from PyQt5.uic.properties import QtWidgets
from configControl.confParser import confParser
from configControl.confParserLM import confParserLM
from hostPcTestsRunner import hostPcTestsRunner
from UI.GUI.viewGui import *
import _thread
from datetime import datetime
from UI.GUI.viewGui import mainWindow
from datetime import date

class ControllerPc():

    def __init__(self,conf='defaultConfiguration.json'):
        self.configs = confParser().parseAll(loadConf=conf)
        self.runtimeHostPcsData = {}
        self.GUIInit()

    def reload(self,conf):
        if conf is not "":
            self.configs = confParser().parseAll(loadConf=conf)
            self.runtimeHostPcsData = {}
            self.GUIInit()

    def threadMain(self,hostPc):
        hostPcTestsRunner(self, hostPc).runAllTests()

    #for each hostPc we create a thread that well manage the execution of its tests
    def dispatchThreads(self):
        self.runtimeHostPcsData = {}
        hostPcs = self.configs.defaultConfContent['hostPCs']
        for hostPc in hostPcs:
            if hostPc["checked"]:
                self.runtimeHostPcsData[hostPc["IP"]] = {"terminal": ""}
                _thread.start_new_thread(self.threadMain,(hostPc,))

    def updateTestStatusInRunTime(self,hostPc,test,testStatus):
        self.runtimeHostPcsData[hostPc["IP"]][test.testname] = testStatus
        self.view.updateTestStatusLblInRunTime(hostPc,test,testStatus)

    def savedDefaultConfContentIntoJson(self):
        now = datetime.now()
        currTime = now.strftime("%H:%M:%S")
        currTime = currTime.replace(":","_")
        defaultConfName = 'defaultConfiguration_New_' + currTime + ".json"
        with open(defaultConfName, 'w+') as fout:
            json_dumps_str = json.dumps(self.configs.defaultConfContent, indent=4)
            print(json_dumps_str, file=fout)

    def updateRunTimeState(self,hostPc,update):
        print (update)
        self.runtimeHostPcsData[hostPc["IP"]]['terminal'] += update.strip() +"\n"
        self.updateguiTerminal(hostPc)

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
        self.dispatchThreads()
        print("running tests")

    def stopExecution(self):
        print("stopping tests")



controllerPc = ControllerPc()