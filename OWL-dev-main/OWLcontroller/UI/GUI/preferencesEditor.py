from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout)

import sys
from collections import namedtuple
from UI.GUI.GUIUtills import *

from PyQt5 import QtWidgets, uic, QtCore

class PreferencesEditor(QDialog):


    def __init__(self,mainWindowRef):
        super(PreferencesEditor, self).__init__()
        self.mainWindowRef = mainWindowRef


        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)


        self.setWindowTitle("Preferences")
        self.fillWithData()

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Preferences")
        layout = QFormLayout()
        portBox = QSpinBox()
        portBox.setMaximum(65535)
        portBox.setMinimum(1025)

        layout.addRow(QLabel("host pc port:"), portBox)
        conectionAttempsBox = QSpinBox()
        conectionAttempsBox.setMinimum(4)
        layout.addRow(QLabel("conection attemps:"), conectionAttempsBox)
        defaultExecutionModeBox =  QComboBox()
        layout.addRow(QLabel("default execution mode:"), defaultExecutionModeBox)
        resultPathBox = QLineEdit()
        layout.addRow(QLabel("result path:"),resultPathBox)
        legacyModePathBox = QLineEdit()
        layout.addRow(QLabel("legacy mode path:"), legacyModePathBox)
        errinjModePathBox = QLineEdit()
        layout.addRow(QLabel("errinj mode path:"), errinjModePathBox)
        analyzerMinVersionBox = QLineEdit()
        layout.addRow(QLabel("analyzer min version:"), analyzerMinVersionBox)
        self.formGroupBox.setLayout(layout)
        formObjectsNamedTuple = namedtuple('formObjects', ['portBox', 'conectionAttempsBox','defaultExecutionModeBox','resultPathBox','legacyModePathBox','errinjModePathBox','analyzerMinVersionBox'])
        self.formObjects = formObjectsNamedTuple(portBox, conectionAttempsBox,defaultExecutionModeBox,resultPathBox,legacyModePathBox,errinjModePathBox,analyzerMinVersionBox)


    def fillWithData(self):
        defaultConf = self.mainWindowRef.controller.configs.defaultConfContent
        self.formObjects.portBox.setValue(defaultConf["hostPcServerPort"])
        self.formObjects.conectionAttempsBox.setValue(defaultConf["attempsToCreateSocket"])
        self.formObjects.defaultExecutionModeBox.addItems(defaultConf["defaultExecutionOptions"])
        self.formObjects.defaultExecutionModeBox.setCurrentText(defaultConf["defaultExecutionMode"])
        self.formObjects.resultPathBox.setText(defaultConf["resultPath"])
        self.formObjects.legacyModePathBox.setText(defaultConf["legacyModePath"])
        self.formObjects.errinjModePathBox.setText(defaultConf["errinjModePath"])
        self.formObjects.analyzerMinVersionBox.setText(defaultConf["analyzerMinVersion"])

    def isFormValid(self):
        if self.formObjects.resultPathBox.text() == "" \
            or self.formObjects.legacyModePathBox.text() == "" \
            or self.formObjects.errinjModePathBox.text() == ""\
            or self.formObjects.analyzerMinVersionBox.text() == "":
            GUIUtills.PopUpWarning("please make sure that all the fields are filled")
            return False
        elif self.formObjects.portBox.value() < 1025 or self.formObjects.portBox.value() > 65535:
            GUIUtills.PopUpWarning("port must be greater then 1024 and less then 65535")
            return False
        return True

    def accept(self):
        if self.isFormValid():
            defaultConf = self.mainWindowRef.controller.configs.defaultConfContent
            defaultConf["hostPcServerPort"] = self.formObjects.portBox.value()
            defaultConf["attempsToCreateSocket"] = self.formObjects.conectionAttempsBox.value()
            defaultConf["defaultExecutionMode"] = str(self.formObjects.defaultExecutionModeBox.currentText())
            defaultConf["resultPath"] = self.formObjects.resultPathBox.text()
            defaultConf["legacyModePath"] = self.formObjects.legacyModePathBox.text()
            defaultConf["errinjModePath"] = self.formObjects.errinjModePathBox.text()
            defaultConf["analyzerMinVersion"] = self.formObjects.analyzerMinVersionBox.text()

            GUIUtills.PopUpWarning("in order for changes to take effect you need to save the configuration and "
                                   "launch the application using the new configuration")
            self.close()




