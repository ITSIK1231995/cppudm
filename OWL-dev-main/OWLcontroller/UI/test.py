from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtCore

import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        _translate = QtCore.QCoreApplication.translate

        for i in range(1,50):
            selectGroupBox = QtWidgets.QGroupBox()
            selectGroupBox.setGeometry(QtCore.QRect(50, 50, 50, 50))
            selectGroupBox.setObjectName("selectGroupBox")

            groupCheckBox3_2 = QtWidgets.QCheckBox(selectGroupBox)
            groupCheckBox3_2.setGeometry(QtCore.QRect(0, 0, 200, 20))
            groupCheckBox3_2.setObjectName("groupCheckBox3_2")
            groupCheckBox3_2.setText(_translate("skippedTestsNumber", "ON"))

            groupCheckBox2_2 = QtWidgets.QCheckBox(selectGroupBox)
            groupCheckBox2_2.setGeometry(QtCore.QRect(80, 0, 200, 20))
            groupCheckBox2_2.setObjectName("groupCheckBox2_2")

            selectGroupBox.setFixedHeight(40)
            selectGroupBox.setFixedWidth(150)

            object = QLabel("TextLabel")

            self.vbox.addWidget(selectGroupBox)

        self.widget.setLayout(self.vbox)

        # self.outerBox = QtWidgets.QGroupBox(self.centralwidget)
        # self.outerBox.setGeometry(QtCore.QRect(10, 350, 131, 131))
        # self.outerBox.setObjectName("selectGroupBox")

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)




        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()

        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()