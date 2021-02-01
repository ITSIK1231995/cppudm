

from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore
from UI.GUI.AddAndEditHostPc import *





class exerHostGroupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,mainWindowRef):
        super(exerHostGroupBox, self).__init__( centralwidget)

        self.mainWindowRef = mainWindowRef
        self.setGeometry(QtCore.QRect(10, 150, 260, 280))
        self.setObjectName("hostExercisersGroupBox")
        self.vbox = QVBoxLayout()

        self.hostPcs = mainWindowRef.controller.configs.defaultConfContent['hostPCs']

        self.hostPCTableSetup()
        self.scrollSetup()
        self.addHostBtnSetup()


    def addHostBtnSetup(self):
        self.addHostPcBtn = QtWidgets.QPushButton(self)
        self.addHostPcBtn.setGeometry(QtCore.QRect(185, 5, 75, 23))
        self.addHostPcBtn.setObjectName("addHostPc")
        self.addHostPcBtn.clicked.connect(self.addHostPcBtnClicked)

    def hostPCTableSetup(self):

        self.hostPcRows = {}
        for hostPc in self.hostPcs:
            self.addHostPcRow(hostPc)

    def addHostPcRow(self,hostPc):
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

        editButton = QtWidgets.QPushButton(groupBox)
        editButton.setGeometry(QtCore.QRect(155, 0, 30, 20))
        editButton.setObjectName("edit_" + hostPc['IP'])
        editButton.clicked.connect(self.editBtnClicked)

        delButton = QtWidgets.QPushButton(groupBox)
        delButton.setGeometry(QtCore.QRect(185, 0, 43, 20))
        delButton.setObjectName("del_" + hostPc['IP'])
        delButton.clicked.connect(self.delBtnClicked)

        groupBox.setFixedHeight(20)
        groupBox.setFixedWidth(260)
        self.vbox.addWidget(groupBox)

        hostPcRowNamedtuple = namedtuple('hostPcRow', ['checkBox',  'showButton', 'editButton','delButton','containingGroupBox'])
        self.hostPcRows[hostPc['IP']] = hostPcRowNamedtuple(checkBox,  showButton, editButton,delButton,groupBox)


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
        AddAndEditHostPc(True,hostPc,self.mainWindowRef).exec()

    def userIsSureHeWantsTODel(self,IP):
        return GUIUtills.PopUpWarning("Are you sure you want to delete hostPc " + str(IP) + " ?\n "
                                        "this delete all tests and data configured")
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
        self.mainWindowRef.setNewHostPC(hostPc)


    def addHostPcBtnClicked(self):
        AddAndEditHostPc(False,None,self.mainWindowRef).exec()



    def retranslateUi(self):
        self.setToolTip("Hosts list")
        self.setTitle("Exerciser / Host")
        for hostPc in self.hostPcs:
            self.hostPcRows[hostPc['IP']].checkBox.setText(hostPc['IP'])
            self.hostPcRows[hostPc['IP']].checkBox.setChecked(hostPc['checked'])
            self.hostPcRows[hostPc['IP']].editButton.setText("Edit")
            self.hostPcRows[hostPc['IP']].showButton.setText("Show")
            self.hostPcRows[hostPc['IP']].delButton.setText("Delete")
        self.addHostPcBtn.setText("Add Host Pc")


