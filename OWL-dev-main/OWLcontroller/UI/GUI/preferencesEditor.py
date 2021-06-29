from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout)
from collections import namedtuple
from UI.GUI.GUIUtills import *

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
        layout.addRow(QLabel("System Under Test Port:"), portBox)
        conectionAttempsBox = QSpinBox()
        conectionAttempsBox.setMinimum(4)
        layout.addRow(QLabel("Connection TO (Minutes):"), conectionAttempsBox)
        defaultExecutionModeBox =  QComboBox()
        layout.addRow(QLabel("Default Execution Mode:"), defaultExecutionModeBox)
        resultPathBox = QLineEdit()
        layout.addRow(QLabel("Result Path:"),resultPathBox)
        legacyModePathBox = QLineEdit()
        legacyModePathBox.setEnabled(False)
        layout.addRow(QLabel("Legacy Mode Path:"), legacyModePathBox)
        # disable Errinj Mode has it canceled for now
        # errinjModePathBox = QLineEdit()
        # layout.addRow(QLabel("Errinj Mode Path:"), errinjModePathBox)
        analyzerMinVersionBox = QLineEdit()
        layout.addRow(QLabel("Analyzer Min Version:"), analyzerMinVersionBox)
        self.formGroupBox.setLayout(layout)
        # disable Errinj Mode has it canceled for now
        # formObjectsNamedTuple = namedtuple('formObjects', ['portBox', 'conectionAttempsBox','defaultExecutionModeBox','resultPathBox','legacyModePathBox','errinjModePathBox','analyzerMinVersionBox'])
        # self.formObjects = formObjectsNamedTuple(portBox, conectionAttempsBox,defaultExecutionModeBox,resultPathBox,legacyModePathBox,errinjModePathBox,analyzerMinVersionBox)
        formObjectsNamedTuple = namedtuple('formObjects', ['portBox', 'conectionAttempsBox','defaultExecutionModeBox','resultPathBox','legacyModePathBox','analyzerMinVersionBox'])
        self.formObjects = formObjectsNamedTuple(portBox, conectionAttempsBox,defaultExecutionModeBox,resultPathBox,legacyModePathBox,analyzerMinVersionBox)

    def fillWithData(self):
        defaultConf = self.mainWindowRef.controller.configs.defaultConfContent
        self.formObjects.portBox.setValue(defaultConf["hostPcServerPort"])
        self.formObjects.conectionAttempsBox.setValue(defaultConf["attempsToCreateSocket"])
        self.formObjects.defaultExecutionModeBox.addItems(defaultConf["defaultExecutionOptions"])
        self.formObjects.defaultExecutionModeBox.setCurrentText(defaultConf["defaultExecutionMode"])
        self.formObjects.resultPathBox.setText(defaultConf["resultPath"])
        self.formObjects.legacyModePathBox.setText(defaultConf["legacyModePath"])
        # self.formObjects.errinjModePathBox.setText(defaultConf["errinjModePath"])  #disable Errinj Mode has it removed from SRS (at the moment)
        self.formObjects.analyzerMinVersionBox.setText(defaultConf["analyzerMinVersion"])

    def isFormValid(self):
        if self.formObjects.resultPathBox.text() == "" \
            or self.formObjects.legacyModePathBox.text() == ""\
            or self.formObjects.analyzerMinVersionBox.text() == "":
            # or self.formObjects.errinjModePathBox.text() == "" \  #disable Errinj Mode has it removed from SRS (at the moment)

            GUIUtills.PopUpWarning("Please make sure that all the fields are filled")
            return False
        elif self.formObjects.portBox.value() < 1025 or self.formObjects.portBox.value() > 65535:
            GUIUtills.PopUpWarning("Port must be greater then 1024 and less then 65535")
            return False
        return True

    def accept(self):
        if self.isFormValid():
            defaultConf = self.mainWindowRef.controller.configs.defaultConfContent
            defaultConf["hostPcServerPort"] = self.formObjects.portBox.value()
            defaultConf["attempsToCreateSocket"] = self.formObjects.conectionAttempsBox.value()
            defaultConf["defaultExecutionMode"] = str(self.formObjects.defaultExecutionModeBox.currentText())
            defaultConf["resultPath"] = self.formObjects.resultPathBox.text()
            defaultConf["legacyModePath"] = self.formObjects.legacyModePathBox.text() #disable Errinj Mode has it canceled for now
            # defaultConf["errinjModePath"] = self.formObjects.errinjModePathBox.text()
            defaultConf["analyzerMinVersion"] = self.formObjects.analyzerMinVersionBox.text()

            GUIUtills.PopUpWarning("In order for changes to take effect you need to save the configuration and "
                                   "launch the application using the New configuration")
            self.close()




