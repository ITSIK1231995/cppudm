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
        formObjectsNamedTuple = namedtuple('formObjects', ['IPBox','aliasBox', 'COMBox','chanelBox','stopOnFailure','postPingWaitTimeBox'])
        self.formObjects = formObjectsNamedTuple(IPBox,aliasBox,COMBox,chanelBox,stopOnFailure,postPingWaitTimeBox)

    def fillWithData(self):
        self.formObjects.IPBox.setText(self.hostPc["IP"])
        self.formObjects.aliasBox.setText(self.hostPc["alias"])
        if  "clicker" in self.hostPc.keys():
            if "COM" in self.hostPc["clicker"]:
                self.formObjects.COMBox.setText(self.hostPc["clicker"]["COM"])
            if "chanel" in self.hostPc["clicker"]:
                self.formObjects.chanelBox.setValue(int(self.hostPc["clicker"]["chanel"]))
        if "postPingWaitingTime" in self.hostPc.keys():
            self.formObjects.postPingWaitTimeBox.setValue(int(self.hostPc["postPingWaitingTime"]))
        self.formObjects.stopOnFailure.setChecked(self.hostPc["stopOnFailure"])
    #  #TODO  look at this
    # def validIP(self,IP):
    #     try:
    #         parts = IP.split('.')
    #         return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    #     except ValueError:
    #         return False  # one of the 'parts' not convertible to integer
    #     except (AttributeError, TypeError):
    #         return False  # `ip` isn't even a string

    def validIP(self,IP):
        return not str(IP) == ""

    def IpExsists(self,IP):
        allHostPcs = self.getHostsDictForCurrentSystemMode()
        for hostPC in allHostPcs:
            if hostPC["IP"] == IP:
                return True
        return False

    def acceptEditMode(self):
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
        # TODO  look at this
        if self.formObjects.aliasBox.text() != "" and\
                self.formObjects.aliasBox.text() != None:
            self.mainWindowRef.hostExercisersGroupBox.editSpecificHostPcCheckBoxLabel(self.hostPc["IP"], self.formObjects.aliasBox.text())
        else:
            self.mainWindowRef.hostExercisersGroupBox.editSpecificHostPcCheckBoxLabel(self.hostPc["IP"],self.hostPc["IP"])
        self.close()

    def getTestsByGroupDictForCurrentSystemMode(self): #TODO Go over this
        if self.mainWindowRef.controller.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC:
            return self.mainWindowRef.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups
        else:
            return self.mainWindowRef.controller.configs.legacyMode.legacyTestsByGroup

    def getHostsDictForCurrentSystemMode(self):#TODO Go over this
        if self.mainWindowRef.controller.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC:
            return self.mainWindowRef.controller.configs.defaultConfContent["hostPCs"]
        else:
            return self.mainWindowRef.controller.configs.defaultConfContent["Exercisers"]

    def acceptAddMode(self):
        newHostPCIP = self.formObjects.IPBox.text()
        if not self.validIP(newHostPCIP):
            GUIUtills.PopUpWarning("IP is not writen correctly")
        elif  self.IpExsists(newHostPCIP):
            GUIUtills.PopUpWarning("IP / DNS is already exists")
        else:
            newHostPc = {
                "IP": newHostPCIP,
                "alias" : self.formObjects.aliasBox.text(),
                "stopOnFailure": self.formObjects.stopOnFailure.isChecked(),
                "checked" : False,
                "groupName": list(self.getTestsByGroupDictForCurrentSystemMode().keys())[0], # default is the first group #TODO Go over this
                "tests" : {},
                "postPingWaitingTime" : self.formObjects.postPingWaitTimeBox.value()
            }
            if self.formObjects.COMBox.text() != "":
                newHostPc["clicker"] = {
                    "COM" : self.formObjects.COMBox.text(),
                    "chanel" : self.formObjects.stopOnFailure.isChecked()
                }
            self.getHostsDictForCurrentSystemMode().append(newHostPc) #TODO Go over this
            self.mainWindowRef.hostExercisersGroupBox.addHostPcRow(newHostPc)
            self.mainWindowRef.hostExercisersGroupBox.retranslateUi()
            self.close()

    def accept(self):
        if self.editMode:
            self.acceptEditMode()
        else:
            self.acceptAddMode()





