from collections import namedtuple
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

from UI.GUI import systemModes
from UI.GUI.colorConvertor import *
from UI.GUI.systemModes import systemExecutionModes
from hostPcTestsRunner import testState

class TestsGroupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,mainWindowRef,groupName,tests):
        super(TestsGroupBox, self).__init__(centralwidget)
        self.controller = mainWindowRef.controller
        self.setObjectName("hostExercisersGroupBox")
        self.vbox = QVBoxLayout()
        self.groupName = groupName
        self.tests = tests
        HostsDictForCurrentSystemMode = self.getHostsDictForCurrentSystemMode() #TODO need to change the host pc to host becasue theres two modes
        if len(HostsDictForCurrentSystemMode) != 0:
            self.myHost = HostsDictForCurrentSystemMode[0]
        else:
            self.myHost = None
        self.testTableSetup()
        self.scrollSetup()
        self.checkAllSetup()


    def getHostsDictForCurrentSystemMode(self):#TODO Go over this and put this in Utils because its duplicate code
        if self.controller.isCurrentExecutionModeIsHostPcMode():
            return self.controller.configs.defaultConfContent["hostPCs"]
        else:
            return self.controller.configs.defaultConfContent["Exercisers"]

    def checkAllSetup(self):
        self.checkAllBox = QtWidgets.QCheckBox(self)
        self.checkAllBox.setGeometry(QtCore.QRect(1, 13, 200, 21))
        self.checkAllBox.setObjectName("checkAllBox")
        self.checkAllBox.clicked.connect(self.onCheckAllClicked)

    def testTableSetup(self):
        self.testsRows = {}
        for test in self.tests:
            groupBox = QtWidgets.QGroupBox()
            groupBox.setObjectName("GroupBox_"+test.testname)
            checkBox = QtWidgets.QCheckBox(groupBox)
            checkBox.setGeometry(QtCore.QRect(0, 1, 230, 21))
            checkBox.setObjectName("testCheckBox_"+test.testname)
            checkBox.clicked.connect(self.onCheckBoxClicked)
            repeatTestBox = QtWidgets.QSpinBox(groupBox)
            repeatTestBox.setGeometry(QtCore.QRect(220, 0, 47, 23))
            repeatTestBox.setObjectName("repeatTestBox_"+test.testname)
            repeatTestBox.setRange(0,1000)
            repeatTestBox.valueChanged.connect(self.repeatTestBoxChanged)
            statusLbl = QtWidgets.QLabel(groupBox)
            statusLbl.setGeometry(QtCore.QRect(300, 3, 150, 14))
            statusLbl.setAlignment(QtCore.Qt.AlignCenter)
            statusLbl.setObjectName("TestState_"+test.testname)
            groupBox.setFixedHeight(25)
            groupBox.setFixedWidth(500)
            self.vbox.addWidget(groupBox)
            TestRowNamedtuple = namedtuple('TestRow', ['checkBox', 'repeatTestBox','statusLbl'])
            self.testsRows[test.testname] = TestRowNamedtuple(checkBox, repeatTestBox, statusLbl)

    def repeatTestBoxChanged(self):
        repeatTestBox = self.sender()
        testName = repeatTestBox.objectName().split('_')[1]
        if self.myHost is not None:
            if testName in self.myHost['tests'].keys():
                self.myHost['tests'][testName]['repeatAmount'] = repeatTestBox.value()
            else:
                self.myHost['tests'][testName] = {"repeatAmount" : repeatTestBox.value(), "checked" : False}

    def onCheckBoxClicked(self):
        clickedCheckBox = self.sender()
        testName = clickedCheckBox.objectName().split('_')[1]
        if self.myHost is not None:
            if testName in self.myHost['tests'].keys():
                self.myHost['tests'][testName]['checked'] = clickedCheckBox.isChecked()
            else:
                self.myHost['tests'][testName] = {"repeatAmount" : 0, "checked" : clickedCheckBox.isChecked()}

    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 30, 540, 250))

    def retranslateUi(self):
        self.setToolTip("tests list")
        self.setTitle(self.groupName + " Tests")
        self.setStyleSheet("background-color:rgb(224,224,224)")
        self.checkAllBox.setText("Check All")
        for test in self.tests:
            self.testsRows[test.testname].checkBox.setText(test.testname)
            self.testsRows[test.testname].statusLbl.setText("Not Started")
            self.testsRows[test.testname].statusLbl.setStyleSheet("background-color: rgb(192, 192, 192);")

    def updateTestStatusLbl(self,hostPc,testName): #
        _translate = QtCore.QCoreApplication.translate
        parsingTestRepeatsSummary = self.prepareTestRepeatsSummary(hostPc, testName)
        self.testsRows[testName].statusLbl.setText(_translate("skippedTestsNumber", parsingTestRepeatsSummary.resultsStr))
        self.testsRows[testName].statusLbl.setStyleSheet(COLOR_CONVERTER[parsingTestRepeatsSummary.stateForColor])

    def prepareTestRepeatsSummary(self, hostPc, testName):
        parsedTestRepeatsSummary = namedtuple('parsedTestRepeatsSummary', ['stateForColor', 'resultsStr'])
        if self.controller.runtimeHostPcsData[hostPc["IP"]][testName]["testRepeatsCurrStatus"].name == testState.RUNNING.name:
            return parsedTestRepeatsSummary(testState.RUNNING, "Running (Passed: " + str(self.controller.runtimeHostPcsData[hostPc["IP"]][testName]['testRepeatsSummary'][testState.PASSED]) + " Failed: " + str(self.controller.runtimeHostPcsData[hostPc["IP"]][testName]['testRepeatsSummary'][testState.FAILED]) + ")")
        if self.controller.runtimeHostPcsData[hostPc["IP"]][testName]['testRepeatsSummary'][testState.FAILED] > 0:
            return parsedTestRepeatsSummary(testState.FAILED, " Passed: " + str(self.controller.runtimeHostPcsData[hostPc["IP"]][testName]['testRepeatsSummary'][testState.PASSED]) + " Failed: " + str(self.controller.runtimeHostPcsData[hostPc["IP"]][testName]['testRepeatsSummary'][testState.FAILED]))
        elif self.controller.runtimeHostPcsData[hostPc["IP"]][testName]['testRepeatsSummary'][testState.PASSED] > 0:
            return parsedTestRepeatsSummary(testState.PASSED, " Passed: " + str(self.controller.runtimeHostPcsData[hostPc["IP"]][testName]['testRepeatsSummary'][testState.PASSED]))

    def loadHostPCSTestParams(self, hostPc):
        self.myHost = hostPc
        self.setTitle(self.groupName + " Tests,   For " + self.myHost['IP'])
        for test in self.tests:
            if test.testname in self.myHost['tests']:
                savedTestParmsPerHostPc = self.myHost['tests'][test.testname]
                self.testsRows[test.testname].checkBox.setChecked(savedTestParmsPerHostPc['checked'])
                self.testsRows[test.testname].repeatTestBox.setValue(savedTestParmsPerHostPc['repeatAmount'])
            else:
                self.testsRows[test.testname].checkBox.setChecked(False)
                self.testsRows[test.testname].repeatTestBox.setValue(0)

            if self.myHost["IP"] in self.controller.runtimeHostPcsData.keys() and test.testname in self.controller.runtimeHostPcsData[self.myHost["IP"]].keys():
                parsedTestRepeatsSummary = self.prepareTestRepeatsSummary(hostPc, test.testname)
                self.testsRows[test.testname].statusLbl.setText(parsedTestRepeatsSummary.resultsStr)
                self.testsRows[test.testname].statusLbl.setStyleSheet(COLOR_CONVERTER[parsedTestRepeatsSummary.stateForColor])
            else:
                self.testsRows[test.testname].statusLbl.setText("Not Started")
                self.testsRows[test.testname].statusLbl.setStyleSheet(COLOR_CONVERTER[testState.NOTSTARTED])

    def onCheckAllClicked(self):
        for testRow in self.testsRows.values():
            testRow.checkBox.setChecked(self.checkAllBox.isChecked())
        if self.myHost is not None:
            for test in self.tests:
                if test.testname in self.myHost['tests'].keys():
                    self.myHost['tests'][test.testname]['checked'] = self.checkAllBox.isChecked()
                else:
                    self.myHost['tests'][test.testname] = {"repeatAmount": 0, "checked": self.checkAllBox.isChecked()}

    def clearAll(self):
        self.setTitle(self.groupName + " tests")
        for testRow in self.testsRows.values():
            testRow.checkBox.setChecked(False)
            testRow.repeatTestBox.setValue(0)
