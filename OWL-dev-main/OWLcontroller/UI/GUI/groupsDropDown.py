from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QComboBox
from UI.GUI import systemModes
from UI.GUI.GUIUtills import *

class groupsDropDown(QtWidgets.QGroupBox): #TODO need to look at this new drop down instead of group box
    def __init__(self, centralwidget, mainWindowRef):
        super(groupsDropDown, self).__init__(centralwidget)
        self.mainWindowRef = mainWindowRef
        self.setGeometry(QtCore.QRect(10, 440, 260, 185))
        self.setObjectName("selectGroupBox")
        self.vbox = QVBoxLayout()
        self.groupNames = self.getDictOfTestByGroupsForCurrentSystemMode().keys()  #TODO  look at this
        self.groupListSetup()

    def getDictOfTestByGroupsForCurrentSystemMode(self):  #TODO need to use here the isHostPC methood and also take this function to the utils because it also in more files in the GUI
        if self.mainWindowRef.controller.isCurrentExecutionModeIsHostPcMode():
            return self.mainWindowRef.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups
        else:
            return self.mainWindowRef.controller.configs.legacyMode.legacyTestsByGroup

    def groupListSetup(self):
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(10, 50, 150, 18)
        self.comboBox.addItems(self.groupNames)
        self.comboBox.activated[str].connect(self.onSelected)

    def onSelected(self):
            if self.displaySwitchGroupWarningPopUp():
                groupName = self.comboBox.currentText()
                self.mainWindowRef.setDisplayedTestGroup(groupName)

    def displaySwitchGroupWarningPopUp(self):
        return GUIUtills.PopUpWarning("Are you sure you want to switch group?\n "
                                      "Switching will delete all tests configured for current System Under Test")

    def changeSelected(self, groupName):
        self.comboBox.setCurrentText(groupName)

    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 20, 260, 165))

    def retranslateUi(self):
        self.setToolTip("Group Drop Down")
        self.setTitle("Select Group")
        self.setStyleSheet("background-color:rgb(224,224,224)")

