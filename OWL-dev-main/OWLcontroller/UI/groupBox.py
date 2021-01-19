
from collections import namedtuple
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore


#TODO : make single select
class groupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,configs):
        super(groupBox, self).__init__( centralwidget)

        # self.selectGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.setGeometry(QtCore.QRect(10, 350, 131, 131))
        self.setObjectName("selectGroupBox")

        self.vbox = QVBoxLayout()

        self.groupNames = configs.legacyMode.legacyFlowOperationsTestsByGroups.keys()

        self.groupListSetup()
        self.scrollSetup()

    def groupListSetup(self):
        self.groupCheckBoxArr = {}
        for groupName in self.groupNames:
            self.groupCheckBoxArr[groupName] = QtWidgets.QCheckBox(self)
            self.groupCheckBoxArr[groupName].setGeometry(QtCore.QRect(0, 0, 64, 18))
            self.groupCheckBoxArr[groupName].setObjectName("groupCheckBox_"+groupName)
            self.vbox.addWidget(self.groupCheckBoxArr[groupName])

    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)  # Scroll Area which contains the widgets, set as the centralWidget
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 20, 131, 110))

    def retranslateUi(self, skippedTestsNumber,_translate):
        self.setToolTip(_translate("skippedTestsNumber", "Hosts list"))
        self.setTitle(_translate("skippedTestsNumber", "Select Group"))
        for groupName in self.groupNames:
            self.groupCheckBoxArr[groupName].setText(_translate("skippedTestsNumber",groupName))

