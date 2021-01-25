import configparser
from configControl.confParser import confParser
from configControl.confParserLM import confParserLM
from hostPcTestsRunner import hostPcTestsRunner
from UI.GUI.viewGui import *
import _thread


class ControllerPc():
    def __init__(self):
        self.configs = confParser().parseAll()
        self.GUIInit()

    def threadMain(self,hostPc):
        hostPcTestsRunner(self, hostPc).runAllTests()
    #for eatch hostPc we create a thread that well manage the execution of its tests
    def dispatchThreads(self):
        hostPcs = self.configs.defaultConfContent['hostPCs']
        for hostPc in hostPcs:
            if hostPc["checked"]:
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
        print("runing tests")

    def stopExecution(self):
        print("stoping tests")



controllerPc = ControllerPc()