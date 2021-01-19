
from PyQt5 import QtCore, QtGui, QtWidgets


#TODO : figure out were the groups come from
#TODO : add scrollbar
#TODO : make single select
class groupBox(QtWidgets.QGroupBox):
    def __init__(self, centralwidget,configs):
        super(groupBox, self).__init__( centralwidget)

        # self.selectGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.setGeometry(QtCore.QRect(10, 350, 131, 131))
        self.setObjectName("selectGroupBox")

        self.groupNames = configs.legacyMode.legacyFlowOperationsTestsByGroups.keys()
        posX = 1
        self.groupCheckBoxArr = {}
        for groupName in self.groupNames:
            self.groupCheckBoxArr[groupName] = QtWidgets.QCheckBox(self)
            self.groupCheckBoxArr[groupName].setGeometry(QtCore.QRect(20, 25*posX, 64, 18))
            self.groupCheckBoxArr[groupName].setObjectName("groupCheckBox_"+groupName)
            posX+=1


    def retranslateUi(self, skippedTestsNumber,_translate):
        self.setToolTip(_translate("skippedTestsNumber", "Hosts list"))
        self.setTitle(_translate("skippedTestsNumber", "Select Group"))
        for groupName in self.groupNames:
            self.groupCheckBoxArr[groupName].setText(_translate("skippedTestsNumber",groupName))

