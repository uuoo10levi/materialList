import sys
from screeninfo import get_monitors
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem
import json

class AddMaterial(QMainWindow):

    def __init__(self):
        super(AddMaterial, self).__init__()


        self.monitor = get_monitors()
        self.monitorXSize = int()
        self.monitorYSize = int()
        self.xShift = int()
        self.yShift = int()
        self.xSize = int
        self.ySize = int()

        self.itemNoComboBox = [QComboBox()]
        self.dock = QDockWidget('A')
        self.dockLayout = QFormLayout()

        self.dockMenu = QDockWidget
        self.dockLayout = QFormLayout

        self.buildMainWindow()
        self.buildRightDock()

    def buildMainWindow(self):
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xShift = int(self.monitorXSize*.25)
        self.yShift = int(self.monitorYSize*.25)
        self.xSize = int(self.monitorXSize/2)
        self.ySize = int(self.monitorYSize/2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Material to Contract')

    def buildRightDock(self):
        self.removeDockWidget(self.dock)
        self.dock = QDockWidget('Menu')                                                 #Defines a dock object
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)       #Mandatory dock setup
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock) 

        self.dockMenu = QWidget()                                                       #Define widget that will be attached to the dock
        self.dockLayout = QFormLayout()                                                 #Define layout that will be applied to above widget

        self.removeDockWidget(self.dock)
        self.dock = QDockWidget('Description')                                                 #Defines a dock object
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)       #Mandatory dock setup
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock)     #Add dock to main window
        

        self.dockMenu = QWidget()                                                       #Define widget that will be attached to the dock
        self.dockLayout = QFormLayout()

        self.itemNo = QLineEdit()
        self.manufactor = QLineEdit()
        self.shortName = QLineEdit()
        self.modelNumber = QLineEdit()

        self.dockLayout.addRow(self.itemNo)
        self.dockLayout.addRow(self.manufactor)
        self.dockLayout.addRow(self.shortName)
        self.dockLayout.addRow(self.modelNumber)

        self.dockMenu.setLayout(self.dockMenu)
        self.dock.setWidget(self.dock)


if  __name__ == "__main__":
    app = QApplication([])
    application = AddMaterial()
    application.show()
    sys.exit(app.exec())