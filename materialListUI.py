import sys
from screeninfo import get_monitors
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGridLayout, QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem
import json



class mainProgram(QMainWindow):
    def __init__(self, tableHeaders = ['Item No.'], masterMaterialList = {'':''}):
        super(mainProgram, self).__init__()

        self.matListFileName = 'projectMatlist.json'
        
        self.monitor = get_monitors()
        '''Defines monitor object that allows automatic screen window sizing per screen size'''
        self.monitorXSize = int()
        '''Defines width of user's monitor'''
        self.monitorYSize = int()
        '''Defines height of user's monitor'''
        self.xShift = int()
        '''Defines x shift used to center window'''
        self.yShift = int()
        '''Defines y shift used to center window'''
        self.xSize = int()
        '''Defines width of window'''
        self.ySize = int()
        '''Defines height of window'''

        self.tableWidget = QTableWidget()                   
        '''Defines Main Scrollable Table'''
        self.tableWidgetItems = [[]] #customTableWidgetItem
        '''Defines objects to be slotted into main table cells'''
        self.tableHeaders = tableHeaders
        '''Defines headers for the main table \n'''
        

        self.dock = QDockWidget('Menu')
        '''Defines right-side dock'''
        self.dockMenu = QWidget()
        '''Defines widget to be added to right-side dock'''
        self.dockLayout = QFormLayout()
        '''Defines layout for widget on right-side dock'''
        self.dockItemPanels = [QLineEdit()]
        '''Defines One Text box per panel to allow for new row addition'''
        self.addButton = QPushButton()
        '''Defines button on right-side dock that makes new entry from right-side dock data'''
        self.deviceNames = [QLineEdit()]
        '''Defines text boxes on right-side dock used to enter individual device names'''
        self.deviceNameSlots = 0
        self.spacer = QSpacerItem(0,0)
        '''Defines space between the add section of the right-side dock and the rest of the right-side dock'''
        self.printButton = QPushButton()
        '''Defines button to print the current table to the console'''

        self.currentlySelectedCell = [0,0]

        self.uniqueItemNumbers = []
        
        self.masterMatList = masterMaterialList
        '''Defines a dictionary of form {"|Item No.|":"|Description|"}'''
        

        #Initial Setup
        self.buildMainWindow()
        data = self.importData(self.matListFileName)
        self.getUniqueItemNumbers(data)
        self.buildInitialTable(data)
        self.buildRightDock()

        #Main Loop
        self.mainProgramLoop()

    def buildMainWindow(self):
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xShift = int(self.monitorXSize*.25)
        self.yShift = int(self.monitorYSize*.25)
        self.xSize = int(self.monitorXSize/2)
        self.ySize = int(self.monitorYSize/2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Material to Contract')

    def importData(self, input):
        '''If input is a string representing a path to a json file, import data from the json file\n
        If input is a dictionary, import data from the dictionary'''
        if type(input) == type(str()):
            with open(input) as jsonFile:
                data = json.load(jsonFile)
        
        if type(input) == type(dict()):
            data = input
            for i in list(data.keys()):
                self.tableHeaders.append(i)

        return data   

    def getUniqueItemNumbers(self,data):
        for panel in data:
            for item in data[panel]:
                if item != 'description' and item not in self.uniqueItemNumbers:
                    self.uniqueItemNumbers.append(item)
        self.uniqueItemNumbers.sort()

    def buildInitialTable(self, data):
        '''Dimensions[0] = rows, Dimensions[1] = columns'''
        dimensions = [len(self.uniqueItemNumbers),len(self.tableHeaders)]
        self.tableWidget.setColumnCount(dimensions[1])
        for i in range(dimensions[1]):
            self.tableWidget.setColumnWidth(i,200)
        self.tableWidget.setRowCount(dimensions[0])
        self.tableWidget.setHorizontalHeaderLabels(self.tableHeaders)
        
        for panelIndex, panel in enumerate(self.tableHeaders):
            for itemIndex, item in enumerate(self.uniqueItemNumbers):
                if panel != 'Item No.':
                    #self.tableWidget.setItem(itemIndex,panelIndex,customTableWidgetItem(data[panel][item]['count']))
                    cell = customTableWidgetItem(data[panel][item]['count'])
                    cell.currentTextChanged.connect(self.buildRightDock)
                    self.tableWidget.setCellWidget(itemIndex,panelIndex,cell)
                if panel == 'Item No.':
                    #itemNumberCell = customTableWidgetItem(item)
                    itemNumberCell = QTableWidgetItem(item)
                    itemNumberCell.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled) #Disables editing of the first column
                    self.tableWidget.setItem(itemIndex,panelIndex,itemNumberCell)

        self.tableWidget.itemChanged.connect(self.tableItemChanged)
        self.tableWidget.itemSelectionChanged.connect(self.tableItemSelectionChanged)

        self.setCentralWidget(self.tableWidget)

    def buildRightDock(self):
        self.removeDockWidget(self.dock)
        self.dockItemSelect = QComboBox()
        for item in self.uniqueItemNumbers:
            self.dockItemSelect.addItem(item)

        self.dockItemPanels = []
        for panel in self.tableHeaders[1:]:
            dockItemCountEntry = QLineEdit()
            dockItemCountEntry.setPlaceholderText(panel)
            self.dockItemPanels.append(dockItemCountEntry)

        self.addItemButton = QPushButton('Add Entry',clicked=self.addItem)
        self.printButton = QPushButton('Print Data to Console',clicked=self.printDataToConsole)

        self.deviceNameSlots = 0
        if self.currentlySelectedCell[1] >= 1:
            #self.deviceNameSlots = int(self.tableWidget.item(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).text())
            self.deviceNameSlots = int(self.tableWidget.cellWidget(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).currentText())
            
        
        self.deviceNames = [QLineEdit() for i in range(self.deviceNameSlots)]
        for i in range(len(self.deviceNames)):
            self.deviceNames[i].setPlaceholderText(f'Device {i+1} Name:')
        self.updateDeviceNamesButton = QPushButton('Update Device Names',clicked=self.updateDeviceNames)
        

        self.dockLayout = QFormLayout()
        self.dockLayout.addRow(self.dockItemSelect)
        for i in self.dockItemPanels:
            self.dockLayout.addRow(i)
        self.dockLayout.addRow(self.addItemButton)
        for i in self.deviceNames:
            self.dockLayout.addRow(i)
        self.dockLayout.addRow(self.updateDeviceNamesButton)
        self.dockLayout.addRow(self.printButton)


        self.dockMenu = QWidget()
        self.dockMenu.setLayout(self.dockLayout)


        self.dock = QDockWidget('Menu')
        #self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)   
        self.dock.setWidget(self.dockMenu)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock) 

    def tableItemSelectionChanged(self):
        self.currentlySelectedCell = (self.tableWidget.currentRow(),self.tableWidget.currentColumn())
        self.buildRightDock()

    def tableItemChanged(self):
        pass

    def addItem(self):
        pass

    def printDataToConsole(self):
        pass

    def updateDeviceNames(self):
        pass

    def mainProgramLoop(self):
        #Functions attached to events or buttons:
        #tableItemSelectionChanged()
        #tableItemChanged()
        #addItem()
        #printDataToConsole()
        
        
        pass

# class customTableWidgetItem(QTableWidgetItem):
#     def __init__(self,text,deviceNames=[]):
#         super(customTableWidgetItem,self).__init__(text)
#         self.deviceNames = deviceNames

class customTableWidgetItem(QComboBox):
    def __init__(self,text,deviceNames=[]):
        super(customTableWidgetItem,self).__init__()
        self.addItems([str(i) for i in range(0,99)])
        self.setCurrentText(text)
        self.deviceNames = deviceNames



if  __name__ == "__main__":
    app = QApplication([])
    application = mainProgram(tableHeaders=['Item No.','Panel B1','Panel B2', 'Panel B3'],masterMaterialList={'3J':'','44':'Test','55':'Pierce'})
    application.show()
    sys.exit(app.exec())