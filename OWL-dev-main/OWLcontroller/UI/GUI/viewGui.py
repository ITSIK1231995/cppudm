import os

import systemModes
from UI.GUI import browser
from UI.GUI.ScrollLabel import ScrollLabel
from UI.GUI.exerHostGroupBox import exerHostGroupBox
from UI.GUI.groupsDropDown import *
from UI.GUI.browser import browser
from UI.GUI.TestsGroupBox import *
from UI.GUI.preferencesEditor import *
from PyQt5.QtWidgets import (
    QStackedLayout,
    QWidget, QMenu, QAction)
from collections import OrderedDict
import logging
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
from Utils import getHostsDictFromDefaultConfigurationForCurrentExecutionMode


class mainWindow(object): #TODO  need to make this pretty and to work on top labels in the app
    def setupUi(self, QMainWindow, controller):
        self.controller = controller
        self.displayPreRunValidationErorrs() if controller.firstGuiInit else ""


        QMainWindow.setObjectName("skippedTestsNumber")
        QMainWindow.resize(840, 666)
        QMainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(QMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.currentHost = None
        #QMainWindow.setWindowIcon(QtGui.QIcon(os.getcwd() + r'\UI\GUI\pictures\Owl.jpg'))
        self.createTestScreens()
        self.createTerminal(QMainWindow)

        self.hostExercisersGroupBox = exerHostGroupBox(self.centralwidget, self)
        self.selectGroupBox = groupsDropDown(self.centralwidget, self)

        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 30, 815, 111))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 759, 109))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.runTests = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.runTests.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.runTests.setObjectName("runTests")
        self.runTests.clicked.connect(self.runBtnPressed)
        self.runTests.setStyleSheet("background-color: rgb(0, 204, 102);")
        self.stopButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.stopButton.setGeometry(QtCore.QRect(90, 50, 75, 23))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.clicked.connect(self.stopBtnPressed)
        self.stopButton.setStyleSheet("background-color: rgb(255, 102, 102);")
        self.totalTestsNumber_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.totalTestsNumber_2.setGeometry(QtCore.QRect(540, 40, 20, 20))
        self.totalTestsNumber_2.setIndent(1)
        self.totalTestsNumber_2.setObjectName("totalTestsNumber_2")
        self.totalTestsLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.totalTestsLabel.setGeometry(QtCore.QRect(530, 70, 47, 14))
        self.totalTestsLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.totalTestsLabel.setAutoFillBackground(False)
        self.totalTestsLabel.setObjectName("totalTestsLabel")
        self.lineTotal = QtWidgets.QFrame(self.scrollAreaWidgetContents_4)
        self.lineTotal.setGeometry(QtCore.QRect(510, 30, 20, 61))
        self.lineTotal.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineTotal.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineTotal.setObjectName("lineTotal")
        self.linePassed = QtWidgets.QFrame(self.scrollAreaWidgetContents_4)
        self.linePassed.setGeometry(QtCore.QRect(570, 30, 20, 61))
        self.linePassed.setFrameShape(QtWidgets.QFrame.VLine)
        self.linePassed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linePassed.setObjectName("linePassed")
        self.passedTestsLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.passedTestsLabel.setGeometry(QtCore.QRect(590, 70, 47, 14))
        self.passedTestsLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.passedTestsLabel.setAutoFillBackground(False)
        self.passedTestsLabel.setObjectName("passedTestsLabel")
        self.passedTestsNumber = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.passedTestsNumber.setGeometry(QtCore.QRect(600, 40, 31, 21))
        self.passedTestsNumber.setIndent(1)
        self.passedTestsNumber.setObjectName("passedTestsNumber")
        self.lineFailed = QtWidgets.QFrame(self.scrollAreaWidgetContents_4)
        self.lineFailed.setGeometry(QtCore.QRect(630, 30, 20, 61))
        self.lineFailed.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineFailed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineFailed.setObjectName("lineFailed")
        self.failedTestsNumber = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.failedTestsNumber.setGeometry(QtCore.QRect(660, 40, 20, 20))
        self.failedTestsNumber.setIndent(1)
        self.failedTestsNumber.setObjectName("failedTestsNumber")
        self.failedTestsLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.failedTestsLabel.setGeometry(QtCore.QRect(650, 70, 47, 14))
        self.failedTestsLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.failedTestsLabel.setAutoFillBackground(False)
        self.failedTestsLabel.setObjectName("failedTestsLabel")
        self.lineSkipped = QtWidgets.QFrame(self.scrollAreaWidgetContents_4)
        self.lineSkipped.setGeometry(QtCore.QRect(690, 30, 20, 61))
        self.lineSkipped.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineSkipped.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSkipped.setObjectName("lineSkipped")
        self.skippedTestsLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.skippedTestsLabel.setGeometry(QtCore.QRect(710, 70, 47, 14))
        self.skippedTestsLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.skippedTestsLabel.setAutoFillBackground(False)
        self.skippedTestsLabel.setObjectName("skippedTestsLabel")
        self.skippedTestsNumber_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.skippedTestsNumber_2.setGeometry(QtCore.QRect(720, 40, 20, 20))
        self.skippedTestsNumber_2.setIndent(1)
        self.skippedTestsNumber_2.setObjectName("skippedTestsNumber_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_4)

        QMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menufiles = QtWidgets.QMenu(self.menubar)
        self.menufiles.setObjectName("menufiles")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        QMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QMainWindow)
        self.statusbar.setObjectName("statusbar")
        QMainWindow.setStatusBar(self.statusbar)

        self.menu = QMenu()

        self.actionSaveConfigurationInsteadTheCurrentConfigurationFile = QAction(QMainWindow)
        self.actionSaveConfigurationInsteadTheCurrentConfigurationFile.setObjectName("actionSave_configuration")
        self.menu.addAction(self.actionSaveConfigurationInsteadTheCurrentConfigurationFile)
        self.actionSaveConfigurationInsteadTheCurrentConfigurationFile.triggered.connect(self.saveConfBtnClicked)

        self.actionSave_configuration = QAction(QMainWindow)
        self.actionSave_configuration.setObjectName("actionSave_configuration")
        self.menu.addAction(self.actionSave_configuration)
        self.actionSave_configuration.triggered.connect(self.saveConfAsBtnClicked)


        self.actionLoad_configuration = QtWidgets.QAction(QMainWindow)
        self.actionLoad_configuration.setObjectName("actionLoad_configuration")
        self.actionSettings = QtWidgets.QAction(QMainWindow)
        self.menu.addAction(self.actionLoad_configuration)
        self.actionLoad_configuration.triggered.connect(self.loadConfBtnClicked)
        self.actionSettings.setObjectName("actionSettings")

        self.actionPreferences = QtWidgets.QAction(QMainWindow)
        self.actionPreferences.triggered.connect(self.runPreferencesEditor)
        self.actionPreferences.setObjectName("actionPreferences")

        self.actionLegacy_Mode_Host_PC = QtWidgets.QAction(QMainWindow)
        self.actionLegacy_Mode_Host_PC.setObjectName("actionLegacy_Mode_Host_PC")
        self.actionLegacy_Mode_Exerciser = QtWidgets.QAction(QMainWindow)
        self.actionLegacy_Mode_Exerciser.setObjectName("actionLegacy_Mode_Exerciser")
        # disable Errinj Mode has it canceled for now
        # self.actionErrinj_Mode = QtWidgets.QAction(skippedTestsNumber)
        # self.actionErrinj_Mode.setObjectName("actionErrinj_Mode")
        self.menufiles.addAction(self.actionSaveConfigurationInsteadTheCurrentConfigurationFile)
        self.menufiles.addAction(self.actionSave_configuration)
        self.menufiles.addAction(self.actionLoad_configuration)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionSettings)

        self.menuTools.addAction(self.actionPreferences)
        self.menuMode.addAction(self.actionLegacy_Mode_Host_PC)
        self.menuMode.addAction(self.actionLegacy_Mode_Exerciser)
        # self.menuMode.addAction(self.actionErrinj_Mode)  # disable Errinj Mode has it canceled for now
        self.menubar.addAction(self.menufiles.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(QMainWindow)
        # self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(QMainWindow)

    def displayPreRunValidationErorrs(self):
        if len(self.controller.preRunValidationErorrs) != 0:
            if 'corruptedSequenceFile' in self.controller.preRunValidationErorrs:
                outPutcorruptedSequenceFile = ""
                for curraptedSeqfile in self.controller.preRunValidationErorrs['corruptedSequenceFile']:
                    for sequenceFileName, sequenceFileError in curraptedSeqfile.items():
                        outPutcorruptedSequenceFile += str(sequenceFileError)
                #GUIUtills.PopUpWarning(outPutcorruptedSequenceFile) # The recommendation is to have this option not as a comment but the user required to erase this so instead - it will be written in the log file
                logging.warning(outPutcorruptedSequenceFile)
                self.controller.exitSystem()
            for listOfErrors in self.controller.preRunValidationErorrs:
                for Error in self.controller.preRunValidationErorrs[listOfErrors]:
                    #GUIUtills.PopUpWarning(Error) The recommendation is to have this option not as a comment but the user required to erase this so instead - it will be written in the log file
                    logging.warning(Error)


    def loadConfBtnClicked(self):
        fileChoosedPath = browser("Load Configuration").getChoosedFolderName("Load Configuration","load")
        if fileChoosedPath is not "":
            self.controller.currentDefaultConfigurationLoadedName = fileChoosedPath # The split remove the .json from the file's name
            self.controller.reload(fileChoosedPath)

    def getFileNameFromUser(self):
        return browser("Save Configuration").saveFileDialog("Save Configuration")

    def saveConfAsBtnClicked(self):
        fileName = self.getFileNameFromUser()
        if fileName is not None:
            self.controller.savedDefaultConfContentIntoJson(fileName + '.json')

    def saveConfBtnClicked(self):
        self.controller.savedDefaultConfContentIntoJson(self.controller.currentDefaultConfigurationLoadedName)

    def retranslateUi(self, skippedTestsNumber):
        self._translate = QtCore.QCoreApplication.translate
        skippedTestsNumber.setWindowTitle(self._translate("skippedTestsNumber", "O.W.L"))
        self.selectGroupBox.retranslateUi()
        self.hostExercisersGroupBox.retranslateUi()
        self.retranslateUiTestsGroupBoxs()
        self.runTests.setText(self._translate("skippedTestsNumber", "Run"))
        self.stopButton.setText(self._translate("skippedTestsNumber", "Stop"))
        self.totalTestsNumber_2.setText(self._translate("skippedTestsNumber", "0"))
        self.totalTestsLabel.setText(self._translate("skippedTestsNumber", "Total"))
        self.passedTestsLabel.setText(self._translate("skippedTestsNumber", "Passed"))
        self.passedTestsLabel.setStyleSheet("background-color:rgb(0,255,0)")
        self.passedTestsNumber.setText(self._translate("skippedTestsNumber", "0"))
        self.failedTestsNumber.setText(self._translate("skippedTestsNumber", "0"))
        self.failedTestsLabel.setText(self._translate("skippedTestsNumber", "Failed"))
        self.failedTestsLabel.setStyleSheet("background-color:rgb(255,102,102)")
        self.skippedTestsLabel.setText(self._translate("skippedTestsNumber", "Skipped"))
        self.skippedTestsLabel.setStyleSheet("background-color:rgb(255,178,102)")
        self.skippedTestsNumber_2.setText(self._translate("skippedTestsNumber", "0"))
        self.menufiles.setTitle(self._translate("skippedTestsNumber", "Files"))
        self.menuHelp.setTitle(self._translate("skippedTestsNumber", "Help"))
        self.menuTools.setTitle(self._translate("skippedTestsNumber", "Tools"))
        self.menuAbout.setTitle(self._translate("skippedTestsNumber", "About"))
        self.menuMode.setTitle(self._translate("skippedTestsNumber", "Mode"))

        self.actionSaveConfigurationInsteadTheCurrentConfigurationFile.setText(self._translate("skippedTestsNumber", "Save Configuration"))
        self.actionSave_configuration.setText(self._translate("skippedTestsNumber", "Save Configuration As"))
        self.actionLoad_configuration.setText(self._translate("skippedTestsNumber", "Load Configuration"))

        self.actionSettings.setText(self._translate("skippedTestsNumber", "Settings"))
        self.actionPreferences.setText(self._translate("skippedTestsNumber", "Preferences"))
        self.actionLegacy_Mode_Host_PC.setText(self._translate("skippedTestsNumber", "System Under Test"))
        self.actionLegacy_Mode_Host_PC.triggered.connect(self.hostPcModeChoosed)
        self.actionLegacy_Mode_Exerciser.setText(self._translate("skippedTestsNumber", "Exerciser"))
        self.actionLegacy_Mode_Exerciser.triggered.connect(self.exerciserModeChoosed)
        # self.actionErrinj_Mode.setText(self._translate("skippedTestsNumber", "Errinj Mode"))  # disable Errinj Mode has it canceled for now

    def runBtnPressed(self):
        self.controller.startExecution()

    def stopBtnPressed(self):
        self.controller.stopExecution()

    def exerciserModeChoosed(self):
        self.controller.currentSystemExecutionMode = systemModes.systemExecutionModes.LEGACY_MODE_EXCERCISER
        self.controller.configs.defaultConfContent['defaultExecutionMode'] = "Exerciser"
        self.controller.firstGuiInit = False
        self.controller.GUIInit()

    def hostPcModeChoosed(self):
        self.controller.currentSystemExecutionMode = systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC
        self.controller.configs.defaultConfContent['defaultExecutionMode'] = "Host Pc"
        self.controller.firstGuiInit = False
        self.controller.GUIInit()

    # in this functions we create a stack of tests GroupBox, watch per group, in order to switch accordingly
    def createTestScreens(self):
        self.widget = QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(285, 150, 540, 280))
        self.stackedLayout = QStackedLayout(self.widget)
        self.testsGroupBoxWithLeveltuples = OrderedDict()
        TestsGroupBoxWithLeveltuple = namedtuple('TestRow', ['testsGroupBox', 'stackLevel'])
        stackLevel = 0
        testsByGroupDictForCurrentSystemMode = getTestsByGroupDictForCurrentSystemExecutionMode(self.controller)
        if self.controller.configs:
            for groupName, groupTests in testsByGroupDictForCurrentSystemMode.items():
                self.testsGroupBoxWithLeveltuples[groupName] = TestsGroupBoxWithLeveltuple(
                    TestsGroupBox(self.centralwidget, self, groupName, groupTests)
                    , stackLevel)
                self.stackedLayout.addWidget(self.testsGroupBoxWithLeveltuples[groupName].testsGroupBox)
                stackLevel += 1

    def retranslateUiTestsGroupBoxs(self):
        for groupName, testsGroupBoxWithLevelTuple in self.testsGroupBoxWithLeveltuples.items():
            testsGroupBoxWithLevelTuple.testsGroupBox.retranslateUi()
        self.setDefultHostPc()

    def removeTestStatusLblFromPreviousExecution(self, groupName): #TODO look at this
        self.testsGroupBoxWithLeveltuples[groupName].testsGroupBox.retranslateUi()

    def setDefultHostPc(self):
        hostLists = getHostsDictFromDefaultConfigurationForCurrentExecutionMode(self.controller)
        if len(hostLists) != 0:
            defaultHostPC = hostLists[0]
            self.currentHost = defaultHostPC
            self.setNewHostPC(defaultHostPC)

    def getCurrentTestsGroupBoxWithLevelTuple(self):
        currentTGBStackLevel = self.stackedLayout.currentIndex()
        return next((TGB for TGB in self.testsGroupBoxWithLeveltuples.values() if TGB.stackLevel == currentTGBStackLevel), None)

    def setNewHostPC(self, host):
        self.currentHost = host
        if self.currentHost is not None:
            self.stackedLayout.setCurrentIndex(self.testsGroupBoxWithLeveltuples[host['groupName']].stackLevel)
            self.selectGroupBox.changeSelected(host['groupName'])
            testsGroupBoxWithLevelTuple = self.getCurrentTestsGroupBoxWithLevelTuple()
            testsGroupBoxWithLevelTuple.testsGroupBox.loadHostPCSTestParams(host)
            self.setTerminal(host)
        else:  # if no host is selected clear all
            for testsGroupBoxWithLevel in self.testsGroupBoxWithLeveltuples.values():
                testsGroupBoxWithLevel.testsGroupBox.clearAll()
            self.terminalLbl.setText("")

    def setTerminal(self, host):
        if host["IP"] in self.controller.runtimeHostPcsData:
            self.terminalLbl.setText(self.controller.runtimeHostPcsData[host["IP"]]['terminal'])
        else:
            self.terminalLbl.setText("")

    def updateCurrentTernimal(self, host):
        if self.currentHost == host:
            self.terminalLbl.setText(self.controller.runtimeHostPcsData[host["IP"]]['terminal'])

    def createTerminal(self, skippedTestsNumber):
        self.terminalLbl = ScrollLabel(skippedTestsNumber)
        self.terminalLbl.setGeometry(QtCore.QRect(285, 470, 540, 180))
        self.terminalLbl.setObjectName("Terminal")
        self.terminalLbl.setStyleSheet("background-color:rgb(224,224,224)")
        self.terminalLbl.setText("")

    def setDisplayedTestGroup(self, groupName):
        if self.currentHost is not None:
                self.currentHost['groupName'] = groupName
                self.currentHost['tests'] = {}
                self.setNewHostPC(self.currentHost)
        else:
            self.stackedLayout.setCurrentIndex(self.testsGroupBoxWithLeveltuples[groupName].stackLevel)

    def updateTestStatusLblInRunTime(self, host, test):
        if self.currentHost == host:
            self.getCurrentTestsGroupBoxWithLevelTuple().testsGroupBox.updateTestStatusLbl(host, test.testname)

    def updateUiSummerizeBox(self,numOfPassTests,numOffailedTests,numOfTestToRun): #TODO look at this
        self.passedTestsNumber.setText(self._translate("skippedTestsNumber", str(numOfPassTests)))
        self.failedTestsNumber.setText(self._translate("skippedTestsNumber", str(numOffailedTests)))
        self.totalTestsNumber_2.setText(self._translate("skippedTestsNumber", str(numOfTestToRun)))
    def updateHostPcLabels(self, hostPcWithNewStatus):
        self.hostExercisersGroupBox.hostPcRows[hostPcWithNewStatus["IP"]].checkBox.setStyleSheet(
            COLOR_CONVERTER[self.controller.runtimeHostPcsData[hostPcWithNewStatus["IP"]]["hostPcLblColor"]])

    def runPreferencesEditor(self):
        PreferencesEditor(self).exec()
