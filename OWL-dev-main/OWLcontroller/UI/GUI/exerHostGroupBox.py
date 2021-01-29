
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QScrollArea
from collections import namedtuple
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore
from UI.GUI.AddAndEditHostPc import *

import sys

#TODO : another screen for editing and adding

class exerHostGroupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,configs,mainWindowRef):
        super(exerHostGroupBox, self).__init__( centralwidget)

        self.mainWindowRef = mainWindowRef
        self.setGeometry(QtCore.QRect(10, 150, 220, 280))
        self.setObjectName("hostExercisersGroupBox")
        self.vbox = QVBoxLayout()

        self.hostPcs = configs.defaultConfContent['hostPCs']

        self.hostPCTableSetup()
        self.scrollSetup()
        self.addHostBtnSetup()


    def addHostBtnSetup(self):
        self.addHostPcBtn = QtWidgets.QPushButton(self)
        self.addHostPcBtn.setGeometry(QtCore.QRect(145, 5, 75, 23))
        self.addHostPcBtn.setObjectName("addHostPc")
        self.addHostPcBtn.clicked.connect(self.addHostPcBtnClicked)

    def hostPCTableSetup(self):

        self.hostPcRows = {}
        for hostPc in self.hostPcs:
            self.addHostPcRow(hostPc)

    def addHostPcRow(self,hostPc):
        groupBox = QtWidgets.QGroupBox()
        groupBox.setObjectName("GroupBox_" + hostPc['IP'])

        checkBox = QtWidgets.QCheckBox(groupBox)
        checkBox.setGeometry(QtCore.QRect(0, 0, 100, 21))
        checkBox.setObjectName("groupCheckBox_" + hostPc['IP'])
        checkBox.clicked.connect(self.onCheckBoxClicked)

        showButton = QtWidgets.QPushButton(groupBox)
        showButton.setGeometry(QtCore.QRect(120, 0, 35, 20))
        showButton.setObjectName("show_" + hostPc['IP'])
        showButton.clicked.connect(self.showBtnClicked)

        editButton = QtWidgets.QPushButton(groupBox)
        editButton.setGeometry(QtCore.QRect(155, 0, 30, 20))
        editButton.setObjectName("edit_" + hostPc['IP'])
        editButton.clicked.connect(self.editBtnClicked)

        groupBox.setFixedHeight(20)
        groupBox.setFixedWidth(185)

        self.vbox.addWidget(groupBox)

        hostPcRowNamedtuple = namedtuple('hostPcRow', ['checkBox',  'showButton', 'editButton'])
        self.hostPcRows[hostPc['IP']] = hostPcRowNamedtuple(checkBox,  showButton, editButton)


    def onCheckBoxClicked(self):
        clickedCheckBox = self.sender()
        hostPc = self.getHostPCFromBtnName(clickedCheckBox)
        hostPc['checked'] = clickedCheckBox.isChecked()

    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)  # Scroll Area which contains the widgets, set as the centralWidget
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 30, 220, 250))

    def getHostPCFromBtnName(self, btn):
        hostPcIp =  btn.objectName().split('_')[1]
        return next((hostPc for hostPc in self.hostPcs if hostPc['IP'] == hostPcIp), None)

    def editBtnClicked(self):
        hostPc = self.getHostPCFromBtnName(self.sender())
        AddAndEditHostPc(True,hostPc,self.mainWindowRef).exec()

    def showBtnClicked(self):
        hostPc = self.getHostPCFromBtnName(self.sender())
        self.mainWindowRef.setNewHostPC(hostPc)

    def addHostPcBtnClicked(self):
        AddAndEditHostPc(False,None,self.mainWindowRef).exec()




    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setToolTip(_translate("skippedTestsNumber", "Hosts list"))
        self.setTitle(_translate("skippedTestsNumber", "Exerciser / Host"))
        for hostPc in self.hostPcs:
            self.hostPcRows[hostPc['IP']].checkBox.setText(_translate("skippedTestsNumber", hostPc['IP']))
            self.hostPcRows[hostPc['IP']].checkBox.setChecked(hostPc['checked'])
            self.hostPcRows[hostPc['IP']].editButton.setText(_translate("skippedTestsNumber", "edit"))
            self.hostPcRows[hostPc['IP']].showButton.setText(_translate("skippedTestsNumber", "show"))


        self.addHostPcBtn.setText(_translate("skippedTestsNumber", "Add host pc"))


