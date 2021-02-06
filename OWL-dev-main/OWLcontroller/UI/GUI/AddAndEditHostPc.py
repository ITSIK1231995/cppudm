from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QCheckBox,QRadioButton)

import sys
from collections import namedtuple
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
            self.setWindowTitle("Edit HostPC")
            self.fillWithData()
        else:
            self.setWindowTitle("Add HostPC")


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("host Pc Settings")
        layout = QFormLayout()
        IPBox = QLineEdit()
        if self.editMode:
            IPBox.setReadOnly(True)
        layout.addRow(QLabel("IP:"),IPBox)
        COMBox = QLineEdit()
        layout.addRow(QLabel("Clicker COM:"),COMBox)
        chanelBox = QSpinBox()
        layout.addRow(QLabel("Clicker chanel:"),chanelBox)
        stopOnFailure = QCheckBox()
        layout.addRow(QLabel("stop on failure:"), stopOnFailure)
        postPingWaitTimeBox = QSpinBox()
        layout.addRow(QLabel("post ping waiting time:"), postPingWaitTimeBox)
        self.formGroupBox.setLayout(layout)


        formObjectsNamedTuple = namedtuple('formObjects', ['IPBox', 'COMBox','chanelBox','stopOnFailure','postPingWaitTimeBox'])
        self.formObjects = formObjectsNamedTuple(IPBox, COMBox,chanelBox,stopOnFailure,postPingWaitTimeBox)


    def fillWithData(self):

        self.formObjects.IPBox.setText(self.hostPc["IP"])
        if  "clicker" in self.hostPc.keys():
            if "COM" in self.hostPc["clicker"]:
                self.formObjects.COMBox.setText(self.hostPc["clicker"]["COM"])
            if "chanel" in self.hostPc["clicker"]:
                self.formObjects.chanelBox.setValue(int(self.hostPc["clicker"]["chanel"]))

        if "postPingWaitingTime" in self.hostPc.keys():
            self.formObjects.postPingWaitTimeBox.setValue(int(self.hostPc["postPingWaitingTime"]))

        self.formObjects.stopOnFailure.setChecked(self.hostPc["stopOnFailure"])

    def validIP(self,IP):
        try:
            parts = IP.split('.')
            return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
        except ValueError:
            return False  # one of the 'parts' not convertible to integer
        except (AttributeError, TypeError):
            return False  # `ip` isn't even a string

    def IpExsists(self,IP):
        allHostPcs = self.mainWindowRef.controller.configs.defaultConfContent["hostPCs"]
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

        self.close()

    def acceptAddMode(self):
        newHostPCIP = self.formObjects.IPBox.text()
        if not self.validIP(newHostPCIP):
            GUIUtills.PopUpWarning("IP is not writen correctly")
        elif  self.IpExsists(newHostPCIP):
            GUIUtills.PopUpWarning("IP already exists")
        else:
            newHostPc = {
                "IP": newHostPCIP,
                "stopOnFailure": self.formObjects.stopOnFailure.isChecked(),
                "checked" : False,
                "groupName": list(self.mainWindowRef.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups.keys())[0], # defult is the first group
                "tests" : {},
                "postPingWaitingTime" : self.formObjects.postPingWaitTimeBox.value()
            }
            if self.formObjects.COMBox.text() != "":
                newHostPc["clicker"] = {
                    "COM" : self.formObjects.COMBox.text(),
                    "chanel" : self.formObjects.stopOnFailure.isChecked()
                }
            self.mainWindowRef.controller.configs.defaultConfContent["hostPCs"].append(newHostPc)
            self.mainWindowRef.hostExercisersGroupBox.addHostPcRow(newHostPc)
            self.mainWindowRef.hostExercisersGroupBox.retranslateUi()
            self.close()

    def accept(self):
        if self.editMode:
            self.acceptEditMode()
        else:
            self.acceptAddMode()





