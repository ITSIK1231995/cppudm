import configparser

from PyQt5.uic.properties import QtWidgets
from configControl.confParser import confParser
from configControl.confParserLM import confParserLM
from hostPcTestsRunner import hostPcTestsRunner
from UI.GUI.viewGui import *
import _thread

from OWLcontroller.UI.GUI.viewGui import mainWindow


class ControllerPc():

    def __init__(self):
        self.configs = confParser().parseAll()
        self.GUIInit()
        self.runtimeHostPcsData = {}

    def threadMain(self,hostPc):
        hostPcTestsRunner(self, hostPc).runAllTests()

    #for each hostPc we create a thread that well manage the execution of its tests
    def dispatchThreads(self):
        self.runtimeHostPcsData = {}
        hostPcs = self.configs.defaultConfContent['hostPCs']
        for hostPc in hostPcs:
            if hostPc["checked"]:
                port = self.configs.defaultConfContent['hostPcServerPort']['min']
                self.runtimeHostPcsData[hostPc["IP"]] = {"Port": port, "terminal": ""}
                port += 1
                _thread.start_new_thread(self.threadMain,(hostPc,))


    def GUIInit(self):
        app = QtWidgets.QApplication(sys.argv)
        QMainWindow = QtWidgets.QMainWindow()
        self.view = mainWindow()
        self.view.setupUi(QMainWindow,self)
        QMainWindow.show()
        app.exec_()

    def startExecution(self):
        self.dispatchThreads()
        print("running tests")

    def stopExecution(self):
        print("stopping tests")



controllerPc = ControllerPc()