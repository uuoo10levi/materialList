#NOT RELEASED FOR USE
import sys
from screeninfo import get_monitors
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QAction, QShortcut, QMessageBox, QFileDialog, QRadioButton, QAbstractScrollArea, QSpinBox, QCheckBox, QInputDialog, QLabel, QGridLayout, QComboBox, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QSpacerItem
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
import re
import os
import csv
from datetime import date


def naturalSortKey(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(re.compile('([0-9]+)'), s)]

class revisionWindow(QMainWindow):
    def __init__(self, signals, revisionData: dict = {"date":[],"user":[],"description":[]}):
        super(revisionWindow,self).__init__()
        print(revisionData)
        self.signals = signals
        self.revisionData = revisionData

        self.monitor = get_monitors()
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xShift = int(self.monitorXSize*.1)
        self.yShift = int(self.monitorYSize*.1)
        self.xSize = int(self.monitorXSize*.8)
        self.ySize = int(self.monitorYSize*.8)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Cable List')

        self.revisionTable = QTableWidget()
        self.dockMenuButtonAddRevision = QPushButton()
        self.dockMenuButtonRemoveRevision = QPushButton()
        self.printOutput = QPushButton()
        self.dockMenuLayout = QFormLayout()
        self.dockMenuWidget = QWidget()
        self.dockMenu = QDockWidget()


        self.dockMenuButtonAddRevision.setText('Add Revision')
        self.dockMenuButtonAddRevision.clicked.connect(self.addRevision)
        self.dockMenuButtonRemoveRevision.setText('Remove Currently Selected Revision')
        self.dockMenuButtonRemoveRevision.clicked.connect(self.removeRevision)
        self.dockMenuLayout.addRow(self.dockMenuButtonAddRevision)
        self.dockMenuLayout.addRow(self.dockMenuButtonRemoveRevision)
        #self.dockMenuLayout.addRow(self.printOutput)
        self.revisionTable.setColumnCount(len(self.revisionData))

        self.revisionTable.setHorizontalHeaderLabels(self.revisionData.keys())
        self.revisionTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)


        self.dockMenuWidget.setLayout(self.dockMenuLayout)
        self.dockMenu.setWidget(self.dockMenuWidget)
        self.setCentralWidget(self.revisionTable)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dockMenu)
        self.fillTable()

    def fillTable(self):
        for rowIndex, row in enumerate(self.revisionData['date']):
            self.revisionTable.insertRow(self.revisionTable.rowCount())
            for columnIndex, column in enumerate(self.revisionData.keys()):
                item = QTableWidgetItem()
                item.setText(self.revisionData[column][rowIndex])
                self.revisionTable.setItem(self.revisionTable.rowCount()-1,columnIndex,item)

    def addRevision(self):
        self.revisionTable.insertRow(self.revisionTable.rowCount())
        for columnIndex, column in enumerate(self.revisionData.keys()):
            item = QTableWidgetItem()
            self.revisionTable.setItem(self.revisionTable.rowCount()-1,columnIndex,item)

    def removeRevision(self):
        self.revisionTable.removeRow(self.revisionTable.currentRow())

    def closeEvent(self,event):
        self.developOutputDictionary()
        self.signals.saveRevisionData.emit()

    def developOutputDictionary(self):
        for key in self.revisionData.keys():
            self.revisionData[key] = []
        for rowIndex in range(self.revisionTable.rowCount()):
            for columnIndex, column in enumerate(self.revisionData.keys()):
                self.revisionData[column].append(self.revisionTable.item(rowIndex, columnIndex).text())

class cableWindow(QMainWindow):
    def __init__(self, signals, cableData: dict = {"Item No.": [],
                                    "Cable Type": [],
                                    "Estimated Length": [],
                                    "From\nRelay Type": [],
                                    "From\nDevice Number": [],
                                    "From\nPort": [],
                                    "From\nPanel Number": [],
                                    "To\nRelay Type": [],
                                    "To\nDevice Number": [],
                                    "To\nPort": [],
                                    "To\nPanel Number": []
                                    }, 
                        availableItemNumbers = [],
                        availableCableTypes = [],
                        availableRelayTypes = [],
                        availableDeviceNumbers = [],
                        availablePanelNumbers = [],
                        ):
        super(cableWindow,self).__init__()
        self.cableData = cableData
        self.availableItemNumbers = availableItemNumbers
        self.availableCableTypes = availableCableTypes
        self.availableRelayTypes = availableRelayTypes
        self.availableDeviceNumbers = availableDeviceNumbers
        self.availablePanelNumbers = availablePanelNumbers
        self.signals = signals

        #--------------------------------------------------------------------
        #This section should never matter if cableData is entered correctly
        maxLength = max([len(self.cableData[key]) for key in self.cableData.keys()])
        for column in self.cableData.keys():
            for i in range(maxLength-len(self.cableData[column])):
                self.cableData[column].append(0)
        #--------------------------------------------------------------------
        


        self.monitor = get_monitors()
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xShift = int(self.monitorXSize*.1)
        self.yShift = int(self.monitorYSize*.1)
        self.xSize = int(self.monitorXSize*.8)
        self.ySize = int(self.monitorYSize*.8)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Cable List')




        
        self.cableTable = QTableWidget()
        self.dockMenuButtonAddCable = QPushButton()
        self.dockMenuButtonRemoveCable = QPushButton()
        self.printOutput = QPushButton()
        self.dockMenuLayout = QFormLayout()
        self.dockMenuWidget = QWidget()
        self.dockMenu = QDockWidget()

        #self.printOutput.setText('Save')
        #self.printOutput.clicked.connect(self.developOutputDictionary)
        self.dockMenuButtonAddCable.setText('Add Cable')
        self.dockMenuButtonAddCable.clicked.connect(self.addCable)
        self.dockMenuButtonRemoveCable.setText('Remove Currently Selected Cable')
        self.dockMenuButtonRemoveCable.clicked.connect(self.removeCable)
        self.dockMenuLayout.addRow(self.dockMenuButtonAddCable)
        self.dockMenuLayout.addRow(self.dockMenuButtonRemoveCable)
        #self.dockMenuLayout.addRow(self.printOutput)
        self.cableTable.setColumnCount(len(self.cableData))
        self.fillTable()


        self.cableTable.setHorizontalHeaderLabels(self.cableData.keys())
        self.cableTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)


        self.dockMenuWidget.setLayout(self.dockMenuLayout)
        self.dockMenu.setWidget(self.dockMenuWidget)
        self.setCentralWidget(self.cableTable)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dockMenu)

    def determineItemType(self, column, defaultValue = '0'):
        if column == 'Item No.':
            item = QComboBox()
            item.addItems(self.availableItemNumbers)
            item.setCurrentText(defaultValue)
        elif column == 'Cable Type':
            item = QComboBox()
            item.addItems(self.availableCableTypes)
            item.setCurrentText(defaultValue)
        elif column == 'Estimated Length':
            item = QSpinBox()
            item.setValue(int(defaultValue))
        elif column == 'From\nRelay Type' or column == 'To\nRelay Type':
            item = QComboBox()
            item.addItems(self.availableRelayTypes)
            item.setCurrentText(defaultValue)
        elif column == 'From\nDevice Number' or column == 'To\nDevice Number':
            item = QComboBox()
            item.addItems(self.availableDeviceNumbers)
            item.setCurrentText(defaultValue)
        elif column == 'From\nPort' or column == 'To\nPort':
            item = QSpinBox()
            item.setValue(int(defaultValue))
        elif column == 'From\nPanel Number' or column == 'To\nPanel Number':
            item = QComboBox()
            item.addItems(self.availablePanelNumbers)
            item.setCurrentText(defaultValue)
        
        return item

    def fillTable(self):
        for rowIndex, row in enumerate(self.cableData['Item No.']):
            self.cableTable.insertRow(self.cableTable.rowCount())
            for columnIndex, column in enumerate(self.cableData.keys()):
                item = self.determineItemType(column, defaultValue=self.cableData[column][rowIndex])
                self.cableTable.setCellWidget(self.cableTable.rowCount()-1,columnIndex,item)

    def addCable(self):
        self.cableTable.insertRow(self.cableTable.rowCount())
        for columnIndex, column in enumerate(self.cableData.keys()):
            item = self.determineItemType(column)
            self.cableTable.setCellWidget(self.cableTable.rowCount()-1,columnIndex,item)

    def removeCable(self):
        self.cableTable.removeRow(self.cableTable.currentRow())

    def developOutputDictionary(self):
        for key in self.cableData.keys():
            self.cableData[key] = []
        for rowIndex in range(self.cableTable.rowCount()):
            for columnIndex, column in enumerate(self.cableData.keys()):
                try:
                    self.cableData[column].append(str(self.cableTable.cellWidget(rowIndex,columnIndex).value()))
                except:
                    self.cableData[column].append(self.cableTable.cellWidget(rowIndex,columnIndex).currentText())

    def closeEvent(self,event):
        self.developOutputDictionary()
        self.signals.saveCableData.emit()

class mainProgram(QMainWindow):
    def __init__(self, signalClass, masterMaterialList = {'':''}):
        super(mainProgram, self).__init__()
        self.masterMatList = masterMaterialList
        self.signals = signalClass
        self.signals.refreshCellDimensions.connect(self.refreshCells)
        self.signals.needsSaved.connect(self.needsSaved)
        self.signals.saveCableData.connect(self.saveCableData)
        self.signals.saveRevisionData.connect(self.saveRevisionData)
        self.itemNoFont = QtGui.QFont()
        self.itemNoFont.setBold(True)
        self.refreshCellsShortcut = QShortcut(QtGui.QKeySequence(self.tr("R")),self)
        self.refreshCellsShortcut.activated.connect(self.refreshCells)
        self.refreshDockShortcut = QShortcut(QtGui.QKeySequence(self.tr("D")),self)
        self.refreshDockShortcut.activated.connect(self.buildRightDock)
        self.helpShortcut = QShortcut(QtGui.QKeySequence(self.tr("H")),self)
        self.helpShortcut.activated.connect(self.displayHints)
        self.cellNoteShortcut = QShortcut(QtGui.QKeySequence(self.tr('N')),self)
        self.cellNoteShortcut.activated.connect(self.addCellNote)
        self.test = QShortcut(QtGui.QKeySequence(self.tr('T')),self)
        self.test.activated.connect(self.makeCableTable)
        #self.cableDataShortcut = QShortcut(QtGui.QKeySequence(self.tr("C")),self)
        #self.cableDataShortcut.activated.connect(self.showCableData)
        #self.deviceNames = QShortcut(QtGui.QKeySequence(self.tr("N")),self)
        #self.deviceNames.activated.connect(self.getNumberOfCables)
        self.saved = False
        
        self.quit = QAction("Quit",self)
        self.quit.triggered.connect(self.closeEvent)

        code = self.startupMessage()
        if code == 0:
            exit()
        elif code == 1:
            self.newFile = True
        elif code == 2:
            self.newFile = False


        #Variable Declarations
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
        self.tableWidgetItems = [[]] 
        '''Defines objects to be slotted into main table cells'''
        self.columnHeaders = ['Item Options']
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
        self.deleteRow = QPushButton()
        self.addItemButton = QPushButton()
        self.dockItemSelect = QComboBox()


        self.currentlySelectedCell = [0,0]
        self.uniqueItemNumbers = []
        self.loosePanelPresent = False


        #Initial Setup
        
        if self.newFile:
            data = self.buildNewMatlist()
        else:
            file = QFileDialog()
            file.setNameFilters(["Text files (*.csv *.json)"])
            file.exec()
            try:
                self.matListFileName = file.selectedFiles()[0]
                self.pdfFileName = self.matListFileName.split('.')[0]+'.pdf'

                data = self.importData(self.matListFileName)
            except:
                message = QMessageBox()
                message.setText('Error Loading File\nNew File Being Created')
                message.exec()
                data = self.buildNewMatlist()
                

        self.buildMainWindow()
        self.cableData = data['cableData']
        self.revisionData = data['revisions']
        self.getUniqueItemNumbers(data)
        self.buildInitialTable(data)
        self.buildRightDock()
        self.saved = True

    def addCellNote(self):
        self.currentlySelectedCell = (self.tableWidget.currentRow(),self.tableWidget.currentColumn())
        noteBox = QInputDialog()
        noteBox.setWindowTitle("Cell Note")
        noteBox.setLabelText(f"Enter Note for item {self.uniqueItemNumbers[self.currentlySelectedCell[0]]} on panel {self.columnHeaders[self.currentlySelectedCell[1]]}")
        noteBox.exec()
        self.tableWidget.cellWidget(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).note = noteBox.textValue()

    def getAllDeviceNames(self):
        deviceNames = []
        for rowIndex, row in enumerate(self.uniqueItemNumbers):
            for columnIndex, column in enumerate(self.columnHeaders[1:]):
                for deviceName in self.tableWidget.cellWidget(rowIndex,columnIndex+1).deviceNames:
                    deviceNames.append(deviceName.text())
        return deviceNames
    
    def getNumberOfCables(self):
        total = 0
        for rowIndex, row in enumerate(self.uniqueItemNumbers):
            if row[0] == '2' and len(row) >= 3:
                for columnIndex, column in enumerate(self.columnHeaders[1:]):
                    total += self.tableWidget.cellWidget(rowIndex,columnIndex+1).countSelect.value()
        minimumCableCount = 0 #Get this from loaded json file
        return(max(total,minimumCableCount))
    
    def showCableData(self):
        availablePanels = list(self.columnHeaders) #list() forces "copy by value" instead of "copy by reference"
        if 'Loose and Not Mounted' in availablePanels:
            availablePanels.remove('Loose and Not Mounted')
        availablePanels.remove('Item Options')
        self.cableDataWindow1 = cableWindow(self.signals, self.cableData,availableItemNumbers=self.uniqueItemNumbers, availableDeviceNumbers=self.getAllDeviceNames(), availablePanelNumbers=availablePanels)
        self.cableDataWindow1.show()
        #self.saved = False

    def showRevisionData(self):
        self.revisionDataWindow1 = revisionWindow(self.signals, self.revisionData)
        self.revisionDataWindow1.show()

    def saveCableData(self):
        self.cableData = self.cableDataWindow1.cableData
        self.saved = False
        #self.export()

    def saveRevisionData(self):
        self.revisionData = self.revisionDataWindow1.revisionData
        self.saved = False
        
    def renamePanel(self):
        newPanelName = QInputDialog()
        newPanelName.setWindowTitle("Rename Panel:")
        newPanelName.setLabelText("Rename Panel:")
        newPanelName.exec()
        name = newPanelName.textValue()
        self.columnHeaders[self.currentlySelectedCell[1]] = name
        self.tableWidget.setHorizontalHeaderLabels(self.columnHeaders)
        
    def needsSaved(self):
        self.saved = False

    def startupMessage(self):
        '''Code = 0 -> Exit Program\n
        Code = 1 -> New File\n
        Code = 2 -> Existing File'''
        code = 0
        newFileDialog = QDialog()
        newFileDialog.setWindowTitle('New Material List?')
        newFileDialog.setMinimumSize(400,50)
        newFileDialogLayout = QGridLayout()
        newFileDialogMessage = QLabel("Create New Material List?")
        newFileRadioButtonYes = QRadioButton()
        newFileRadioButtonYes.setText('New Material List')
        newFileRadioButtonNo = QRadioButton()
        newFileRadioButtonNo.setText('Select Existing Material List')
        newFileDialogAccept = QPushButton('Enter')
        newFileDialogAccept.clicked.connect(newFileDialog.close)
        newFileDialogLayout.addWidget(newFileDialogMessage,0,0)
        newFileDialogLayout.addWidget(newFileRadioButtonYes,1,0)
        newFileDialogLayout.addWidget(newFileRadioButtonNo,1,1)
        newFileDialogLayout.addWidget(newFileDialogAccept)
        newFileDialog.setLayout(newFileDialogLayout)
        newFileDialog.exec()
        if newFileRadioButtonYes.isChecked():
            code = 1
        if newFileRadioButtonNo.isChecked():
            code = 2
        return code

    def closeEvent(self,event):
        if self.saved == False:
            close = QMessageBox.question(self,'QUIT','Quit Without Saving?',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if close == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
  
    def refreshCells(self):
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def buildMainWindow(self):
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xShift = int(self.monitorXSize*.1)
        self.yShift = int(self.monitorYSize*.1)
        self.xSize = int(self.monitorXSize*.8)
        self.ySize = int(self.monitorYSize*.8)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        filename = os.path.basename(self.matListFileName).split('.')[0]
        self.setWindowTitle(f'{filename} Contract List')

    def addPanel(self):        
        self.columnHeaders.append(self.newPanelName.text())
        self.tableWidget.insertColumn(self.tableWidget.columnCount())
        for row in range(self.tableWidget.rowCount()):
            cell = advancedCustomTableWidgetItem(self.signals,coordinates=(row,self.tableWidget.columnCount()-1))
            cell.oneLotSelected = self.tableWidget.cellWidget(row,0).oneLot.isChecked()
            cell.oneLot()
            cell.showDevices = self.tableWidget.cellWidget(row,0).deviceNames.isChecked()
            #print(cell.showDevices)
            self.tableWidget.setCellWidget(row,self.tableWidget.columnCount()-1,cell)
        self.tableWidget.setHorizontalHeaderLabels(self.columnHeaders)
        self.newPanelName.setText('')
        self.refreshCells()
        self.saved = False

    def buildNewMatlist(self):
        self.matListFileName = 'newFile.json'
        self.pdfFileName = self.matListFileName.split('.')[0]+'.pdf'

        #if type(input) == type(dict()):
        #data = {"Panel":{"item":{"count":'0',"names":[],"description":""}}}
        data = {}
        data['cableData'] = {"Item No.":[],
                                "Cable Type":[],
                                "Estimated Length":[],
                                "From\nRelay Type":[],
                                "From\nDevice Number":[],
                                "From\nPort":[],
                                "From\nPanel Number":[],
                                "To\nRelay Type":[],
                                "To\nDevice Number":[],
                                "To\nPort":[],
                                "To\nPanel Number":[]}
        data['revisions'] = {"date":[],"user":[],"description":[]}
        # for i in list(data.keys()):
        #     self.columnHeaders.append(i)

        return data
    
    def importData(self, inputFile):
        data = {}
        if inputFile.split('.')[1] == 'json':
            with open(inputFile) as jsonFile:
                data = json.load(jsonFile)
        elif inputFile.split('.')[1] == 'csv':
            with open (inputFile,newline='') as file:
                csvData = list(csv.reader(file))
            panelList = []
            itemList = ['description']
            for row in csvData[1:]:
                if row[0] not in itemList:
                    itemList.append(row[0])
                if row[2] not in panelList:
                    panelList.append(row[2])
            for panel in panelList:
                data[panel] = {}
                for item in itemList:
                    data[panel][item] = {'count':0,'names':[],'description':''}
            for row in csvData[1:]:
                data[row[2]][row[0]]['count'] = data[row[2]][row[0]]['count'] + 1
                data[row[2]][row[0]]['names'].append(row[1])


        for i in list(data.keys()): 
            if i != 'cableData' and i != 'revisions':
                self.columnHeaders.append(i)
                if i == 'Loose and Not Mounted':
                    self.loosePanelPresent = True
        return data   

    def getUniqueItemNumbers(self,data):
        for panel in data:
            if panel != 'cableData' and panel != 'revisions':
                for item in data[panel]:
                    if item != 'description' and item not in self.uniqueItemNumbers:
                        self.uniqueItemNumbers.append(item)
        
        self.uniqueItemNumbers.sort(key=naturalSortKey)

    def buildInitialTable(self, data):
        dimensions = [len(self.uniqueItemNumbers),len(self.columnHeaders)]
        self.tableWidget.setColumnCount(dimensions[1])
        self.tableWidget.setRowCount(dimensions[0])
        self.tableWidget.setHorizontalHeaderLabels(self.columnHeaders)
        self.tableWidget.setVerticalHeaderLabels(self.uniqueItemNumbers)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setTabKeyNavigation(False)
        
        for panelIndex, panel in enumerate(self.columnHeaders):
            for itemIndex, item in enumerate(self.uniqueItemNumbers):
                if panel != 'Item Options':
                    if data[panel][item]['count'] != '1 Lot':
                        count = int(data[panel][item]['count'])
                    else:
                        count = '1 Lot'
                    cell = advancedCustomTableWidgetItem(self.signals, count=count,deviceNames=data[panel][item]['names'],coordinates=(itemIndex,panelIndex), note=data[panel][item]['note'])
                    cell.showDevices = self.tableWidget.cellWidget(itemIndex,0).deviceNames.isChecked()
                    
                    self.tableWidget.setCellWidget(itemIndex,panelIndex,cell)
                
                if panel == 'Item Options':
                    itemNumberCell = firstColumnWidget(self.signals,itemNo=item,coordinates=(itemIndex,panelIndex))
                    self.tableWidget.setCellWidget(itemIndex,panelIndex,itemNumberCell)

        self.tableWidget.itemSelectionChanged.connect(self.tableItemSelectionChanged)
        self.tableWidget.cellDoubleClicked.connect(self.showItemDescription)
        self.refreshCells()


        self.setCentralWidget(self.tableWidget)

    def showItemDescription(self):
        self.currentlySelectedCell = (self.tableWidget.currentRow(),self.tableWidget.currentColumn())
        description = QMessageBox()
        description.setWindowTitle(self.uniqueItemNumbers[self.tableWidget.currentRow()])
        description.setText(self.masterMatList[self.uniqueItemNumbers[self.tableWidget.currentRow()]])
        description.exec()

    def updateAddRowButton(self):
        self.addItemButton.setText('Add Item: '+self.dockItemSelect.currentText())
    
    def updateDeleteRowButton(self):
        if self.tableWidget.rowCount()>0:
            self.deleteRow.setText('Delete Item: '+self.tableWidget.cellWidget(self.currentlySelectedCell[0],0).text)

    def updateDeletePanelButton(self):
        self.deletePanelButton.setText('Delete Panel: '+self.columnHeaders[self.currentlySelectedCell[1]])

    def buildRightDock(self):
        self.removeDockWidget(self.dock)
        self.dockItemSelect = QComboBox()
        self.dockItemSelect.currentTextChanged.connect(self.updateAddRowButton)
        for item in self.masterMatList.keys():
            self.dockItemSelect.addItem(item)

        self.addItemButton = QPushButton('Add Item: 0',clicked=self.addItem)
        self.printButton = QPushButton('Save',clicked=self.export)
        #self.revisionButton = QPushButton('Add Revision Information',clicked=self.addRevisionInformation)
        self.deleteRow = QPushButton(f'Delete Item: ',clicked=self.deleteItem)
        self.addPanelButton = QPushButton('Add Panel',clicked=self.addPanel)
        self.deletePanelButton = QPushButton('Delete Panel', clicked=self.deletePanel)
        self.newPanelName = QLineEdit()
        self.newPanelName.setPlaceholderText('Panel Name')
        self.hintsButton = QPushButton('Hints',clicked=self.displayHints)
        self.renamePanelButton = QPushButton('Rename Panel',clicked=self.renamePanel)
        self.addLooseButton = QPushButton('Add "Loose and Not Mounted"',clicked=self.addLoose)
        self.cableDataWindowButton = QPushButton('Show Cable Window', clicked=self.showCableData)
        self.revisionDataWindowButton = QPushButton("Show Revision Data",clicked=self.showRevisionData)

        self.dockLayout = QFormLayout()
        self.dockLayout.addRow(self.dockItemSelect)
        self.dockLayout.addRow(self.addItemButton)
        self.dockLayout.addRow(self.deleteRow)
        self.dockLayout.addItem(QSpacerItem(50,50))
        self.dockLayout.addRow(self.newPanelName)
        self.dockLayout.addRow(self.addPanelButton)
        self.dockLayout.addRow(self.renamePanelButton)
        self.dockLayout.addRow(self.deletePanelButton)
        self.dockLayout.addRow(self.addLooseButton)
        self.dockLayout.addItem(QSpacerItem(50,50))
        self.dockLayout.addRow(self.cableDataWindowButton)
        self.dockLayout.addRow(self.revisionDataWindowButton)
        self.dockLayout.addItem(QSpacerItem(50,50))
        self.dockLayout.addRow(self.printButton)
        self.dockLayout.addItem(QSpacerItem(50,300))
        self.dockLayout.addRow(self.hintsButton)
        
        self.dockMenu = QWidget()
        self.dockMenu.setLayout(self.dockLayout)
        self.dock = QDockWidget('Menu')
        self.dock.setWidget(self.dockMenu)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock) 
    
    def addLoose(self):
        if not self.loosePanelPresent:
            self.columnHeaders.append('Loose and Not Mounted')
            self.tableWidget.insertColumn(self.tableWidget.columnCount())
            for row in range(self.tableWidget.rowCount()):
                cell = advancedCustomTableWidgetItem(self.signals,coordinates=(row,self.tableWidget.columnCount()-1))
                cell.oneLotSelected = self.tableWidget.cellWidget(row,0).oneLot.isChecked()
                cell.oneLot()
                cell.showDevices = self.tableWidget.cellWidget(row,0).deviceNames.isChecked()
                #print(cell.showDevices)
                self.tableWidget.setCellWidget(row,self.tableWidget.columnCount()-1,cell)
            self.tableWidget.setHorizontalHeaderLabels(self.columnHeaders)
            self.newPanelName.setText('')
            self.refreshCells()
            self.saved = False
            self.loosePanelPresent = True

    def displayHints(self):
        hints = QMessageBox()
        hints.setWindowTitle('Hints')
        hints.setText('Shortcuts:\n\'R\': Resize Cells to Fit Contents\n\'D\': Show Menu\n\'C\': Show Cable Data\n\'H\': Display Hints\nDouble-Click Cell: Show Item Description\nType: "<br/>" when entering data to force a new line')
        hints.exec()

    def deletePanel(self):
        if self.columnHeaders[self.currentlySelectedCell[1]] == 'Loose and Not Mounted':
            self.loosePanelPresent = False
        self.columnHeaders.remove(self.columnHeaders[self.currentlySelectedCell[1]])
        self.tableWidget.removeColumn(self.currentlySelectedCell[1])
        self.saved = False

    def tableItemSelectionChanged(self):
        self.currentlySelectedCell = (self.tableWidget.currentRow(),self.tableWidget.currentColumn())
        self.updateDeleteRowButton()
        self.updateDeletePanelButton()
        #self.buildRightDock()
        
    def addItem(self):
        if self.dockItemSelect.currentText() not in [self.tableWidget.cellWidget(i,0).text for i in range(self.tableWidget.rowCount())]:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            itemNumberCell = firstColumnWidget(signalClass=self.signals,itemNo=self.dockItemSelect.currentText(),coordinates=(self.tableWidget.rowCount()-1,0))
            #itemNumberCell.setTextAlignment(QtCore.Qt.AlignCenter)
            #itemNumberCell.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled) #Disables editing of the first column
            self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1,0,itemNumberCell)
            #for panelIndex, perPanelCount in enumerate(self.dockItemPanels):
            #print(len(self.dockItemPanels),self.tableWidget.columnCount())
            for panelIndex in range(self.tableWidget.columnCount()-1):
                #cell = customTableWidgetItem(perPanelCount.text())
                cell = advancedCustomTableWidgetItem(self.signals , coordinates=(self.tableWidget.rowCount()-1,panelIndex+1))
                #cell.currentTextChanged.connect(self.buildRightDock)
                self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1,panelIndex+1,cell)
            self.uniqueItemNumbers.append(self.dockItemSelect.currentText())
        self.tableWidget.setVerticalHeaderLabels(self.uniqueItemNumbers)
        self.refreshCells()
        self.saved = False

    def export(self):
        if self.newFile:
            self.matListFileName = QFileDialog.getSaveFileName(filter="*.json")[0]

            self.pdfFileName = self.matListFileName.split('.')[0]+'.pdf'
            self.newFile = False

        self.developOutputDictionary()
        self.saveJSONFile()
        self.makePDF()
        self.saved = True
        message = QMessageBox()
        directory = os.path.split(self.matListFileName)[0]
        message.setText(f'PDF and JSON saved in {directory}')
        message.exec()
        
    def developOutputDictionary(self):
        self.outputDictionary = {}
        for header in self.columnHeaders:
            if header != 'Item Options':
                self.outputDictionary[header] = {}
        for panel in self.outputDictionary:
            self.outputDictionary[panel]['description'] = ''
            for item in self.uniqueItemNumbers:
                row = self.uniqueItemNumbers.index(item)
                column = self.columnHeaders.index(panel)
                self.outputDictionary[panel][item] = {}
                if self.tableWidget.cellWidget(row,column).oneLotSelected:
                    self.outputDictionary[panel][item]['count'] = '1 Lot'
                else:
                    self.outputDictionary[panel][item]['count'] = self.tableWidget.cellWidget(row,column).countSelect.value()
                self.outputDictionary[panel][item]['names'] = [i.text() for i in self.tableWidget.cellWidget(row,column).deviceNames]
                self.outputDictionary[panel][item]['description'] = ''
                self.outputDictionary[panel][item]['note'] = self.tableWidget.cellWidget(row, column).note
                #if item[0] == '2' and len(item) >= 3: #Only for cables
                #    self.outputDictionary[panel][item]['cables'] = self.tableWidget.cellWidget(row,column).cableData
                #else:
                #    self.outputDictionary[panel][item]['cables'] = 'N/A'
        self.outputDictionary['cableData'] = self.cableData
        self.outputDictionary['revisions'] = self.revisionData
                    
    def saveJSONFile(self):
        self.developOutputDictionary()
        with open(self.matListFileName,'w') as outfile:
            json.dump(self.outputDictionary,outfile)

        '''Saves with form:
        {'|Panel|':{'description':'|panel description|','|item number|':{'count':'|count|','names':'|[names]|','description':'|item description|'}}}'''
    
    def makeMatlistTable(self):
        styleCustomCenterJustified = ParagraphStyle(name='BodyText', parent=getSampleStyleSheet()['BodyText'], spaceBefore=6, alignment=1, fontSize=8)
        styleCustomLeftJustified = ParagraphStyle(name='BodyText', parent=getSampleStyleSheet()['BodyText'], spaceBefore=6, alignment=0, fontSize=8)
        matlistTableData = [['' for i in range(self.tableWidget.columnCount()+2)] for j in range(self.tableWidget.rowCount()+3)]
        matlistTableData[0][0] = os.path.basename(self.matListFileName).split('.')[0] + " Material List"
        matlistTableData[1][2] = Paragraph('QUANTITY / DEVICE NAMES', styleCustomCenterJustified)
        matlistTableData[2][0] = Paragraph('ITEM NO.',styleCustomCenterJustified)
        matlistTableData[2][1] = Paragraph('EQUIPMENT DESCRIPTION',styleCustomCenterJustified)
        matlistTableData[2][2] = Paragraph('Total',styleCustomCenterJustified)
        #Fill Headers
        for panelIndex, panel in enumerate(self.columnHeaders[1:]):
            matlistTableData[2][panelIndex+3] = Paragraph(panel, styleCustomCenterJustified)
        #Fill Item Count and Names Cells
        for rowIndex in range(self.tableWidget.rowCount()):
            for columnIndex in range(1, self.tableWidget.columnCount()):
                if self.tableWidget.cellWidget(rowIndex,columnIndex).oneLotSelected:
                    matlistTableData[rowIndex+3][columnIndex+2] = Paragraph('1 Lot<br/>'+self.tableWidget.cellWidget(rowIndex,columnIndex).note,styleCustomCenterJustified)
                else:
                    matlistTableData[rowIndex+3][columnIndex+2] = Paragraph('<br/>'.join([str(self.tableWidget.cellWidget(rowIndex,columnIndex).countSelect.value()),'<br/>'.join([i.text() for i in self.tableWidget.cellWidget(rowIndex,columnIndex).deviceNames])])+self.tableWidget.cellWidget(rowIndex,columnIndex).note,styleCustomCenterJustified)
        #Fill Total Cells    
            if True in [self.tableWidget.cellWidget(rowIndex, columnIndex).oneLotSelected for columnIndex in range(1,self.tableWidget.columnCount())]:
                matlistTableData[rowIndex+3][2] = Paragraph('1 Lot',styleCustomCenterJustified)
            else:  
                matlistTableData[rowIndex+3][2] = Paragraph(str(sum([self.tableWidget.cellWidget(rowIndex, columnIndex).countSelect.value() for columnIndex in range(1,self.tableWidget.columnCount())])), styleCustomCenterJustified)
        #Fill Item Numbers and Descriptions
            matlistTableData[rowIndex+3][0] = Paragraph(self.tableWidget.cellWidget(rowIndex, 0).text, styleCustomCenterJustified)
            matlistTableData[rowIndex+3][1] = Paragraph(self.masterMatList[self.tableWidget.cellWidget(rowIndex, 0).text], styleCustomLeftJustified)
        matlistColumnWidths = [50,200,50]
        for i in matlistTableData[0][2:]:
            matlistColumnWidths.append((self.pageWidth*inch-250)/len(matlistTableData[0][2:]))
        matlistTable = Table(matlistTableData, colWidths=matlistColumnWidths, repeatRows=3, style=[
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('SPAN', (0,0), (-1, 0)),
            ('SPAN', (0,1), (1, 1)),
            ('SPAN', (2,1), (-1, 1)),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'TOP')])
        return matlistTable

    def makeCableTable(self):
        styleCustomCenterJustified = ParagraphStyle(name='BodyText', parent=getSampleStyleSheet()['BodyText'], spaceBefore=6, alignment=1, fontSize=8)
        #cableTableData = [[Paragraph(key.upper(), styleCustomCenterJustified) for key in list(self.cableData.keys())]]
        cableTableData = [['ITEM NO.', 'CABLE TYPE', 'ESTIMATED LENGTH', 'FROM', '', '', '', 'TO', '', '', ''],['', '', '', 'RELAY TYPE', 'DEVICE NUMBER', 'PORT', 'PANEL NUMBER', 'RELAY TYPE', 'DEVICE NUMBER', 'PORT', 'PANEL NUMBER']]
        for rowIndex in range(len(cableTableData)):
            for colIndex in range(len(cableTableData[0])):
                cableTableData[rowIndex][colIndex] = Paragraph(cableTableData[rowIndex][colIndex], styleCustomCenterJustified)
        colWidths=[(self.pageWidth*inch-50)/11 for i in cableTableData[0]]
        colWidths[2] = colWidths[2] + 10
        for rowIndex in range(len(list(self.cableData['Item No.']))):
            row = [Paragraph(str(self.cableData[key][rowIndex]), styleCustomCenterJustified) for key in self.cableData.keys()]
            cableTableData.append(row)
        cableTable = Table(cableTableData, colWidths=colWidths, repeatRows=2, style=[('GRID',(0,0),(-1,-1),0.5,colors.black),
                                                                                        ('SPAN', (0,0), (0,1)),
                                                                                        ('SPAN', (1,0), (1,1)),
                                                                                        ('SPAN', (2,0), (2,1)),
                                                                                        ('SPAN', (3,0), (6,0)),
                                                                                        ('SPAN', (7,0), (10,0))])
        return cableTable

    def makeRevisionTable(self):
        styleCustomCenterJustified = ParagraphStyle(name='BodyText', parent=getSampleStyleSheet()['BodyText'], spaceBefore=6, alignment=1, fontSize=8)
        revisionTableData = [[Paragraph(key.upper(), styleCustomCenterJustified) for key in list(self.revisionData.keys())]]
        for rowIndex in range(len(list(self.revisionData['date']))):
            row = [Paragraph(str(self.revisionData[key][rowIndex]), styleCustomCenterJustified) for key in self.revisionData.keys()]
            revisionTableData.append(row)
        revisionTable = Table(revisionTableData, colWidths=[50, 50, 400], repeatRows=2, style=[  ('GRID',(0,0),(-1,-1),0.5,colors.black),],hAlign='LEFT')
        return revisionTable

    def makePDF(self):
        self.pageWidth = 8.5
        self.pageHeight = 11
        if len(self.columnHeaders) > 5:
            self.pageWidth = 11
            self.pageHeight = 8.5
        if len(self.columnHeaders) > 9:
            self.pageWidth = 17
            self.pageHeight = 11
        matlistTable = self.makeMatlistTable()
        cableTable = self.makeCableTable()
        revisionTable = self.makeRevisionTable()
        
        pagesize = (self.pageWidth * inch, self.pageHeight * inch)
        doc = SimpleDocTemplate(self.pdfFileName, pagesize=pagesize)
        doc.__setattr__('topMargin', 0.25*inch)
        doc.__setattr__('leftMargin', 0.25*inch)
        doc.__setattr__('rightMargin', 0.25*inch)
        doc.__setattr__('bottomMargin', 0.25*inch)
        elements = []
        #elements.append(Paragraph("Title"))
        #elements.append(Paragraph("Material List"))
        elements.append(matlistTable)
        elements.append(PageBreak())
        #elements.append(Paragraph("Cable List"))
        elements.append(cableTable)
        elements.append(PageBreak())
        #elements.append(Paragraph("Revisions"))
        elements.append(revisionTable)
        doc.build(elements, canvasmaker=NumberedPageCanvas)

    def deleteItem(self):
        if len(self.uniqueItemNumbers) > 0:
            self.uniqueItemNumbers.remove(self.tableWidget.cellWidget(self.currentlySelectedCell[0],0).text)
            self.tableWidget.removeRow(self.currentlySelectedCell[0])
        if len(self.uniqueItemNumbers) > 0:
            self.deleteRow.setText(f'Delete Item: {self.tableWidget.cellWidget(self.currentlySelectedCell[0],0).text}')
        else:
            self.deleteRow.setText(f'')
        self.saved = False

class advancedCustomTableWidgetItem(QWidget):
    def __init__(self,signalClass, count=0,deviceNames=[], coordinates=(), note = ''):
        super(advancedCustomTableWidgetItem,self).__init__()
        self.signals=signalClass
        self.signals.enableDeviceNames.connect(self.enableDeviceNames)
        self.signals.disableDeviceNames.connect(self.disableDeviceNames)
        self.signals.enableOneLot.connect(self.enableOneLot)
        self.signals.disableOneLot.connect(self.disableOneLot)
        self.coordinates = coordinates
        self.layout1 = QGridLayout()
        self.countSelect = QSpinBox()
        self.countSelect.setMaximum(999)
        self.countSelect.valueChanged.connect(self.spinBoxChanged)
        self.oneLotSelected = False
        self.showDevices = False
        self.note = note

        #List of dictionaries for cable data
        #One dictionary entry per cable
        #Add button to show new window with table that has one row per cable in cell
        # self.cableData = [{"From Relay Type":'',
        #                   "From Device Number":'',
        #                   "From Port":'',
        #                   "From Panel Number":'',
        #                   "To Relay Type":'',
        #                   "To Device Number":'',
        #                   "To Port":'',
        #                   "To Panel Number":'',
        #                   'Estimated Length':''}]
        

        self.deviceNames = [QLineEdit() for i in deviceNames]
        if len(self.deviceNames)>0:
            self.signals.checkDeviceNames.emit(coordinates[0])
        for i in range(len(deviceNames)):
            self.deviceNames[i].setText(deviceNames[i])
            self.deviceNames[i].editingFinished.connect(self.lineEditFinished)




        if count != '1 Lot':
            self.countSelect.setValue(count)
        else:
            self.countSelect.setValue(0)
            self.countSelect.setDisabled(True)
            self.oneLotSelected = True
            self.signals.checkOneLot.emit(coordinates[0])

        

        self.countSelect.valueChanged.connect(self.updateDeviceNameSlots)


        if len(self.deviceNames) != 0:
            self.showDevices = True

        self.layout1 = QGridLayout()
        self.layout1.addWidget(self.countSelect,0,0)
        for i in range(len(self.deviceNames)):
            self.layout1.addWidget(self.deviceNames[i],i+2,0,1,2)
        self.setLayout(self.layout1)

        self.updateDeviceNameSlots()

    def spinBoxChanged(self):
        self.signals.needsSaved.emit(True)

    def lineEditFinished(self):
        self.signals.needsSaved.emit(True)

    def disableDeviceNames(self,coordinates):
        #print(coordinates)
        if coordinates == self.coordinates[0]:
            self.showDevices = False
        self.updateDeviceNameSlots()
        
    def disableOneLot(self,coordinates):
        #print(coordinates)
        if coordinates == self.coordinates[0]:
            self.oneLotSelected = False
        self.oneLot()
        
    def enableDeviceNames(self,coordinates):
        #print(coordinates)
        if coordinates == self.coordinates[0]:
            self.showDevices = True
            self.countSelect.setValue(0)
        self.updateDeviceNameSlots()
        
    def enableOneLot(self,coordinates):
        #print(coordinates)
        if coordinates == self.coordinates[0]:
            self.oneLotSelected = True
        self.oneLot()
        
    def updateDeviceNameSlots(self):
        if self.showDevices == True:
            while self.countSelect.value() != len(self.deviceNames):
                if self.countSelect.value() > len(self.deviceNames):
                    self.addDeviceNameSlot()
                if self.countSelect.value() < len(self.deviceNames):
                    self.removeDeviceNameSlot()    
        else:
            while len(self.deviceNames) > 0:
                self.removeDeviceNameSlot()
        
        self.signals.refreshCellDimensions.emit()

    def toggleDevices(self):
        if self.showDevices == True:
            self.countSelect.setValue(0)
        self.updateDeviceNameSlots()

    def addDeviceNameSlot(self):
        self.deviceNames.append(QLineEdit())
        self.layout1.addWidget(self.deviceNames[-1],len(self.deviceNames)+2,0,1,2)
        if self.oneLotSelected:
            self.countSelect.setValue(0)
            self.deviceNames = []
        self.signals.needsSaved.emit(True)

    def removeDeviceNameSlot(self):
        self.layout1.removeWidget(self.deviceNames[-1])
        self.deviceNames.pop()
        self.signals.needsSaved.emit(True)
        
    def oneLot(self):
        if self.oneLotSelected:
            self.countSelect.setDisabled(True)
            for i in reversed(range(len(self.deviceNames))):
                self.layout1.removeWidget(self.deviceNames[i])
            self.countSelect.setValue(0)
            self.updateDeviceNameSlots()
        else:
            self.countSelect.setDisabled(False)

class firstColumnWidget(QWidget):
    def __init__(self,signalClass, deviceNames = False, oneLot = False, itemNo = '', coordinates = (0,0)):
        super(firstColumnWidget,self).__init__()
        self.signals = signalClass
        self.deviceNames = QCheckBox()
        self.oneLot = QCheckBox()
        self.deviceNames.setChecked(deviceNames)
        self.oneLot.setChecked(oneLot)
        self.deviceNames.setText('Show Device Names')
        self.oneLot.setText('1 Lot')
        self.deviceNames.clicked.connect(self.enableDeviceNames)
        self.oneLot.clicked.connect(self.enableOneLot)
        self.layout1 = QFormLayout()
        self.layout1.addRow(self.deviceNames)
        self.layout1.addRow(self.oneLot)
        self.setLayout(self.layout1)
        self.text = itemNo
        self.coordinates = coordinates
        self.signals.checkOneLot.connect(self.checkOneLot)
        self.signals.checkDeviceNames.connect(self.checkDeviceNames)

    def enableDeviceNames(self):
        if self.deviceNames.isChecked():
            self.signals.enableDeviceNames.emit(self.coordinates[0])
        else:
            self.signals.disableDeviceNames.emit(self.coordinates[0])
        self.signals.needsSaved.emit(True)

    def enableOneLot(self):
        if self.oneLot.isChecked():
            self.signals.enableOneLot.emit(self.coordinates[0])
            self.deviceNames.setDisabled(True)
            self.deviceNames.setChecked(False)
        else:
            self.signals.disableOneLot.emit(self.coordinates[0])
            self.deviceNames.setDisabled(False)
        self.signals.needsSaved.emit(True)

    def checkOneLot(self,row):
        if row == self.coordinates[0]:
            self.oneLot.setChecked(True)
        self.enableOneLot()

    def checkDeviceNames(self,row):
        if row == self.coordinates[0]:
            self.deviceNames.setChecked(True)
        
class signalClass(QWidget):
    refreshCellDimensions = QtCore.pyqtSignal()  
    enableDeviceNames = QtCore.pyqtSignal(int)
    enableOneLot = QtCore.pyqtSignal(int)
    disableDeviceNames = QtCore.pyqtSignal(int)
    disableOneLot = QtCore.pyqtSignal(int)
    checkDeviceNames = QtCore.pyqtSignal(int)
    checkOneLot = QtCore.pyqtSignal(int)
    needsSaved = QtCore.pyqtSignal(bool)
    saveCableData = QtCore.pyqtSignal()
    saveRevisionData = QtCore.pyqtSignal()


#--------------------------------------------------------PDF SECTION----------------------------------------------------------------
class NumberedPageCanvas(Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    http://www.blog.pythonlibrary.org/2013/08/12/reportlab-how-to-add-page-numbers/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            self.draw_rev_number()
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 8)
        self.drawRightString(10.75 * inch, 0.25 * inch, page)
        
    def draw_rev_number(self):
        self.setFont("Helvetica", 8)
        self.drawString(0.25 * inch, 0.25 * inch, 'Rev. 0')

if  __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('json/MasterList.json') as file:
        masterList = json.load(file)
    signals = signalClass()
    application = mainProgram(signals,masterMaterialList=masterList)
    application.show()
    sys.exit(app.exec())

