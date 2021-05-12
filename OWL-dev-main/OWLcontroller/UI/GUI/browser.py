import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

class browser(QWidget):
    def __init__(self,name):
        super().__init__()
        self.title = name
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def getChoosedFolderName(self,name):
        folderName = self.openFileNameDialog(name)
        self.show()
        self.hide()
        return folderName

    def openFileNameDialog(self,name):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, name, "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName
        else:
            return ""

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
