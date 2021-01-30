
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QScrollArea
from collections import namedtuple
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore

import sys

#TODO : another screen for editing and adding

#todo : present erorr when hostpc has a test in the defultconfig that does not have a an actural test in the test configs


class TestsGroupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,configs,groupName,tests,controller):
        super(TestsGroupBox, self).__init__(centralwidget)

        self.controller = controller
        self.configs = configs
        # self.setGeometry(QtCore.QRect(250, 150, 540, 280))
        self.setObjectName("hostExercisersGroupBox")
        self.vbox = QVBoxLayout()
        self.groupName = groupName
        self.tests = tests
        self.hostPc = configs.defaultConfContent['hostPCs'][0]

        self.testTableSetup()
        self.scrollSetup()
        self.checkAllSetup()

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
            checkBox.setGeometry(QtCore.QRect(0, 1, 200, 21))
            checkBox.setObjectName("testCheckBox_"+test.testname)
            checkBox.clicked.connect(self.onCheckBoxClicked)


            repeatTestBox = QtWidgets.QSpinBox(groupBox)
            repeatTestBox.setGeometry(QtCore.QRect(200, 0, 47, 23))
            repeatTestBox.setObjectName("repeatTestBox_"+test.testname)
            repeatTestBox.setRange(0,1000)
            repeatTestBox.valueChanged.connect(self.repeatTestBoxChanged)

            statusLbl = QtWidgets.QLabel(groupBox)
            statusLbl.setGeometry(QtCore.QRect(270, 3, 100, 14))
            statusLbl.setObjectName("TestState_"+test.testname)

            groupBox.setFixedHeight(25)
            groupBox.setFixedWidth(500)

            self.vbox.addWidget(groupBox)

            TestRowNamedtuple = namedtuple('TestRow', ['checkBox', 'repeatTestBox','statusLbl'])
            self.testsRows[test.testname] = TestRowNamedtuple(checkBox, repeatTestBox, statusLbl)

    def repeatTestBoxChanged(self):
        repeatTestBox = self.sender()
        testName = repeatTestBox.objectName().split('_')[1]
        if testName in self.hostPc['tests'].keys():
            self.hostPc['tests'][testName]['repeatAmount'] = repeatTestBox.value()
        else:
            self.hostPc['tests'][testName] = {"repeatAmount" : repeatTestBox.value(),"checked" : False}


    def onCheckBoxClicked(self):
        clickedCheckBox = self.sender()
        testName = clickedCheckBox.objectName().split('_')[1]
        if testName in self.hostPc['tests'].keys():
            self.hostPc['tests'][testName]['checked'] = clickedCheckBox.isChecked()
        else:
            self.hostPc['tests'][testName] = {"repeatAmount" : 0,"checked" : clickedCheckBox.isChecked()}


    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)  # Scroll Area which contains the widgets, set as the centralWidget
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 30, 540, 250))


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setToolTip(_translate("skippedTestsNumber", "tests list"))
        self.setTitle(_translate("skippedTestsNumber", self.groupName + " tests"))
        self.checkAllBox.setText("check all")
        for test in self.tests:
            self.testsRows[test.testname].checkBox.setText(_translate("skippedTestsNumber", test.testname))
            self.testsRows[test.testname].statusLbl.setText(_translate("skippedTestsNumber", "Not Started"))

    def updateTestStatusLbl(self,testName,testStatus):
        _translate = QtCore.QCoreApplication.translate
        self.testsRows[testName].statusLbl.setText(_translate("skippedTestsNumber", testStatus))

    def setHostPCSavedTestParams(self,hostPc):
        self.hostPc = hostPc
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("skippedTestsNumber", self.groupName + " tests,   for "+self.hostPc['IP']))
        for test in self.tests:
            if test.testname in self.hostPc['tests']:
                savedTestParmsPerHostPc = self.hostPc['tests'][test.testname]
                self.testsRows[test.testname].checkBox.setChecked(savedTestParmsPerHostPc['checked'])
                self.testsRows[test.testname].repeatTestBox.setValue(savedTestParmsPerHostPc['repeatAmount'])
            else:
                self.testsRows[test.testname].checkBox.setChecked(False)
                self.testsRows[test.testname].repeatTestBox.setValue(0)


            if self.hostPc["IP"] in self.controller.runtimeHostPcsData.keys() \
                    and test.testname in self.controller.runtimeHostPcsData[self.hostPc["IP"]].keys():
                self.testsRows[test.testname].statusLbl.setText(self.controller.runtimeHostPcsData[self.hostPc["IP"]][test.testname])
            else:
                self.testsRows[test.testname].statusLbl.setText("Not Started")

    def onCheckAllClicked(self):
        for testRow in self.testsRows.values():
            testRow.checkBox.setChecked(self.checkAllBox.isChecked())
        for test in self.hostPc["tests"].values():
            test["checked"] = self.checkAllBox.isChecked()
