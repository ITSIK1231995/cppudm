
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QScrollArea
from collections import namedtuple

#TODO : add scrollBar
#TODO : edit button per row
#TODO : another screen for editing and adding

class exerHostGroupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,configs):
        super(exerHostGroupBox, self).__init__( centralwidget)

        # self.selectGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.setGeometry(QtCore.QRect(20, 150, 200, 180))
        self.setObjectName("hostExercisersGroupBox")
        self.hotPcs = configs.defaultConfContent['hostPCs']
        posX = 1
        self.hostPcRows = {}
        for hostPc in self.hotPcs:

            checkBox = QtWidgets.QCheckBox(self)
            checkBox.setGeometry(QtCore.QRect(0, 25*posX+5, 100, 21))
            checkBox.setObjectName("groupCheckBox_"+hostPc['IP'])

            onOffLbl = QtWidgets.QLabel(self)
            onOffLbl.setGeometry(QtCore.QRect(100, 25*posX+8, 47, 14))
            onOffLbl.setObjectName("hostPcState_"+hostPc['IP'])

            showButton = QtWidgets.QPushButton(self)
            showButton.setGeometry(QtCore.QRect(120, 25*posX+5, 35, 20))
            showButton.setObjectName("show_"+hostPc['IP'])
            showButton.clicked.connect(self.showBtnClicked)

            editButton = QtWidgets.QPushButton(self)
            editButton.setGeometry(QtCore.QRect(155, 25*posX+5, 30, 20))
            editButton.setObjectName("edit_"+hostPc['IP'])
            editButton.clicked.connect(self.editBtnClicked)

            hostPcRowNamedtuple = namedtuple('hostPcRow', ['checkBox', 'onOffLbl','showButton','editButton'])
            self.hostPcRows[hostPc['IP']] = hostPcRowNamedtuple(checkBox,onOffLbl,showButton,editButton)
            posX+=1

        self.addHostPc = QtWidgets.QPushButton(self)
        self.addHostPc.setGeometry(QtCore.QRect(165, 5, 35, 23))
        self.addHostPc.setObjectName("addHostPc")



    def getIPFromBtnName(self,btn):
        return btn.objectName().split('_')[1]

    def editBtnClicked(self,btn):
        hostPcIp = self.getIPFromBtnName(self.sender())
        print(hostPcIp)

    def showBtnClicked(self, btn):
        hostPcIp = self.getIPFromBtnName(self.sender())
        print(hostPcIp)



    def retranslateUi(self, skippedTestsNumber,_translate):
        self.setToolTip(_translate("skippedTestsNumber", "Hosts list"))
        self.setTitle(_translate("skippedTestsNumber", "Exerciser / Host"))
        for hostPc in self.hotPcs:
            self.hostPcRows[hostPc['IP']].checkBox.setText(_translate("skippedTestsNumber", hostPc['IP']))
            self.hostPcRows[hostPc['IP']].checkBox.setChecked(hostPc['checked'])
            self.hostPcRows[hostPc['IP']].onOffLbl.setText(_translate("skippedTestsNumber", "ON"))
            self.hostPcRows[hostPc['IP']].editButton.setText(_translate("skippedTestsNumber", "edit"))
            self.hostPcRows[hostPc['IP']].showButton.setText(_translate("skippedTestsNumber", "show"))


        self.addHostPc.setText(_translate("skippedTestsNumber", "+"))


