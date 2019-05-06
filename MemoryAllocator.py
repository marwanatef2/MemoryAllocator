from PyQt5.QtWidgets import QDialog, QWidget,QLineEdit, QGridLayout, QRadioButton, QHBoxLayout, QPushButton, QSpinBox, QApplication, QVBoxLayout, QLabel, QGroupBox
import sys
from PyQt5 import QtGui, QtCore

# main window
class MainWindow(QDialog) :
    def __init__(self):
        super().__init__()

        #setting the main window in the class constructor
        self.title = "Memory Allocator"
        self.left = 500
        self.top = 200
        self.width = 350
        self.height = 250
        self.iconName = "E:/Marwan/projects/memory-allocator/ram.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        # vbox & grid to resize the window
        vbox = QVBoxLayout()
        grid = QGridLayout()

        maingroupbox = QGroupBox("Info")
        maingroupbox.setFont(QtGui.QFont("Sanserif", 14))
        
        # first group box for memory size
        groupbox1 = QGroupBox("Memory Size")
        groupbox1.setFont(QtGui.QFont("Sanserif", 14))
        groupbox1.setMinimumHeight(175)

        hbox1 = QHBoxLayout()

        # label used for user friendly purposes
        self.label1 = QLabel("Size of Memory : ")
        self.label1.setFont(QtGui.QFont("Sanserif", 12))
        hbox1.addWidget(self.label1)

        # line edit to take memory size from user
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setFont(QtGui.QFont("Sanserif", 12))
        self.lineEdit1.setMaximumWidth(100)
        hbox1.addWidget(self.lineEdit1)

        groupbox1.setLayout(hbox1)

        grid.addWidget(groupbox1,0,0)

        # 2nd group box for allocation type
        groupbox2 = QGroupBox("Memory Size")
        groupbox2.setFont(QtGui.QFont("Sanserif", 14))
        groupbox2.setMinimumHeight(175)

        hbox2 = QHBoxLayout()

        self.radiobtn1 = QRadioButton("First fit")
        self.radiobtn1.setFont((QtGui.QFont("Sanserif", 12)))
        hbox2.addWidget(self.radiobtn1)

        self.radiobtn2 = QRadioButton("Best fit")
        self.radiobtn2.setFont((QtGui.QFont("Sanserif", 12)))
        hbox2.addWidget(self.radiobtn2)

        groupbox2.setLayout(hbox2)

        grid.addWidget(groupbox2,0,1)

        # third group box for no of processes
        groupbox3 = QGroupBox("Processes")
        groupbox3.setFont(QtGui.QFont("Sanserif", 14))
        groupbox3.setMinimumHeight(175)

        hbox3 = QHBoxLayout()

        # label used for user friendly purposes
        self.label3 = QLabel("No. of processes :")
        self.label3.setFont(QtGui.QFont("Sanserif", 12))
        hbox3.addWidget(self.label3)

        # spin box to determine no of processes
        self.spinBox3 = QSpinBox()
        self.spinBox3.setFont(QtGui.QFont("Sanserif", 10))
        self.spinBox3.setMaximumWidth(100)
        hbox3.addWidget(self.spinBox3)

        groupbox3.setLayout(hbox3)

        grid.addWidget(groupbox3,1,0)

        # fourth group box for no of holes
        groupbox4 = QGroupBox("Holes")
        groupbox4.setFont(QtGui.QFont("Sanserif", 14))
        groupbox4.setMinimumHeight(175)

        hbox4 = QHBoxLayout()

        # label used for user friendly purposes
        self.label4 = QLabel("No. of holes :")
        self.label4.setFont(QtGui.QFont("Sanserif", 12))
        hbox4.addWidget(self.label4)

        # spin box to determine no of holes
        self.spinBox4 = QSpinBox()
        self.spinBox4.setFont(QtGui.QFont("Sanserif", 10))
        self.spinBox4.setMaximumWidth(100)
        hbox4.addWidget(self.spinBox4)

        groupbox4.setLayout(hbox4)

        grid.addWidget(groupbox4,1,1)

        # a push button to switch to 2nd menu
        self.button = QPushButton("Next", self)
        self.button.setFont(QtGui.QFont("Sanserif", 12))
        self.button.setToolTip("Proceed to next step")
        self.button.setMaximumWidth(300)
        self.button.setMinimumWidth(150)
        self.button.clicked.connect(self.onButtonPressed)

        maingroupbox.setLayout(grid)

        vbox.addWidget(maingroupbox)
        vbox.addWidget(self.button, 0, QtCore.Qt.AlignCenter)

        self.setLayout(vbox)

    # function that calls 2nd window to take more info about holes and processes
    # when the button is pressed
    # and fetches inputs
    def onButtonPressed(self):
        self.memorySize = self.lineEdit1.text()
        if self.radiobtn1.isChecked():
            self.allocatingType = "FF"  
        elif self.radiobtn2.isChecked():
            self.allocatingType = "BF"
        self.noOfProcesses = self.spinBox3.value()
        self.noOfHoles = self.spinBox4.value()

        self.hide()
        self.secondwindow = SecondWindow(self.memorySize, self.allocatingType, self.noOfProcesses, self.noOfHoles)


# 2nd window
class SecondWindow(QDialog) :
    def __init__(self, memsize, allocatetype, noprocesses, noholes):
        super().__init__()

        self.memorySize = memsize
        self.allocatingType =  allocatetype
        self.noOfProcesses = noprocesses
        self.noOfHoles = noholes

        #setting the main window in the class constructor
        self.title = "Memory Allocator"
        self.left = 500
        self.top = 200
        self.width = 350
        self.height = 250
        self.iconName = "E:/Marwan/projects/memory-allocator/ram.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        vbox = QVBoxLayout()
        self.grid1 = QGridLayout()
        self.grid2 = QGridLayout()

        self.segmentslist = []
        self.startlist = []
        self.sizelist = []

        processgroupbox = QGroupBox("Processes Info")
        processgroupbox.setFont(QtGui.QFont("Sanserif", 14))

        holesgroupbox = QGroupBox("Processes Info")
        holesgroupbox.setFont(QtGui.QFont("Sanserif", 14))

        # for each process get no of segments
        for i in range(self.noOfProcesses):

            hbox = QHBoxLayout()

            # group box for each process
            groupbox = QGroupBox("Process " + str(i+1))
            groupbox.setFont(QtGui.QFont("Sanserif", 14))
            groupbox.setMinimumHeight(100)
            groupbox.setMaximumHeight(150)

            self.label1 = QLabel("No. of Segments")
            self.label1.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label1)

            # for the input of no of segments
            self.lineEdit1 = QLineEdit(self)
            self.lineEdit1.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit1.setMaximumWidth(100)
            hbox.addWidget(self.lineEdit1)

            # appending the arrival time in a list
            # so as to access its value later on
            self.segmentslist.append(self.lineEdit1)

            groupbox.setLayout(hbox)

            if i%2 == 0:
                self.grid1.addWidget(groupbox, i, 0)
            else :
                self.grid1.addWidget(groupbox, i-1, 1)

        # for each hole get start address and size
        for i in range(self.noOfHoles):

            hbox = QHBoxLayout()

            # group box for each process
            groupbox = QGroupBox("Hole " + str(i+1))
            groupbox.setFont(QtGui.QFont("Sanserif", 14))
            groupbox.setMinimumHeight(100)
            groupbox.setMaximumHeight(150)

            self.label1 = QLabel("Start")
            self.label1.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label1)

            # for the input of start
            self.lineEdit1 = QLineEdit(self)
            self.lineEdit1.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit1.setMaximumWidth(100)
            hbox.addWidget(self.lineEdit1)

            # appending the start in a list
            # so as to access its value later on
            self.startlist.append(self.lineEdit1)

            hbox.addStretch()

            self.label2 = QLabel("Size")
            self.label2.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label2)

            # for the input of size
            self.lineEdit2 = QLineEdit(self)
            self.lineEdit2.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit2.setMaximumWidth(100)
            hbox.addWidget(self.lineEdit2)

            # appending the arrival time in a list
            # so as to access its value later on
            self.sizelist.append(self.lineEdit2)

            groupbox.setLayout(hbox)

            if i%2 == 0:
                self.grid2.addWidget(groupbox, i, 0)
            else :
                self.grid2.addWidget(groupbox, i-1, 1)

        # a push button to switch to 3nd menu
        self.button = QPushButton("Next", self)
        self.button.setFont(QtGui.QFont("Sanserif", 12))
        self.button.setToolTip("Proceed to next step")
        self.button.setMaximumWidth(300)
        self.button.setMinimumWidth(150)
        # self.button.clicked.connect(self.onButtonPressed)

        processgroupbox.setLayout(self.grid1)
        holesgroupbox.setLayout(self.grid2)
        
        vbox.addWidget(processgroupbox)
        vbox.addWidget(holesgroupbox)
        vbox.addWidget(self.button, 0, QtCore.Qt.AlignCenter)

        self.setLayout(vbox)



# running the program
App = QApplication(sys.argv)
window = MainWindow()
sys.exit(App.exec())