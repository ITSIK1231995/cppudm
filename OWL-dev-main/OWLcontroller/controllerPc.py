import configparser
from configControl.confParser import confParser
from configControl.confParserLM import confParserLM
from hostPcTestEnvClient import hostPcTestEnvClient
from UI.viewGui import *

class controllerPc():
    def __init__(self):
        parserResults = (confParser().parseAll())
        # self.legacyTestsByGroup = parserResults.legacyMode.legacyTestsByGroup
        # self.legacyFlowOperationsTestsByGroups = parserResults.legacyMode.legacyFlowOperationsTestsByGroups
        # self.testsByGroupErrinj = parserResults.ErrinjMode.testsByGroupErrinj
        # self.defaultConfContent = parserResults.defaultConfContent
        self.configs = parserResults
        # # #  Host Pc server case
        # hostPcTestEnvClient().runSequanceOfOperations([{'operation': 'runCommandViaCmd', 'param': "ipconfig"}
        #                                      , 'shutdown', 'sleep', 'hibernate',
        #                                      {'operation': 'wait', 'param': "5"}])


        #hostPcTestEnvClient().runSequanceOfOperations(self.legacyFlowOperationsTestsByGroups['Hermes'][1].flowoperations)
        self.GUIInit()


    def GUIInit(self):
        app = QtWidgets.QApplication(sys.argv)
        QMainWindow = QtWidgets.QMainWindow()
        self.view = mainWindow()
        self.view.setupUi(QMainWindow,self)
        QMainWindow.show()
        app.exec_()






controllerPc()