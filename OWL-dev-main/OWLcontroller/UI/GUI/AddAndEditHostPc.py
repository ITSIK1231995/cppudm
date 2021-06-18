from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QCheckBox,QRadioButton)
from collections import namedtuple

from UI.GUI import systemModes
from UI.GUI.GUIUtills import *

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
            self.setWindowTitle("Edit System Under Test")
            self.fillWithData()
        else:
            self.setWindowTitle("Add System Under Test")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("System Under Test Settings")
        layout = QFormLayout()
        IPBox = QLineEdit()
        if self.editMode:
            IPBox.setReadOnly(True)
        layout.addRow(QLabel("IP \ DNS:"),IPBox)
        aliasBox = QLineEdit()
        layout.addRow(QLabel("Alias:"), aliasBox)
        if self.mainWindowRef.controller.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC:
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
            formObjectsNamedTuple = namedtuple('formObjects', ['IPBox','aliasBox', 'COMBox','chanelBox','stopOnFailure','postPingWaitTimeBox'])
            self.formObjects = formObjectsNamedTuple(IPBox,aliasBox,COMBox,chanelBox,stopOnFailure,postPingWaitTimeBox)
        else:  # Current execution mode is Excercier mode
            formObjectsNamedTuple = namedtuple('formObjects',['IPBox', 'aliasBox', 'stopOnFailure','postPingWaitTimeBox'])
            self.formObjects = formObjectsNamedTuple(IPBox, aliasBox, stopOnFailure,postPingWaitTimeBox)

    def fillWithData(self):
        self.formObjects.IPBox.setText(self.hostPc["IP"])
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
        allHostPcs = self.getHostsDictForCurrentSystemMode()
        for hostPC in allHostPcs:
            if hostPC["IP"] == IP:
                return True
        return False

    def acceptEditMode(self):
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            if "clicker" in self.hostPc.keys():
                self.hostPc["clicker"]["COM"] = self.formObjects.COMBox.text()
                self.hostPc["clicker"]["chanel"] = int(self.formObjects.chanelBox.text())
            else:
                self.hostPc["clicker"] = {
                    "COM": self.formObjects.COMBox.text(),
                    "chanel": self.formObjects.stopOnFailure.isChecked()
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

    def getTestsByGroupDictForCurrentSystemMode(self):
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            return self.mainWindowRef.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups
        else:
            return self.mainWindowRef.controller.configs.legacyMode.legacyTestsByGroup

    def getHostsDictForCurrentSystemMode(self):
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            return self.mainWindowRef.controller.configs.defaultConfContent["hostPCs"]
        else:
            return self.mainWindowRef.controller.configs.defaultConfContent["Exercisers"]

    def acceptAddMode(self):
        newHostIP = self.formObjects.IPBox.text()
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
                "groupName": list(self.getTestsByGroupDictForCurrentSystemMode().keys())[0], # default is the first group
                "tests" : {},
                "postPingWaitingTime" : self.formObjects.postPingWaitTimeBox.value()
            }
            if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
                if self.formObjects.COMBox.text() != "":
                    host["clicker"] = {
                        "COM" : self.formObjects.COMBox.text(),
                        "chanel" : self.formObjects.stopOnFailure.isChecked()
                    }
            self.getHostsDictForCurrentSystemMode().append(host)
            self.mainWindowRef.hostExercisersGroupBox.addHostPcRow(host)
            self.mainWindowRef.hostExercisersGroupBox.retranslateUi()
            self.close()

    def accept(self):
        if self.editMode:
            self.acceptEditMode()
        else:
            self.acceptAddMode()





