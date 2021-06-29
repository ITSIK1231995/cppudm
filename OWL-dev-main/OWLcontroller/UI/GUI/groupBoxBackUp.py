# from PyQt5.QtCore import Qt
# from PyQt5 import QtWidgets, QtCore
# import systemModes
# from UI.GUI.GUIUtills import *
#
#
# class groupBox(QtWidgets.QGroupBox):
#     def __init__(self, centralwidget, mainWindowRef):
#         super(groupBox, self).__init__(centralwidget)
#         self.mainWindowRef = mainWindowRef
#         self.setGeometry(QtCore.QRect(10, 440, 260, 185))
#         self.setObjectName("selectGroupBox")
#         self.vbox = QVBoxLayout()
#         self.groupNames = self.getDictOfTestByGroupsForCurrentSystemMode().keys()
#         self.groupListSetup()
#         self.scrollSetup()
#
#     def getDictOfTestByGroupsForCurrentSystemMode(self):
#         if self.mainWindowRef.controller.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC:
#             return self.mainWindowRef.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups
#         elif self.mainWindowRef.controller.currentSystemExecutionMode == systemModes.systemExecutionModes.LEGACY_MODE_EXCERCISER:
#             return self.mainWindowRef.controller.configs.legacyMode.legacyTestsByGroup
#
#     def groupListSetup(self):
#         self.groupCheckBoxArr = {}
#         first = True
#         for groupName in self.groupNames:
#             self.groupCheckBoxArr[groupName] = QtWidgets.QCheckBox(self)
#             self.groupCheckBoxArr[groupName].setGeometry(QtCore.QRect(0, 0, 64, 18))
#             self.groupCheckBoxArr[groupName].setObjectName("groupCheckBox_" + groupName)
#             self.groupCheckBoxArr[groupName].clicked.connect(self.onChacked)
#             self.vbox.addWidget(self.groupCheckBoxArr[groupName])
#
#             if first:  # set first option to be the default
#                 first = False
#                 self.groupCheckBoxArr[groupName].setChecked(True)
#                 self.mainWindowRef.setDisplayedTestGroup(groupName)
#
#     def onChacked(self):
#         clickedCheckBox = self.sender()
#         if clickedCheckBox.isChecked():
#             if self.displaySwitchGroupWarningPopUp():
#                 for checkBox in self.groupCheckBoxArr.values():
#                     if checkBox is not clickedCheckBox and checkBox.isChecked():
#                         checkBox.setChecked(False)
#                 groupName = clickedCheckBox.objectName().split('_')[1]
#                 self.mainWindowRef.setDisplayedTestGroup(groupName)
#             else:
#                 clickedCheckBox.setChecked(False)
#         else:
#             clickedCheckBox.setChecked(True)
#
#     def displaySwitchGroupWarningPopUp(self):
#         return GUIUtills.PopUpWarning("Are you sure you want to switch group?\n "
#                                       "Switching will delete all tests configured for current System Under Test")
#
#     def cahngeSelected(self, groupName):
#         for checkBox in self.groupCheckBoxArr.values():
#             if checkBox.objectName().split('_')[1] == groupName:
#                 checkBox.setChecked(True)
#             else:
#                 checkBox.setChecked(False)
#
#     def scrollSetup(self):
#         self.widget = QWidget()
#         self.widget.setLayout(self.vbox)
#         self.scroll = QScrollArea(self)
#         self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.scroll.setWidgetResizable(True)
#         self.scroll.setWidget(self.widget)
#         self.scroll.setGeometry(QtCore.QRect(0, 20, 260, 165))
#
#     def retranslateUi(self):
#         self.setToolTip("Group list")
#         self.setTitle("Select Group")
#         self.setStyleSheet("background-color:rgb(224,224,224)")
#         for groupName in self.groupNames:
#             self.groupCheckBoxArr[groupName].setText(groupName)
