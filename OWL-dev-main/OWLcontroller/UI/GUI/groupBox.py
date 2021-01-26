
from collections import namedtuple
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore


#TODO : make single select
class groupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,configs,mainWindowRef):
        super(groupBox, self).__init__( centralwidget)

        self.mainWindowRef = mainWindowRef
        self.setGeometry(QtCore.QRect(10, 440, 220, 180))
        self.setObjectName("selectGroupBox")

        self.vbox = QVBoxLayout()

        self.groupNames = configs.legacyMode.legacyFlowOperationsTestsByGroups.keys()

        self.groupListSetup()
        self.scrollSetup()

    def groupListSetup(self):
        self.groupCheckBoxArr = {}
        first=True
        for groupName in self.groupNames:
            self.groupCheckBoxArr[groupName] = QtWidgets.QCheckBox(self)
            self.groupCheckBoxArr[groupName].setGeometry(QtCore.QRect(0, 0, 64, 18))
            self.groupCheckBoxArr[groupName].setObjectName("groupCheckBox_"+groupName)
            self.groupCheckBoxArr[groupName].clicked.connect(self.onChacked)
            self.vbox.addWidget(self.groupCheckBoxArr[groupName])

            if first: # set first option to be the default
                first=False
                self.groupCheckBoxArr[groupName].setChecked(True)
                self.mainWindowRef.setDisplayedTestGroup(groupName)


    def onChacked(self):
        clickedCheckBox = self.sender()
        if clickedCheckBox.isChecked():
            if self.displaySwitchGroupWarningPopUp():
                for checkBox in self.groupCheckBoxArr.values():
                    if checkBox is not clickedCheckBox and checkBox.isChecked():
                        checkBox.setChecked(False)


                groupName = clickedCheckBox.objectName().split('_')[1]
                self.mainWindowRef.setDisplayedTestGroup(groupName)
            else:
                clickedCheckBox.setChecked(False)
        else:
            clickedCheckBox.setChecked(True)

    def displaySwitchGroupWarningPopUp(self):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("are you sure you want to switch group?\n "
                       "switching well delete all tests configured for current host Pc")
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msgBox.exec() == QMessageBox.Ok

    def cahngeSelected(self,groupName):
        for checkBox in self.groupCheckBoxArr.values():
            if checkBox.objectName().split('_')[1] == groupName:
                checkBox.setChecked(True)
            else:
                checkBox.setChecked(False)


    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 20, 220, 160))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setToolTip(_translate("skippedTestsNumber", "Hosts list"))
        self.setTitle(_translate("skippedTestsNumber", "Select Group"))
        for groupName in self.groupNames:
            self.groupCheckBoxArr[groupName].setText(_translate("skippedTestsNumber",groupName))

