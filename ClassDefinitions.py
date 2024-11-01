import sys
from screeninfo import get_monitors
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem
import json

class mainProgram(QMainWindow):
    def __init__(self, tableHeaders = [''], masterMaterialList = {'':''}):
        super(mainProgram, self).__init__()
        
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
        self.itemSelectComboBoxes = [QComboBox()] 
        '''Defines Drop-Down-Select Boxes that are slotted into the first column for item number\n
        Length should always equal the number of rows in self.tableWidget'''

        self.dock = QDockWidget('Menu')
        '''Defines right-side dock'''
        self.dockItemPanels = [QLineEdit()]
        '''Defines One Text box per panel to allow for new row addition'''
        self.dockMenu = QWidget()
        '''Defines widget to be added to right-side dock'''
        self.dockLayout = QFormLayout()
        '''Defines layout for widget on right-side dock'''
        self.dockItemSelect = QComboBox()
        '''Defines drop-down-select to be placed at top of right-side dock'''
        self.addButton = QPushButton()
        '''Defines button on right-side dock that makes new entry from right-side dock data'''
        self.deviceNames = [QLineEdit()]
        '''Defines text boxes on right-side dock used to enter individual device names'''
        self.spacer = QSpacerItem(0,0)
        '''Defines space between the add section of the right-side dock and the rest of the right-side dock'''
        self.printButton = QPushButton()
        '''Defines button to print the current table to the console'''
        self.currentlySelectedCell = (0,0)
        '''Defines coordinates for most recently selected cell'''

        self.tableHeaders = tableHeaders
        '''Defines headers for the main table \n
        Should be provided upon instantiation of the mainProgram object'''
        self.data = [["" for i in self.tableHeaders]]
        '''Defines the data that fills the table \n
        Should be altered to reflect changes to the table or additional rows made by the user'''
        self.availableItemNumbers = list(masterMaterialList.keys())
        '''Defines item numbers that the user can select from when adding a row\n
        Should be read in from the master database json file'''
        self.panels = list(self.tableHeaders[1:])
        '''Defines a clone of self.tableHeaders, but without the first 'Item Number' value'''

        self.importData()


        self.buildMainWindow()
        self.buildTable()

        
        
    def buildMainWindow(self):
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xShift = int(self.monitorXSize*.25)
        self.yShift = int(self.monitorYSize*.25)
        self.xSize = int(self.monitorXSize/2)
        self.ySize = int(self.monitorYSize/2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Material to Contract')

    def buildTable(self):
        #buildTable-A  (general size/shape)
        self.tableWidget = QTableWidget()                                   #Initialize table widget
        self.tableWidget.setColumnCount(len(self.data[0]))                  #Set table column count
        for i in range(len(self.data[0])):                                  #Iterate over each column
            self.tableWidget.setColumnWidth(i,200)                          #Set width of each column
        self.tableWidget.setRowCount(len(self.data))                        #Set table row count
        self.tableWidget.setHorizontalHeaderLabels(self.tableHeaders)       #Sets table headers
        self.tableWidget.itemChanged.connect(self.recordTableChange)        #Defines function to run when a table item is changed (save all table changes to self.data)
        self.tableWidget.itemSelectionChanged.connect(self.refreshRightDock)         #Defines function to run when a table item is clicked (update right-side dock to show deviceNames input boxes)
        

        #buildTable-B (combo boxes)
        self.itemSelectComboBoxes = []                                      #Defines list to store first column (device number) drop-down-select object
        for i in range(len(self.data)):                                     #Iterate over each row in data
            self.itemSelectComboBoxes.append(QComboBox())                   #Add drop-down-select object to list
            for j in self.availableItemNumbers:                             #Iterate over all available item numbers
                self.itemSelectComboBoxes[i].addItem(j)                     #Add all available item numbers to drop-down-select object's options
            comboBoxOptions = [self.itemSelectComboBoxes[i].itemText(j) for j in range(self.itemSelectComboBoxes[i].count())]
            self.itemSelectComboBoxes[i].setCurrentIndex(comboBoxOptions.index(self.data[i][0]))
            self.tableWidget.setCellWidget(i,0,self.itemSelectComboBoxes[i])#Slot each drop-down-select object into table (each drop-down-select object is now a member of self.itemSelectComboBoxes and self.tableWidget)
        self.setCentralWidget(self.tableWidget)                             #Attach table widget to main window
        self.refreshTable()                                                 #Ensure live self.data values are displaying on the table

    def recordTableChange(self, item):
        '''Runs when an item in the tableWidget is changed\n
        Stores changed item's data into self.data'''
        self.data[item.row()][item.column()] = item.text()                  #Stores changed item's data into self.data
        self.refreshRightDock()

    def buildRightDock(self):
        self.removeDockWidget(self.dock)
        self.dock = QDockWidget('Menu')                                                 #Defines a dock object
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)       #Mandatory dock setup
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock)     #Add dock to main window
        

        self.dockMenu = QWidget()                                                       #Define widget that will be attached to the dock
        self.dockLayout = QFormLayout()                                                 #Define layout that will be applied to above widget

        self.dockItemSelect = QComboBox()                                               #Define drop-down-box for item number selection
        for j in self.availableItemNumbers:                                             #For each available item number
                self.dockItemSelect.addItem(j)                                          #Add item number to drop-down-box

        self.dockItemPanels = []                                                        #Defines list of text boxes for per-panel device count entry
        for i in self.panels:                                                           #Iterate over each panel
            dockItemPanel = QLineEdit()                                                 #Define text box
            dockItemPanel.setPlaceholderText(i)                                         #Set text box prompt
            self.dockItemPanels.append(dockItemPanel)                                   #Add text box to list

        self.addButton = QPushButton('Add Entry', clicked=self.addEntry)                #Defines button that adds a new row based on dock information
        self.spacer = QSpacerItem(50,200)                                               #Defines arbitrary space between buttons
        self.printButton = QPushButton('Print Data', clicked=self.printData)            #Defines button that prints self.data to console

        self.deviceNameSlots = 0
                                                                                        #Determine appropriate number of device name entry text boxes (default to zero)
        if self.currentlySelectedCell[1] >= 1:
            try:
                self.deviceNameSlots = int(self.data[self.currentlySelectedCell[0]][self.currentlySelectedCell[1]])
            except:
                self.deviceNameSlots = 0


        #I don't even know how this paragraph works, but it does. It ensures the hidden device name data on each cell matches the visible device name text boxes on the right-side dock at all times
        self.deviceNames = ['' for i in range(self.deviceNameSlots)]                         #Defines appropriately sized list for device name text boxes
        if self.currentlySelectedCell[1] >= 1 and len(self.tableWidget.item(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).hiddenText) != len(self.deviceNames):
            self.tableWidget.item(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).hiddenText = ['' for i in range(self.deviceNameSlots)]
        for i in range(len(self.deviceNames)):                                          #Iterate over above list    
            self.deviceNames[i] = QLineEdit()                                           #Change each list value to a text box object
            self.deviceNames[i].setPlaceholderText(f'Device {i+1} Name:')               #Set text box prompt
            self.deviceNames[i].setText(self.tableWidget.item(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).hiddenText[i])
         
        self.updateDeviceNamesButton = QPushButton('Update Device Names',clicked=self.updateDeviceNames)#Add button to update device names according to above text boxes

        self.dockLayout.addRow(self.dockItemSelect)                                     #Add objects to layout in desired order (Change this to a grid layout for better and easier control of positions)
        for i in range(len(self.dockItemPanels)):                                       #...
            self.dockLayout.addRow(self.dockItemPanels[i])                              #...
        self.dockLayout.addRow(self.addButton)                                          #...
        for i in range(len(self.deviceNames)):                                          #...
            self.dockLayout.addRow(self.deviceNames[i])                                 #...
        self.dockLayout.addRow(self.updateDeviceNamesButton)
        self.dockLayout.addItem(self.spacer)                                            #...
        self.dockLayout.addRow(self.printButton)                                        #...


        self.dockMenu.setLayout(self.dockLayout)                                        #Apply layout to dockMenu widget
        self.dock.setWidget(self.dockMenu)                                              #Apply dockMenu widget to dock

    def refreshRightDock(self):
        self.currentlySelectedCell = (self.tableWidget.currentRow(),self.tableWidget.currentColumn())#Get currently selected cell coordinates to allow determination of device name text boxes in right-side dock
        self.removeDockWidget(self.dock)
        self.buildRightDock()                                               #Create new dock with correct number of device name text boxes

    def printData(self):
        self.refreshTable()
        print('----------------------------------------------------------------')
        for row in range(len(self.data)):
            for col in range(1,len(self.data[row])):
                pass
                #print(f'Row {row} x Column {col}:')
                #print(self.tableWidget.item(row,col).text())
                #print(self.tableWidget.item(row,col).hiddenText)
        self.exportData()

    def exportData(self):
        print(self.data)
        self.outputDict = {}
        colCounter = 0
        for col in self.tableHeaders[1:]:                            #Iterate over each panel
            self.outputDict[col] = {'description':''}
            rowCounter = 0
            for row in self.data:
                self.outputDict[col][row[0]] = {'count':self.data[rowCounter][colCounter+1],'names':self.tableWidget.item(rowCounter,colCounter+1).hiddenText}
                rowCounter += 1 
            colCounter += 1
            
        print(self.outputDict)
        with open('test.json','w') as outfile:
            json.dump(self.outputDict,outfile)
                
    def importData(self):
        with open('test.json') as jsonFile:
            data = json.load(jsonFile)
        self.tableHeaders = list(data.keys())
        self.tableHeaders.insert(0,'Item No.')
        self.data = []
        self.panels = list(self.tableHeaders[1:])
        presentItems = []
        panelIndex = 1
        for panel in self.panels:
            for item in data[panel]:
                presentItems = [i[0] for i in self.data]
                if item != 'description':
                    if item not in presentItems:
                        newRow = ['' for i in self.tableHeaders]
                        newRow[0] = item
                        newRow[panelIndex] = data[panel][item]['count']
                        self.data.append(newRow)
                    else:
                        self.data[presentItems.index(item)][panelIndex] = data[panel][item]['count']
            panelIndex+=1
        '''^^^Above fills in item counts, but Item No.'s are filled in in the build table function'''

              
        print(self.data)

    def refreshTable(self):
        #Update table from self.data (all but first column)
        for row in range(len(self.data)):                                                       #Iterate over each row in self.data
            for col in range(1,len(self.data[row])):                                            #Iterate over each cell (except for the item number (first) cell)
                if type(self.tableWidget.item(row, col)) != customTableWidgetItem:
                    self.tableWidget.setItem(row, col, customTableWidgetItem(str(self.data[row][col])))  #Slot a tableWidgetItem object into each cell of the table (excluding first column) to display data in table ---> Change to customTableWidgetItem and test
        '''^^^This line is breaking the hidden text feature^^^'''
        #Update self.data from table (first column)
        for i in range(len(self.itemSelectComboBoxes)):                                         #Iterate over each first-column drop-down-select box
            self.data[i][0] = self.itemSelectComboBoxes[i].currentText()                        #Apply currently selected value to associated self.data value

    def addEntry(self):
        '''Should not be used if item number is already present in table\n
        In that case, use updateEntry()'''
        addData = False
        data = [self.dockItemSelect.currentText()]                                                  #Initializes list of new data with first value equal to right-side dock drop-down-select current value
        for i in self.dockItemPanels:                                                               #Iterate over each panel text box
            if i.text() != '':                                                                      #If any panel text box has data
                addData = True                                                                      #Don't end function early
            data.append(i.text())                                                                   #Add each panel text box text to list of new data

        if addData == False:                                                                        #If no devices were added, but addEntry button was pushed
            return                                                                                  #End function early
        
        self.data.append(data)                                                                      #Add list of new data to self.data
        self.tableWidget.insertRow(self.tableWidget.rowCount())                                     #Add row to the end of table to hold new entry

        for i in self.dockItemPanels:                                                               #Reset panel text box
            i.setText('')                                                                           #Clear panel text boxes and re-add text prompt

        newDropDown = QComboBox()                                                                   #Create dummy drop down
        for j in self.availableItemNumbers:                                                         #Iterate over available material numbers
            newDropDown.addItem(j)                                                                  #Add available material numbers to dummy drop down
        self.itemSelectComboBoxes.append(newDropDown)                                               #Add dummy drop down to end of list of left column drop-down-boxes

        #Make drop-down object a member of self.itemSelectComboBoxes list and self.tableWidget object
        self.itemSelectComboBoxes[-1].setCurrentIndex(self.availableItemNumbers.index(data[0]))     #Set new drop-down box to have the same value as drop-down on the right-side dock
        self.tableWidget.setCellWidget(len(self.data)-1,0,self.itemSelectComboBoxes[len(self.data)-1])#Slot new drop-down into the table
        self.refreshTable()

    def updateDeviceNames(self):
        self.tableWidget.item(self.currentlySelectedCell[0],self.currentlySelectedCell[1]).hiddenText = [i.text() for i in self.deviceNames]
        

class customTableWidgetItem(QTableWidgetItem):
    def __init__(self,text):
        super(customTableWidgetItem,self).__init__(text)
        self.hiddenText = ['0'] #For device names
        


if  __name__ == "__main__":
    app = QApplication([])
    application = mainProgram(tableHeaders=['Item No.','Panel B1','Panel B2', 'Panel B3'],masterMaterialList={'3J':'','44':'Test','55':'Pierce'})
    application.show()
    sys.exit(app.exec())