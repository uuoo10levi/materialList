#NOT RELEASED FOR USE
import sys
from screeninfo import get_monitors
from PyQt5 import QtCore
from PyQt5.QtWidgets import QRadioButton, QAbstractScrollArea, QSpinBox, QCheckBox, QInputDialog, QLabel, QGridLayout, QComboBox, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QSpacerItem
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas


class mainProgram(QMainWindow):
    def __init__(self, signalClass, matListFileName = 'projectMatlist.json', masterMaterialList = {'':''}):
        super(mainProgram, self).__init__()
        self.signals = signalClass
        self.signals.signal1.connect(self.resizeCell)

        self.startupMessage = startupMessage()
        self.newFile = self.startupMessage.newFile

        self.matListFileName = matListFileName
        self.pdfFileName = self.matListFileName.split('.')[0]+'.pdf'

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
        self.tableHeaders = ['Item No.']
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
        self.deleteButton = QPushButton()


        self.currentlySelectedCell = [0,0]
        self.uniqueItemNumbers = []
        self.masterMatList = masterMaterialList
        '''Defines a dictionary of form {"|Item No.|":"|Description|"}'''

        #Initial Setup
        self.buildMainWindow()
        if self.newFile:
            data = self.buildNewMatlist()
        else:
            data = self.importData(self.matListFileName)
        self.getUniqueItemNumbers(data)
        self.buildInitialTable(data)
        self.buildRightDock()

        #Main Loop - Contains no code, but comments describe event functionalities
        self.mainProgramLoop()

    def resizeCell(self):
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
        self.setWindowTitle('Add Material to Contract')

    def addPanel(self):
        panel, done = QInputDialog.getText(self, 'New Panel', 'Enter Name for New Panel:')
        self.tableHeaders.append(panel)
        self.tableWidget.insertColumn(self.tableWidget.columnCount())
        for row in range(self.tableWidget.rowCount()):
            cell = advancedCustomTableWidgetItem(self.signals)
            #cell.cellDeviceNames = []
            #cell.currentTextChanged.connect(self.buildRightDock)
            self.tableWidget.setCellWidget(row,self.tableWidget.columnCount()-1,cell)
        message = QDialog()
        layout = QFormLayout()
        messageText = QLabel()
        messageText.setText('Panel Name will Display Properly on Program Reboot')
        layout.addWidget(messageText)
        message.setLayout(layout)
        message.exec()
        self.saveJSONFile()

    def buildNewMatlist(self):
        self.matListFileName = 'newFile.json'
        self.pdfFileName = self.matListFileName.split('.')[0]+'.pdf'

        #if type(input) == type(dict()):
        data = {"Panel":{"item":{"count":'0',"names":[],"description":""}}}
        for i in list(data.keys()):
            self.tableHeaders.append(i)

        return data
    
    def importData(self, input):
        '''If input is a string representing a path to a json file, import data from the json file\n
        If input is a dictionary, import data from the dictionary'''
        #if type(input) == type(str()) and input != 'new':
        with open(input) as jsonFile:
            data = json.load(jsonFile)
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
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setTabKeyNavigation(False)
        
        for panelIndex, panel in enumerate(self.tableHeaders):
            for itemIndex, item in enumerate(self.uniqueItemNumbers):
                if panel != 'Item No.':
                    #cell = customTableWidgetItem(data[panel][item]['count'])
                    if data[panel][item]['count'] != '1 Lot':
                        count = int(data[panel][item]['count'])
                    else:
                        count = '1 Lot'
                    cell = advancedCustomTableWidgetItem(self.signals, count=count,deviceNames=data[panel][item]['names'])
                    self.tableWidget.setCellWidget(itemIndex,panelIndex,cell)
                
                if panel == 'Item No.':
                    itemNumberCell = QTableWidgetItem(item)
                    itemNumberCell.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled) #Disables editing of the first column
                    self.tableWidget.setItem(itemIndex,panelIndex,itemNumberCell)

        self.tableWidget.itemChanged.connect(self.tableItemChanged)
        self.tableWidget.itemSelectionChanged.connect(self.tableItemSelectionChanged)
        self.resizeCell()

        self.setCentralWidget(self.tableWidget)

    def buildRightDock(self):
        self.removeDockWidget(self.dock)
        self.dockItemSelect = QComboBox()
        for item in self.masterMatList.keys():
            self.dockItemSelect.addItem(item)

        # self.dockItemPanels = []
        # for panel in self.tableHeaders[1:]:
        #     dockItemCountEntry = QLineEdit()
        #     dockItemCountEntry.setPlaceholderText(panel)
        #     self.dockItemPanels.append(dockItemCountEntry)

        self.addItemButton = QPushButton('Add Entry',clicked=self.addItem)
        self.printButton = QPushButton('Print Data to Console',clicked=self.printDataToConsole)
        self.deleteButton = QPushButton(f'Delete Row: {self.currentlySelectedCell[0]+1}',clicked=self.deleteItem)
        self.addPanelButton = QPushButton('Add Panel',clicked=self.addPanel)
        self.deletePanelButton = QPushButton('Delete Panel', clicked=self.deletePanel)

        #self.deviceNameSlots = 0
        #if self.currentlySelectedCell[1] >= 1 and self.tableWidget.cellWidget(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).currentText() != '1 Lot':
        #   self.deviceNameSlots = int(self.tableWidget.cellWidget(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).currentText())
        #if self.deviceNameSlots > 15:
        #    self.deviceNameSlots = 15
            
        
        #self.deviceNames = [QLineEdit() for i in range(self.deviceNameSlots)]
        #for i in range(len(self.deviceNames)):
        #    self.deviceNames[i].editingFinished.connect(self.updateDeviceNames)


        #for i in range(len(self.deviceNames)):
        #    self.deviceNames[i].setPlaceholderText(f'Device {i+1} Name:')
        #    try:
        #        self.deviceNames[i].setText(self.tableWidget.cellWidget(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).cellDeviceNames[i])
        #    except:
        #        pass


        self.dockLayout = QFormLayout()
        self.dockLayout.addRow(self.dockItemSelect)
        # for i in self.dockItemPanels:
        #     self.dockLayout.addRow(i)
        self.dockLayout.addRow(self.addItemButton)
        #for i in self.deviceNames:
        #    self.dockLayout.addRow(i)
        self.dockLayout.addRow(self.addPanelButton)
        self.dockLayout.addRow(self.deletePanelButton)
        self.dockLayout.addRow(self.deleteButton)
        self.dockLayout.addRow(self.printButton)


        self.dockMenu = QWidget()
        self.dockMenu.setLayout(self.dockLayout)


        self.dock = QDockWidget('Menu')
        self.dock.setWidget(self.dockMenu)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock) 

    def deletePanel(self):
        self.tableWidget.removeColumn(self.currentlySelectedCell[1])

    def tableItemSelectionChanged(self):
        self.currentlySelectedCell = (self.tableWidget.currentRow(),self.tableWidget.currentColumn())
        self.buildRightDock()
        
    def tableItemChanged(self):
        pass

    def addItem(self):
        if self.dockItemSelect.currentText() not in [self.tableWidget.item(i,0).text() for i in range(self.tableWidget.rowCount())]:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            itemNumberCell = QTableWidgetItem(self.dockItemSelect.currentText())
            itemNumberCell.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled) #Disables editing of the first column
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,0,itemNumberCell)
            #for panelIndex, perPanelCount in enumerate(self.dockItemPanels):
            #print(len(self.dockItemPanels),self.tableWidget.columnCount())
            for panelIndex in range(self.tableWidget.columnCount()-1):
                #cell = customTableWidgetItem(perPanelCount.text())
                cell = advancedCustomTableWidgetItem(self.signals)
                #cell.currentTextChanged.connect(self.buildRightDock)
                self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1,panelIndex+1,cell)
            self.uniqueItemNumbers.append(self.dockItemSelect.currentText())

    def printDataToConsole(self):
        self.developOutputDictionary()
        self.saveJSONFile()
        self.makePDF()
        pass

    def updateDeviceNames(self):
        self.tableWidget.cellWidget(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).cellDeviceNames = [i.text() for i in self.deviceNames]

    def developOutputDictionary(self):
        self.outputDictionary = {}
        for header in self.tableHeaders:
            if header != 'Item No.':
                self.outputDictionary[header] = {}
        for panel in self.outputDictionary:
            self.outputDictionary[panel]['description'] = ''
            for item in self.uniqueItemNumbers:
                row = self.uniqueItemNumbers.index(item)
                column = self.tableHeaders.index(panel)
                self.outputDictionary[panel][item] = {}
                if self.tableWidget.cellWidget(row,column).oneLotCheckBox.isChecked():
                    self.outputDictionary[panel][item]['count'] = '1 Lot'
                else:
                    self.outputDictionary[panel][item]['count'] = self.tableWidget.cellWidget(row,column).countSelect.value()
                self.outputDictionary[panel][item]['names'] = [i.text() for i in self.tableWidget.cellWidget(row,column).deviceNames]
                self.outputDictionary[panel][item]['description'] = ''
                    
    def saveJSONFile(self):
        self.developOutputDictionary()
        with open(self.matListFileName,'w') as outfile:
            json.dump(self.outputDictionary,outfile)

        '''Saves with form:
        {'|Panel|':{'description':'|panel description|','|item number|':{'count':'|count|','names':'|[names]|','description':'|item description|'}}}'''
    
    def makePDF(self):
        headings = [self.matListFileName]
        headings.append('')
        headings.append('')
        headings.append('Item No.')
        headings.append('Description')
        headings.append('Total')
        for i in self.tableHeaders[1:]:
            headings.append(i)

        grid = [['' for j in range(self.tableWidget.columnCount())] for i in range(self.tableWidget.rowCount())]

        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                if column != 0:
                    if not self.tableWidget.cellWidget(row,column).oneLotCheckBox.isChecked():
                        grid[row][column] = [self.tableWidget.cellWidget(row,column).countSelect.value(),[i.text() for i in self.tableWidget.cellWidget(row,column).deviceNames]]
                    else:
                        grid[row][column] = '1 Lot'
                if column == 0:
                    grid[row][column] = self.tableWidget.item(row,column).text()

        self.pdf = pdf(masterMatList = self.masterMatList,grid=grid,headings = headings,name=self.pdfFileName)
        self.pdf.exportPDF()

    def mainProgramLoop(self):
        #Functions attached to events or buttons:
        #tableItemSelectionChanged()
        #tableItemChanged()
        #addItem()
        #printDataToConsole()
        pass

    def deleteItem(self):
        self.uniqueItemNumbers.remove(self.tableWidget.item(self.currentlySelectedCell[0],0).text())
        self.tableWidget.removeRow(self.currentlySelectedCell[0])

class advancedCustomTableWidgetItem(QWidget):
    def __init__(self,signalClass, count=0,deviceNames=[]):
        super(advancedCustomTableWidgetItem,self).__init__()
        self.signals=signalClass

        self.layout1 = QGridLayout()
        self.countSelect = QSpinBox()
        self.countSelect.setMaximum(999)
        self.oneLotCheckBox = QCheckBox()
        self.showDevicesCheckBox = QCheckBox()
        #self.widget = QWidget()
        self.oneLotSelected = False

        if count != '1 Lot':
            self.countSelect.setValue(count)
        else:
            self.countSelect.setValue(0)
            self.oneLotCheckBox.setChecked(True)
            self.countSelect.setDisabled(True)
            self.showDevicesCheckBox.setDisabled(True)
        self.deviceNames = [QLineEdit() for i in deviceNames]
        for i in range(len(deviceNames)):
            self.deviceNames[i].setText(deviceNames[i])
        
        for index in range(len(self.deviceNames)):
            self.deviceNames[index].setText(deviceNames[index])

        self.countSelect.valueChanged.connect(self.updateDeviceNameSlots)
        self.oneLotCheckBox.clicked.connect(self.oneLot)
        self.oneLotCheckBox.setText('1 LOT')
        self.showDevicesCheckBox.setText('Show Device Names')
        if len(self.deviceNames) != 0:
            self.showDevicesCheckBox.setChecked(True)
        self.showDevicesCheckBox.stateChanged.connect(self.toggleDevices)

        self.layout1 = QGridLayout()
        self.layout1.addWidget(self.countSelect,0,0)
        self.layout1.addWidget(self.oneLotCheckBox,0,1)
        self.layout1.addWidget(self.showDevicesCheckBox,1,1)
        for i in range(len(self.deviceNames)):
            self.layout1.addWidget(self.deviceNames[i],i+2,0,1,2)
        self.setLayout(self.layout1)

        self.updateDeviceNameSlots()

    def updateDeviceNameSlots(self):
        if self.showDevicesCheckBox.isChecked():
            while self.countSelect.value() != len(self.deviceNames):
                if self.countSelect.value() > len(self.deviceNames):
                    self.addDeviceNameSlot()
                if self.countSelect.value() < len(self.deviceNames):
                    self.removeDeviceNameSlot()    
        else:
            while len(self.deviceNames) > 0:
                self.removeDeviceNameSlot()
        
        self.signals.signal1.emit()

    def toggleDevices(self):
        if self.showDevicesCheckBox.isChecked():
            self.countSelect.setValue(0)
        self.updateDeviceNameSlots()


    def addDeviceNameSlot(self):
        self.deviceNames.append(QLineEdit())
        self.layout1.addWidget(self.deviceNames[-1],len(self.deviceNames)+2,0,1,2)
        if self.oneLotSelected:
            self.countSelect.setValue(0)
            self.deviceNames = []

    def removeDeviceNameSlot(self):
        self.layout1.removeWidget(self.deviceNames[-1])
        self.deviceNames.pop()
        

    def oneLot(self):
        self.oneLotSelected = self.oneLotCheckBox.isChecked()
        if self.oneLotSelected:
            self.countSelect.setDisabled(True)
            self.showDevicesCheckBox.setChecked(False)
            self.showDevicesCheckBox.setDisabled(True)
            for i in reversed(range(len(self.deviceNames))):
                self.layout1.removeWidget(self.deviceNames[i])
            self.countSelect.setValue(0)
            self.updateDeviceNameSlots()
        else:
            self.countSelect.setDisabled(False)
            self.showDevicesCheckBox.setDisabled(False)

class startupMessage(QWidget):
    def __init__(self):
        self.newFile = False
        self.newFileDialog = QDialog()
        self.newFileDialog.setWindowTitle('New Material List?')
        self.newFileDialog.setMinimumSize(400,50)
        self.newFileDialogLayout = QGridLayout()
        self.newFileDialogMessage = QLabel("Create New Material List?")
        self.newFileRadioButtonYes = QRadioButton()
        self.newFileRadioButtonYes.setText('New Material List')
        self.newFileRadioButtonNo = QRadioButton()
        self.newFileRadioButtonNo.setText('Select Existing Material List')
        self.newFileDialogAccept = QPushButton('Enter')
        self.newFileDialogAccept.clicked.connect(self.newFileDialog.close)
        self.newFileDialogLayout.addWidget(self.newFileDialogMessage,0,0)
        self.newFileDialogLayout.addWidget(self.newFileRadioButtonYes,1,0)
        self.newFileDialogLayout.addWidget(self.newFileRadioButtonNo,1,1)
        self.newFileDialogLayout.addWidget(self.newFileDialogAccept)
        self.newFileDialog.setLayout(self.newFileDialogLayout)
        

        self.newFileDialog.exec()
        self.newFile = self.newFileRadioButtonYes.isChecked()

class signalClass(QWidget):
    signal1 = QtCore.pyqtSignal()  

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

class pdf:
    def __init__(self, masterMatList = {}, grid=[], headings=[], name = '_.pdf', pageWidth = 8.5, pageHeight = 11):
        #print(grid)
        self.styleSheet = getSampleStyleSheet()
        self.pagesize = (pageHeight * inch, pageWidth * inch)
        self.styleCustomCenterJustified = ParagraphStyle(name='BodyText', parent=self.styleSheet['BodyText'], spaceBefore=6, alignment=1, fontSize=8)
        self.styleCustomLeftJustified = ParagraphStyle(name='BodyText', parent=self.styleSheet['BodyText'], spaceBefore=6, alignment=0, fontSize=8)
        self.doc = SimpleDocTemplate(name, pagesize=self.pagesize)
        self.doc.__setattr__('topMargin', 0.25*inch)
        self.doc.__setattr__('leftMargin', 0.25*inch)
        self.doc.__setattr__('rightMargin', 0.25*inch)
        self.doc.__setattr__('bottomMargin', 0.25*inch)
        
        

        tableData = [['' for i in range(len(grid[0])+2)] for j in range(len(grid)+3)]
        tableData[0][0] = headings[0]
        tableData[2][0] = headings[3]
        tableData[2][1] = headings[4]
        tableData[2][2] = 'Total'
        
        for index, heading in enumerate(headings[5:]):
            tableData[2][index+2] = heading

        #Item numbers, and per panel counts/device names
        for rowIndex, row in enumerate(grid):
            for columnIndex, cell in enumerate(row):
                if columnIndex != 0:
                    if cell != '1 Lot':
                        tempCell = str(cell[0])
                        for i in cell[1]:
                            tempCell = tempCell + '<br/>' + i
                    else:
                        tempCell = '1 Lot'
                    tableData[rowIndex+3][columnIndex+2] = tempCell
                if columnIndex == 0:
                    tableData[rowIndex+3][columnIndex] = cell
        #Descriptions
        for rowIndex, row in enumerate(tableData):
            if rowIndex > 2:
                tableData[rowIndex][1] = masterMatList[row[0]]
        
        #Total column
        for rowIndex, row in enumerate(grid):
            if '1 Lot' not in [i[0] for i in grid[rowIndex][1:]]:
                tableData[rowIndex+3][2] = sum([int(i[0]) for i in grid[rowIndex][1:]])
            else:
                tableData[rowIndex+3][2] = '1 Lot'

        
        
        self.elements = []
        # headings = ['Document Title','Item Number', 'Description', 'Total', 'Panel 1', 'Panel 2', 'Panel 3', etc]
        width = pageWidth*inch
        colWidths = [50,100,50]
        for i in tableData[0][3:]:
            colWidths.append((width-200)/len(tableData[0][3:]))


        for i in range(len(tableData)):
            for j in range(len(tableData[i])):
                if j != 1:
                    tableData[i][j] = Paragraph(str(tableData[i][j]), self.styleCustomCenterJustified)
                
        for i in range(len(tableData)):
            if i > 2:
                tableData[i][1] = Paragraph(str(tableData[i][1]), self.styleCustomLeftJustified)

        self.pdftable = Table(tableData, colWidths=colWidths, repeatRows=3, style=[
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('SPAN', (0,0), (-1, 0)),
            ('SPAN', (0,1), (1, 1)),
            ('SPAN', (2,1), (-1, 1)),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'TOP')]
                              )
        self.elements.append(self.pdftable)

    def exportPDF(self):
        self.doc.build(self.elements, canvasmaker=NumberedPageCanvas)

if  __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('json/MasterList.json') as file:
        masterList = json.load(file)
    signals = signalClass()
    application = mainProgram(signals,masterMaterialList=masterList)
    application.show()
    sys.exit(app.exec())
