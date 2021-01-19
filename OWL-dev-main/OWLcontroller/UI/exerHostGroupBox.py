
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QScrollArea
from collections import namedtuple
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore

import sys

#TODO : another screen for editing and adding

class exerHostGroupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,configs):
        super(exerHostGroupBox, self).__init__( centralwidget)

        self.setGeometry(QtCore.QRect(20, 150, 220, 180))
        self.setObjectName("hostExercisersGroupBox")
        self.vbox = QVBoxLayout()

        self.hotPcs = configs.defaultConfContent['hostPCs']

        self.hostPCTableSetup()
        self.scrollSetup()
        self.addHostBtnSetup()


    def addHostBtnSetup(self):
        self.addHostPc = QtWidgets.QPushButton(self)
        self.addHostPc.setGeometry(QtCore.QRect(145, 5, 75, 23))
        self.addHostPc.setObjectName("addHostPc")
        self.addHostPc.clicked.connect(self.addHostPcBtnClicked)

    def hostPCTableSetup(self):

        self.hostPcRows = {}
        for hostPc in self.hotPcs:

            groupBox = QtWidgets.QGroupBox()
            # groupBox.setGeometry(QtCore.QRect(50, 50, 50, 50))
            groupBox.setObjectName("GroupBox_"+hostPc['IP'])

            checkBox = QtWidgets.QCheckBox(groupBox)
            checkBox.setGeometry(QtCore.QRect(0, 0, 100, 21))
            checkBox.setObjectName("groupCheckBox_"+hostPc['IP'])

            onOffLbl = QtWidgets.QLabel(groupBox)
            onOffLbl.setGeometry(QtCore.QRect(100, 3, 47, 14))
            onOffLbl.setObjectName("hostPcState_"+hostPc['IP'])

            showButton = QtWidgets.QPushButton(groupBox)
            showButton.setGeometry(QtCore.QRect(120, 0, 35, 20))
            showButton.setObjectName("show_"+hostPc['IP'])
            showButton.clicked.connect(self.showBtnClicked)

            editButton = QtWidgets.QPushButton(groupBox)
            editButton.setGeometry(QtCore.QRect(155, 0, 30, 20))
            editButton.setObjectName("edit_"+hostPc['IP'])
            editButton.clicked.connect(self.editBtnClicked)

            groupBox.setFixedHeight(20)
            groupBox.setFixedWidth(185)

            self.vbox.addWidget(groupBox)

            hostPcRowNamedtuple = namedtuple('hostPcRow', ['checkBox', 'onOffLbl','showButton','editButton'])
            self.hostPcRows[hostPc['IP']] = hostPcRowNamedtuple(checkBox,onOffLbl,showButton,editButton)

    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)  # Scroll Area which contains the widgets, set as the centralWidget
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 30, 220, 150))

    def getIPFromBtnName(self,btn):
        return btn.objectName().split('_')[1]

    def editBtnClicked(self):
        hostPcIp = self.getIPFromBtnName(self.sender())
        print(hostPcIp)

    def showBtnClicked(self):
        hostPcIp = self.getIPFromBtnName(self.sender())
        print(hostPcIp)

    def addHostPcBtnClicked(self):
        print("addHostPcBtnClicked")



    def retranslateUi(self, skippedTestsNumber,_translate):
        self.setToolTip(_translate("skippedTestsNumber", "Hosts list"))
        self.setTitle(_translate("skippedTestsNumber", "Exerciser / Host"))
        for hostPc in self.hotPcs:#TODO: is this needed?
            self.hostPcRows[hostPc['IP']].checkBox.setText(_translate("skippedTestsNumber", hostPc['IP']))
            self.hostPcRows[hostPc['IP']].checkBox.setChecked(hostPc['checked'])
            self.hostPcRows[hostPc['IP']].onOffLbl.setText(_translate("skippedTestsNumber", "ON"))
            self.hostPcRows[hostPc['IP']].editButton.setText(_translate("skippedTestsNumber", "edit"))
            self.hostPcRows[hostPc['IP']].showButton.setText(_translate("skippedTestsNumber", "show"))


        self.addHostPc.setText(_translate("skippedTestsNumber", "Add host pc"))


