from PyQt5.QtWidgets import (QDialog,
                             QDialogButtonBox, QFormLayout, QGroupBox, QSpinBox, QCheckBox)
from collections import namedtuple

import systemModes
from UI.GUI.GUIUtills import *
from Utils import getHostsDictFromDefaultConfigurationForCurrentExecutionMode, getTestsByGroupDictForCurrentSystemExecutionMode


class AddAndEditHostPc(QDialog):
    def __init__(self,editMode,hostPc,mainWindowRef):
        super(AddAndEditHostPc, self).__init__()
        self.mainWindowRef = mainWindowRef
        self.hostPc = hostPc
        self.editMode = editMode
        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        if editMode:
            self.setWindowTitle("Edit Host")
            self.fillWithData()
        else:
            self.setWindowTitle("Add Host")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Host Settings")
        layout = QFormLayout()
        hostIdentifierBox = QLineEdit()
        if self.editMode:
            hostIdentifierBox.setReadOnly(True)
        layout.addRow(QLabel("IP \ DNS:"),hostIdentifierBox) if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode() else  layout.addRow(QLabel("Exerciser Serial Number"),hostIdentifierBox)
        aliasBox = QLineEdit()
        layout.addRow(QLabel("Alias:"), aliasBox)
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            COMBox = QLineEdit()
            layout.addRow(QLabel("Clicker COM:"),COMBox)
            chanelBox = QSpinBox()
            layout.addRow(QLabel("Clicker Chanel:"),chanelBox)
        stopOnFailure = QCheckBox()
        layout.addRow(QLabel("Stop On Failure:"), stopOnFailure)
        postPingWaitTimeBox = QSpinBox()
        postPingWait = QLabel("Post Ping Waiting Time:")
        postPingWait.setToolTip("In some hosts ping stops before the PC is off, this is the amount of time the controll PC will wait before sending the clicker command")
        postPingWaitTimeBox.setMaximum(1000000)
        postPingWaitTimeBox.setMinimum(0)
        layout.addRow(postPingWait, postPingWaitTimeBox)
        self.formGroupBox.setLayout(layout)
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            formObjectsNamedTuple = namedtuple('formObjects', ['hostIdentifierBox','aliasBox', 'COMBox','chanelBox','stopOnFailure','postPingWaitTimeBox'])
            self.formObjects = formObjectsNamedTuple(hostIdentifierBox,aliasBox,COMBox,chanelBox,stopOnFailure,postPingWaitTimeBox)
        else:  # Current execution mode is Excercier mode
            formObjectsNamedTuple = namedtuple('formObjects',['hostIdentifierBox', 'aliasBox', 'stopOnFailure','postPingWaitTimeBox'])
            self.formObjects = formObjectsNamedTuple(hostIdentifierBox, aliasBox, stopOnFailure,postPingWaitTimeBox)

    def fillWithData(self):
        self.formObjects.hostIdentifierBox.setText(self.hostPc["IP"])
        self.formObjects.aliasBox.setText(self.hostPc["alias"])
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            if  "clicker" in self.hostPc.keys():
                if "COM" in self.hostPc["clicker"]:
                    self.formObjects.COMBox.setText(self.hostPc["clicker"]["COM"])
                if "chanel" in self.hostPc["clicker"]:
                    self.formObjects.chanelBox.setValue(int(self.hostPc["clicker"]["chanel"]))
        if "postPingWaitingTime" in self.hostPc.keys():
            self.formObjects.postPingWaitTimeBox.setValue(int(self.hostPc["postPingWaitingTime"]))
        self.formObjects.stopOnFailure.setChecked(self.hostPc["stopOnFailure"])

    def validIP(self,IP):
        return not str(IP) == ""

    def IpExsists(self,IP):
        allHost = getHostsDictFromDefaultConfigurationForCurrentExecutionMode(self.mainWindowRef.controller)
        for host in allHost:
            if host["IP"] == IP:
                return True
        return False

    def acceptEditMode(self):
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            if self.formObjects.COMBox.text() != "":
                if "clicker" in self.hostPc.keys():
                    self.hostPc["clicker"]["COM"] = self.formObjects.COMBox.text()
                    self.hostPc["clicker"]["chanel"] = int(self.formObjects.chanelBox.text())
                else:
                    self.hostPc["clicker"] = {
                        "COM": self.formObjects.COMBox.text(),
                        #"chanel": self.formObjects.stopOnFailure.isChecked() #TODO need to understand why i wrote it in this way
                        "chanel": self.formObjects.chanelBox.text()
                    }
        self.hostPc["stopOnFailure"] = self.formObjects.stopOnFailure.isChecked()
        self.hostPc["postPingWaitingTime"] = self.formObjects.postPingWaitTimeBox.value()
        self.hostPc["alias"] = self.formObjects.aliasBox.text()
        if self.formObjects.aliasBox.text() != "" and\
                self.formObjects.aliasBox.text() != None:
            self.mainWindowRef.hostExercisersGroupBox.editSpecificHostPcCheckBoxLabel(self.hostPc["IP"], self.formObjects.aliasBox.text())
        else:
            self.mainWindowRef.hostExercisersGroupBox.editSpecificHostPcCheckBoxLabel(self.hostPc["IP"],self.hostPc["IP"])
        self.close()

    def acceptAddMode(self):
        newHostIP = self.formObjects.hostIdentifierBox.text()
        if not self.validIP(newHostIP):
            GUIUtills.PopUpWarning("IP is not writen correctly")
        elif  self.IpExsists(newHostIP):
            GUIUtills.PopUpWarning("IP / DNS is already exists")
        else:
            host = {
                "IP": newHostIP,
                "alias" : self.formObjects.aliasBox.text(),
                "stopOnFailure": self.formObjects.stopOnFailure.isChecked(),
                "checked" : False,
                "groupName": list(getTestsByGroupDictForCurrentSystemExecutionMode(self.mainWindowRef.controller).keys())[0], # default is the first group
                "tests" : {},
                "postPingWaitingTime" : self.formObjects.postPingWaitTimeBox.value()
            }
            if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
                if self.formObjects.COMBox.text() != "":
                    host["clicker"] = {
                        "COM" : self.formObjects.COMBox.text(),
                        # "chanel" : self.formObjects.stopOnFailure.isChecked()#TODO need to understand why i wrote it in this way
                        "chanel": self.formObjects.chanelBox.text()
                    }
            getHostsDictFromDefaultConfigurationForCurrentExecutionMode(self.mainWindowRef.controller).append(host)
            self.mainWindowRef.hostExercisersGroupBox.addHostRow(host)
            self.mainWindowRef.hostExercisersGroupBox.retranslateUi()
            self.close()

    def accept(self):
        if self.editMode:
            self.acceptEditMode()
        else:
            self.acceptAddMode()





