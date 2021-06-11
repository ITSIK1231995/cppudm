from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore

from UI.GUI import systemModes
from UI.GUI.AddAndEditHostPc import *
from UI.GUI.colorConvertor import *

DEFAULT_COLOR_TO_CHOSEN_HOST_PC = "background-color: rgb(124, 226, 252);"


class exerHostGroupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget, mainWindowRef):
        super(exerHostGroupBox, self).__init__(centralwidget)
        self.mainWindowRef = mainWindowRef
        self.setGeometry(QtCore.QRect(10, 150, 260, 280))
        self.setObjectName("hostExercisersGroupBox")
        self.vbox = QVBoxLayout()
        self.controller = mainWindowRef.controller
        if self.controller.configs:
            if self.controller.currentSystemExecutionMode.name == systemModes.systemExecutionModes.LEGACY_MODE_HOST_PC.name:
                self.hostPcs = self.controller.configs.defaultConfContent['hostPCs']
            else:
                self.hostPcs = self.controller.configs.defaultConfContent['Exercisers']
            self.hostPCTableSetup()
            self.scrollSetup()
            self.addHostBtnSetup()
            if len(self.hostPcs) != 0:
                self.currHostPc = self.getFirstHostPc()
                self.setColortoCurrHostCheckBox()

    def getFirstHostPc(self):
        return self.hostPcs[0]

    def setColortoCurrHostCheckBox(self, ):
        self.setDefaultColorToChoosenHostPc(self.currHostPc)

    def addHostBtnSetup(self):
        self.addHostPcBtn = QtWidgets.QPushButton(self)
        self.addHostPcBtn.setGeometry(QtCore.QRect(130, 5, 125, 23))
        self.addHostPcBtn.setObjectName("addHostPc")
        self.addHostPcBtn.setStyleSheet("background-color:rgb(255,178,102)");
        self.addHostPcBtn.clicked.connect(self.addHostPcBtnClicked)

    def hostPCTableSetup(self):
        self.hostPcRows = {}
        for hostPc in self.hostPcs:
            self.addHostPcRow(hostPc)

    def addHostPcRow(self, hostPc):
        groupBox = QtWidgets.QGroupBox()
        groupBox.setObjectName("GroupBox_" + hostPc['IP'])

        checkBox = QtWidgets.QCheckBox(groupBox)
        checkBox.setGeometry(QtCore.QRect(0, 0, 100, 21))
        checkBox.setObjectName("groupCheckBox_" + hostPc['IP'])
        checkBox.clicked.connect(self.onCheckBoxClicked)

        showButton = QtWidgets.QPushButton(groupBox)
        showButton.setGeometry(QtCore.QRect(120, 0, 35, 20))
        showButton.setObjectName("show_" + hostPc['IP'])
        showButton.clicked.connect(self.showBtnClicked)
        showButton.setStyleSheet("background-color:rgb(51,153,255)")

        editButton = QtWidgets.QPushButton(groupBox)
        editButton.setGeometry(QtCore.QRect(155, 0, 30, 20))
        editButton.setObjectName("edit_" + hostPc['IP'])
        editButton.clicked.connect(self.editBtnClicked)
        editButton.setStyleSheet("background-color:rgb(255,178,102)")

        delButton = QtWidgets.QPushButton(groupBox)
        delButton.setGeometry(QtCore.QRect(185, 0, 43, 20))
        delButton.setObjectName("del_" + hostPc['IP'])
        delButton.clicked.connect(self.delBtnClicked)
        delButton.setStyleSheet("background-color:rgb(255,153,153)")

        groupBox.setFixedHeight(20)
        groupBox.setFixedWidth(260)
        self.vbox.addWidget(groupBox)

        hostPcRowNamedtuple = namedtuple('hostPcRow',
                                         ['checkBox', 'showButton', 'editButton', 'delButton', 'containingGroupBox'])
        self.hostPcRows[hostPc['IP']] = hostPcRowNamedtuple(checkBox, showButton, editButton, delButton, groupBox)

    def onCheckBoxClicked(self):
        clickedCheckBox = self.sender()
        hostPc = self.getHostPCFromBtnName(clickedCheckBox)
        hostPc['checked'] = clickedCheckBox.isChecked()

    def scrollSetup(self):
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scroll = QScrollArea(self)  # Scroll Area which contains the widgets, set as the centralWidget
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QtCore.QRect(0, 30, 260, 250))

    def getHostPCFromBtnName(self, btn):
        hostPcIp = btn.objectName().split('_')[1]
        return next((hostPc for hostPc in self.hostPcs if hostPc['IP'] == hostPcIp), None)

    def editBtnClicked(self):
        hostPc = self.getHostPCFromBtnName(self.sender())
        AddAndEditHostPc(True, hostPc, self.mainWindowRef).exec()

    def editSpecificHostPcCheckBoxLabel(self, IP, newAliasForHostPc):
        self.hostPcRows[IP].checkBox.setText(newAliasForHostPc)

    def userIsSureHeWantsTODel(self, IP):
        return GUIUtills.PopUpWarning("Are you sure you want to delete System Under Test " + str(IP) + " ?\n " "This will delete all tests and data configured")

    def delBtnClicked(self):
        hostPc = self.getHostPCFromBtnName(self.sender())
        oldHostPCIP = hostPc["IP"]
        if self.userIsSureHeWantsTODel(hostPc["IP"]):
            self.hostPcRows[hostPc["IP"]].containingGroupBox.deleteLater()
            self.hostPcs.remove(hostPc)
            # if current displayed host pc is deleted then swap for another one
            if self.mainWindowRef.currentHostPc["IP"] == oldHostPCIP:
                if len(self.hostPcs) == 0:
                    self.mainWindowRef.setNewHostPC(None)
                else:
                    self.mainWindowRef.setNewHostPC(self.hostPcs[0])

    def showBtnClicked(self):
        hostPc = self.getHostPCFromBtnName(self.sender())
        self.setColorForPickedShowBtn(hostPc)
        self.mainWindowRef.setNewHostPC(hostPc)

    def setColorForPickedShowBtn(self, pickedHostPc):  # When clicking on the Show button.
        # this statement used for set color to the host pc after clicking "show" on other host pc
        if len(self.hostPcs) == 1:
            self.currHostPc = pickedHostPc
            self.setColortoCurrHostCheckBox()
        if self.currHostPc["IP"] in self.controller.runtimeHostPcsData.keys() \
                and 'hostPcLblColor' in self.controller.runtimeHostPcsData[self.currHostPc["IP"]].keys():
            self.hostPcRows[self.currHostPc["IP"]].checkBox.setStyleSheet(COLOR_CONVERTER[self.controller.runtimeHostPcsData[self.currHostPc["IP"]]['hostPcLblColor']])
        elif self.currHostPc in self.hostPcs:
            self.hostPcRows[self.currHostPc["IP"]].checkBox.setStyleSheet('background-color: None')
        self.setDefaultColorToChoosenHostPc(pickedHostPc)
        self.currHostPc = pickedHostPc

    def setDefaultColorToChoosenHostPc(self, hostPcPicked):  # Set light blue color to the host pc that was choosen
        self.hostPcRows[hostPcPicked["IP"]].checkBox.setStyleSheet(DEFAULT_COLOR_TO_CHOSEN_HOST_PC)

    def addHostPcBtnClicked(self):
        AddAndEditHostPc(False, None, self.mainWindowRef).exec()

    def retranslateUi(self):
        self.setToolTip("System Under Test list")
        self.setTitle("Exercisers / SUTs")
        self.setStyleSheet("background-color:rgb(224,224,224)")

        for hostPc in self.hostPcs:
            if hostPc["alias"] != ""\
                and hostPc["alias"] != None:
                self.hostPcRows[hostPc['IP']].checkBox.setText(hostPc['alias'])
            else:
                self.hostPcRows[hostPc['IP']].checkBox.setText(hostPc['IP'])
            self.hostPcRows[hostPc['IP']].checkBox.setChecked(hostPc['checked'])
            self.hostPcRows[hostPc['IP']].editButton.setText("Edit")
            self.hostPcRows[hostPc['IP']].showButton.setText("Show")
            self.hostPcRows[hostPc['IP']].delButton.setText("Delete")
        self.addHostPcBtn.setText("Add System Under Test")
