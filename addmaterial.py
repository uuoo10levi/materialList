import sys
import json
from screeninfo import get_monitors
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QSpinBox, QCheckBox, QLabel, QGridLayout, QComboBox, QApplication, QMainWindow, QDialog, QWidget, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem, QListWidget, QAction

class CcgLabel(QLabel):
    '''Custom label text aligned center and gray background'''
    def __init__(self, name):
        QLabel.__init__(self)
        
        self.name = name
        '''name attribute reference'''
        self.setText(self.name)
        '''label text as name attribute reference'''
        self.setAlignment(QtCore.Qt.AlignCenter)
        '''text alignment set to center'''
        self.setStyleSheet('background: rgb(150,150,150)')
        '''backgound color set to gray'''
        self.setFixedHeight(25)
        '''fixed height set to 25'''

class CComboBox(QComboBox):
    '''Custom combo box with name attribute reference'''
    def __init__(self, name):
        QComboBox.__init__(self)
        
        self.name = name
        '''name attribute reference'''
        
class CSpinBox(QSpinBox):
    '''Custom spin box with name, suffix, min, and max attribute reference'''
    def __init__(self, name, suffix='', min=0, max=999):
        QSpinBox.__init__(self)
        
        self.name = name
        '''name attribute reference'''
        self.setSuffix(suffix)
        '''set suffix attribute to suffix if variable is supplied'''
        self.setMinimum(min)
        '''set minimum number in spinbox if variable is supplied if not it will be set to 0'''
        self.setMaximum(max)
        '''set maximum number in spinbox if variable is spplied if not it will be set to 999'''
        
class CLineEdit(QLineEdit):
    def __init__(self, name):
        QLineEdit.__init__(self)
        
        self.name = name
        
class CPlainTextEdit(QPlainTextEdit):
    def __init__(self, name):
        QPlainTextEdit.__init__(self)
        
        self.name = name
        
class CListWidget(QListWidget):
    def __init__(self, name):
        QListWidget.__init__(self)
        
        self.name = name
        
class CCheckBox(QCheckBox):
    def __init__(self, name):
        QCheckBox.__init__(self)
        
        self.name = name
        
# class CListWidget(QListWidget):
#     def __init__(self, name):
#         QListWidget.__init__()
        
#         self.name = name
        
class AddMaterial(QMainWindow):
    def __init__(self):
        super(AddMaterial, self).__init__()
        
        self.importJson()

        self.addMaterialDialog = QDialog()
        self.addMaterialDialog.setMinimumSize(100,100)
        self.addMaterialDialogLayout = QGridLayout()

        self.addMaterialDialogLayout.setSpacing(5)
        
        self.displayGrid = False 
        self.gridCoords = []
        
        self.monitor = get_monitors()
        'Defines monitor object that allows automatic screen window sizing per screen size'
        self.monitorXSize = int(self.monitor[0].width)
        'Defines width of user''s monitor'
        self.monitorYSize = int(self.monitor[0].height)
        'Defines height of user''s monitor'
        self.xShift = int()
        'Defines x shift used to center window'
        self.yShift = int()
        'Defines y shift used to center window'
        self.xSize = self.monitorXSize * .8
        'Defines width of window'
        self.ySize = self.monitorYSize * .8
        'Defines height of window'
        self.importComboBoxDict('.\json\ComboBox.json')
        self.importDeviceTypeDict('.\json\DeviceTypes.json')
                
        self.deviceItemNumber = CComboBox('Item Number')
        self.deviceType = CListWidget('Device Type')
        
        for i,device in enumerate(self.deviceTypeDict):
            self.deviceType.addItem(device)

        
        # self.deviceType.addItems(['Relay','Test Switch','Lock Out Relay','Control Switch'])
        self.deviceType.currentItemChanged.connect(self.currentDeviceChanged)
        
        self.grid = []
        
        self.grid = [
            #0-4
            ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            [QLabel('Item No.'), self.deviceItemNumber, CLineEdit('Item Number Midfix'), CLineEdit('Item Number Suffix'), CcgLabel('Device Type'), '1,5', '1,6', CcgLabel('Major Functions'), '1,8', '1,9', '1,10', '1,11', CcgLabel('Inventory'), '1,13'],
            [QLabel('manufacturer'), CLineEdit('manufacturer'), '2,2', '2,3', self.deviceType, '2,5', '2,6', CPlainTextEdit('Major Functions'), '2,8', '2,9', '2,10', '2,11', QLabel('Qty.'), CLineEdit('Qty')],
            [QLabel('Series'), CLineEdit('Series'),'3,2', '3,3', '3,4', '3,5', '3,6', '3,7', '3,8', '3,9', '3,10', '3,11', QLabel('Location'), '3,13'],
            [QLabel('Part Number'), CLineEdit('Part Number'),'4,2', '4,3', '4,4', '4,5', '4,6', '4,7', '4,8', '4,9', '4,10', '4,11', CLineEdit('Location'), '4,13'],
            #5-10
            ['0', '5,1', '5,2', '5,3', '5,4', '5,5', '5,6', '5,7', '5,8', '5,9', '5,10', '5,11', '5,12', '5,13'],
            [CcgLabel('Electrical Properties'), '6,1', '6,2', '6,3', CcgLabel('I/O Details'), '6,5', '6,6', '6,7', '6,8', CcgLabel('Communications'), '6,10', '6,11', '6,12', '6,13'],
            [QLabel('Power Supply Voltage'), CComboBox('Power Supply Voltage'), '7,2', '7,3', CcgLabel('Standard I/O'), '7,5', '7,6', '7,7', '7,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '7,12', '7,13'],
            [QLabel('Control Voltage'), CComboBox('Control Voltage'), '8,2', '8,3', QLabel('Standard Inputs'), CSpinBox('Standard Inputs'), CComboBox('Input Types', ), '8,7', '8,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '8,12', '8,13'],
            [QLabel('AC Current Input'), CSpinBox('AC Current Input', 'A'), '9,2', '9,3', QLabel('Standard Inputs'), CSpinBox('Standard Inputs'), CComboBox('Input Types'),'9,7', '9,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '9,12', '9,13'],
            [QLabel('AC Voltage Input'), CSpinBox('AC Voltage Input', 'V AC'), '10,2', '10,3', QLabel('Standard Outputs'), CSpinBox('Standard Outputs'), CComboBox('Output Types'), '10,7', '10,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '10,12', '10,13'],
            #11-15
            [QLabel('Zones of Protection'), CSpinBox('Zones of Protection', '', 3, 5), '11,2', '11,3', QLabel('Standard Outputs'), CSpinBox('Standard Outputs'), CComboBox('Output Types'), '11,7', '11,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '11,12', '11,13'],
            [QLabel('Coil Operation Volt.'), CComboBox('Coil Operating Voltage'), '12,2', '12,4', CcgLabel('Additional I/O Set 1'), '12,5', '12,6', '12,7', '12,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '12,12', '12,13'],
            [QLabel('Reset'), CComboBox('Reset'), '13,2', '13,3', QLabel('Additional Inputs'), CSpinBox('Additional Inputs'), CComboBox('Input Types'), '13,7', '13,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '13,12', '13,13'],
            [QLabel('Meter Form'), CComboBox('Meter Form'), '14,2', '14,3', QLabel('Additional Inputs'),CSpinBox('Additional Inputs'), CComboBox('Input Types'), '14,7', '14,8', QLabel('Comm. Interface'), CSpinBox('Comm. Interface'), CComboBox('Comm. Interface'), '14,12', '14,13'],
            [QLabel('Number of Phases'), CSpinBox('Number of Phases', '', 3, 3), '15,2', '15,3', QLabel('Additional Outputs'), CSpinBox('Additional Outputs'), CComboBox('Output Types'), '15,7', '15,8', QLabel('Commumincations Protocols'), '15,10',  CPlainTextEdit('Communications Protocols'), '15,12' '15,13'],
            #16-20
            [QLabel('Number of Wires'), CSpinBox('Number of Wires', '', 4, 4), '16,2', '16,3', QLabel('Additional Outputs'), CSpinBox('Additional Inputs'), CComboBox('Output Types'), '16,7', '16,8', '16,9', '16,10', '16,11', '16,12', '16,13'],
            [QLabel('Test Switch Arr. A'), CComboBox('Test Switch Arrangement A'), '17,2', '17,3,', CcgLabel('Additional I/O Set 2'), '17,5', '17,6', '17,7', '17,8', QLabel('Material Status'), CComboBox('Material Status'), '17,11', '17,12', '17,13'],
            [QLabel('Test Switch Arr. B'), CComboBox('Test Switch Arrangement B'), '18,2', '18,3', QLabel('Additional Inputs'), CSpinBox('Additional Inputs'), CComboBox('Input Types'), '18,7', '18,8', QLabel('Itemized Pricing'), CCheckBox('Itemized Pricing'), '18,11', '18,12', '18,13'],
            [QLabel('Test Switch Arr. C'), CComboBox('Test Switch Arrangement C'), '19,2', '19,3', QLabel('Additional Inputs'), CSpinBox('Additional Inputs'), CComboBox('Input Types'), '19,7', '19,8', QLabel('Short Name'), '19,10', '19,11', '19,12', '19,13'],
            [QLabel('Lamp Voltage'), CComboBox('Lamp Voltage'), '20,1', '20,3', QLabel('Additional Outputs'), CSpinBox('Additinal Outputs'), CComboBox('Output Types'), '20,7', '20,8', CPlainTextEdit('Short Name'), '20,10', '20,11', '20,12', '20,13'],
            #21-25
            [CcgLabel('Physcial Properties'), '21,1', '21,2', '21,3', QLabel('Additional Outputs'), CSpinBox('Additinal Outputs'), CComboBox('Output Types'), '21,7', '21,8', '21,9', '21,10', '21,11', '21,12', '21,13'],
            [QLabel('Orientation'), CComboBox('Orientation'), '22,2', '22,3', CcgLabel('Additional I/O Set 3'), '22,5', '22,6', '22,7', '22,8', '22,9', '22,10', '22,11', '22,12', '22,13'],
            [QLabel('Mounting'), CComboBox('Mounting'), '23,2', '23,3', QLabel('Additional Inputs'), CSpinBox('Additinal Inputs'), CComboBox('Input Types'), '23,7', '23,8', '23,9', '23,10', '23,11', '23,12', '23,13'],
            [QLabel('Rack Units'), CSpinBox('Rack Unints'), '24,2', '24,3', QLabel('Additional Inputs'), CSpinBox('Additinal Inputs'), CComboBox('Input Types'), '24,7', '24,8', '24,9', '24,10', '24,11', '24,12', '24,13'],
            [QLabel('User Interface'), CComboBox('User Interface'), '25,2', '25,3', QLabel('Additional Outputs'), CSpinBox('Additinal Outputs'), CComboBox('Output Types'), '25,7', '25,8', '25,9', '25,10', '25,11', '25,12', '25,13'],
            #26-30
            [QLabel('Handle Style'), CComboBox('Handle Style'), '26,2', '26,3', QLabel('Additional Outputs'), CSpinBox('Additinal Outputs'), CComboBox('Output Types'), '26,7', '26,8', '26,9', '26,10', '26,11', '26,12', '26,13'],
            [QLabel('Action'), CComboBox('Action'), '27,2', '27,3', '27,4', '27,5', '27,6', '27,7', '27,8', '27,9', '27,10', '27,11', '27,12', '27,13'],
            [QLabel('Decks'), CSpinBox('Decks'), '28,2', '28,3', QLabel('Catalog cut included'), '28,5', CCheckBox('Catalog cut included'), '28,7', '28,8', '28,9', '28,10', '28,11', '28,12', '28,13'],
            [QLabel('Test Switch Cover'), CComboBox('Test Switch Cover'), '29,2', '29,3', '29,4', '29,5', '29,6', '29,7', '29,8', QPushButton('Save Material', clicked=self.saveMaterial), '29,10', '29,11', '29,12', '29,13'],
            [QLabel('Lamp Color'), CComboBox('Lamp Color'), '30,2', '30,3', QLabel('Photo on file'), '30,5', CCheckBox('Photo on file'), '30,7', '30,8', QPushButton('Duplicate Material'), '30,10', '30,11', '30,12', '30,13'],
            #31-32
            [QLabel('Lens Color'), CComboBox('Lens Color'), '31,2', '31,3', '31,4', '31,5', '31,6', '31,7', '31,8', QPushButton('Delete Material'), '31,10', '31,11', '31,12', '31,13'],
            [QLabel('Length'), CLineEdit('Length'), CComboBox('Length Units'), '32,3', QLabel('Check for this on each contract'), '32,5', CCheckBox('Check for this on each contract'), '32,7', '32,8', QPushButton('Item Numbering Guide'), '32,10', '32,11', '32,12', '32,13'],
            ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        ]
        
        self.gridSpan = [
            #  0      1      2      3      4      5      6      7      8      9      10     11     12     13     14
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1),    ''],
            [(1,1), (1,1), (1,1), (1,1), (3,1),    '',    '', (5,1),    '',    '',    '',    '', (2,1),    '',    ''],
            [(1,1), (3,1),    '',    '', (3,3),    '',    '', (5,3),    '',    '',    '',    '', (1,1), (1,1),    ''],
            [(1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '', (2,1),    '',    ''],
            [(1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '', (2,1),    '',    ''],
            #5-10
            [(1,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(4,1),    '',    '',    '', (5,1),    '',    '',    '',    '', (5,1),    '',    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (5,1),    '',    '',    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            #11-15
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (5,1),    '',    '',    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (2,1),    '', (3,12),   '',    '',    ''],
            #16-20
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (5,1),    '',    '',    '',    '', (1,1), (1,1),    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1),    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (2,1),    '',    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (2,3),    '',    '',    '',    '',    ''],
            #21-25
            [(4,1),    '',    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (2,1),    '',    '', (5,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (2,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    ''],
            #26-30
            [(1,1), (2,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (2,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (2,1),    '', (1,1),    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (2,1),    '',    '',    '',    '',    '',    '',    '', (2,1),    '',    '',    '',    '',    ''],
            [(1,1), (2,1),    '',    '', (2,1),    '', (1,1),    '',    '', (2,1),    '',    '',    '',    '',    ''],
            #31-32
            [(1,1), (2,1),    '',    '',    '',    '',    '',    '',    '', (2,1),    '',    '',    '',    '',    ''],
            [(1,1), (1,1), (1,1),    '', (2,1),    '', (1,1),    '',    '', (2,1),    '',    '',    '',    '',    ''],
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1)]
        ]
        
        error = 0

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if type(cell) is str and cell != '0' and cell != '1' and type(self.gridSpan[i][j]) is tuple:
                    print(f"{i},{j} is {type(cell)}, gridspan is {self.gridSpan[i][j]}")
                    error = 1

        if error == 1:
            exit()
                    
        self.columnWidth = int(self.xSize / len(self.grid[0]))
        self.rowHeight = int(self.ySize / len(self.grid))
        
        for i,row in enumerate(self.grid):
                for j,cell in enumerate(row):
                    # if cell not in ['', '0']:
                    if cell.__class__.__name__ == 'CComboBox' and cell.name != 'Item Number':
                        for options in (self.comboBoxValues(cell.name)):
                            cell.addItem(options)
                            cell.setCurrentIndex(-1)
  
                    if type(cell) is not str:
                        self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                        # field = self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])    
                    if cell == '1':
                        self.addMaterialDialogLayout.addItem(QSpacerItem(1, self.rowHeight), i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                    elif cell == '0':
                        self.addMaterialDialogLayout.addItem(QSpacerItem(self.columnWidth, self.rowHeight), i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                            
        self.widget = QWidget()
        self.widget.setLayout(self.addMaterialDialogLayout)
        
        self.setCentralWidget(self.widget)        
        
        self.buildMainWindow()
        
        print(self.allMaterialDict)
        
    def importJson(self):
        with open('json/material.json', 'r') as file:
            self.allMaterialDict = json.load(file)
            
    def currentDeviceChanged(self, device):
        deviceDict = {
            'Relay': [[1,9],[(13,0),(13,1),(14,0),(14,1),(17,0),(17,1),(18,0),(18,1),(19,0),(19,1),(20,0),(20,1),(26,0),(26,1),(27,0),(27,1),(28,0),(28,1),(29,0),(29,1),(30,0),(30,1),(31,0),(31,1),(32,0),(32,1),(32,2)]],
            'Clock/RTAC/Revenue meter': [[10,19], []],
            'Carrier equipment': [[20,29], []],
            'Control switch/Other rotary switch/Pushbuttons': [[30,39],[]],
            'Test Switch': [[40, 49],[(7,0), (7,1), (8,0), (8, 1), (8, 4), (8, 5), (12, 4), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (20, 1), (20, 4)]],
            'Display meter/Transducer': [[50,59],[]],
            'Auxiliary instrument/Transformer/Signal conditioner': [[60,69],[]],
            'Resistor/Indication lamp': [[70,79],[]],
            'Auxiliary relay': [[80,89],[]],
            'Miscellaneous panel material': [[90,179],[]],
            'Cable': [[200,210], []]
        }
    
        self.deviceItemNumber.clear()
        
        itemNumRange = deviceDict[device.text()][0]
        hideFieldCords = deviceDict[device.text()][1]
        
        for i,row in enumerate(self.grid):
            for j,cell in enumerate(row):
                if type(cell) is not str:
                    cell.setDisabled(False)
                    cell.setHidden(False)
                    self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                
        for i in hideFieldCords:
            cordsx = i[0]
            cordsy = i[1]
            
            disableWidget = self.grid[cordsx][cordsy]
            disableWidget.setDisabled(True)
            disableWidget.setHidden(True)
            self.addMaterialDialogLayout.addWidget(disableWidget, cordsx, cordsy, self.gridSpan[cordsx][cordsy][1], self.gridSpan[cordsx][cordsy][0])            
        
        for i in range(itemNumRange[0], itemNumRange[1]):
            self.deviceItemNumber.addItem(str(i))
        
    def buildMainWindow(self):
        self.xSize = int(self.xSize)
        self.ySize = int(self.ySize)
        self.xShift = int((self.monitorXSize - self.xSize) / 2)
        self.yShift = int((self.monitorYSize - self.ySize) / 2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Item to Master Material List')
    
    def currentTextValue(self, fieldObj):
        fieldType = fieldObj.__class__.__name__
        if fieldObj.isVisible() == True:
            if fieldType == 'CComboBox':
                temp = fieldObj.currentText()
            elif fieldType == 'CLineEdit':
                temp = fieldObj.text()
            elif fieldType == 'CSpinBox':
                temp = str(fieldObj.value())
                if temp == '0':
                    temp = ''
            elif fieldType == 'CCheckBox':
                temp = str(fieldObj.isChecked())
            elif fieldType == 'CListWidget':
                temp = (fieldObj.currentItem().text())
            elif fieldType == 'CPlainTextEdit':
                temp = (fieldObj.toPlainText())
            else:
                temp = 'Issue'
                print('Issue')
                print(fieldObj.name)
            
        
            return(temp)
        
    def importDeviceTypeDict(self, jsonFilePath):
        with open(jsonFilePath, 'r') as file:
            self.deviceTypeDict = json.load(file)
        
    def importComboBoxDict(self, jsonFilePath):
        with open(jsonFilePath, 'r') as file:
            self.comboBoxDict = json.load(file)
        
    def comboBoxValues(self, name):
        if name != 'Item Number':
            comboBoxList = self.comboBoxDict[name]
            return comboBoxList
    
    def saveMaterial(self):
        self.gridFieldDict = {
            'Item Number': [(1,1), (1,2), (1,3)],
            'manufacturer': (2,1),
            'Series': (3,1),
            'Part Number': (4,1),
            'Device Type': (2,4),
            'Power Supply Voltage': (7,1),
            'Control Voltage': (8,1),
            'AC Current Input': (9,1),
            'AC Voltage Input': (10,1),
            'Zones of Protection': (11,1),
            'Coil Operation Volt.': (12,1),
            'Reset': (13,1),
            'Meter Form': (14,1),
            'Number of Phases': (15,1),
            'Number of Wires': (16,1),
            'Test Switch Arr. A': (17,1),
            'Test Switch Arr. B': (18,1),
            'Test Switch Arr. C': (19,1),
            'Lamp Voltage': (20,1),
            'Orentation': (22,1),
            'Mounting': (23,1),
            'Rack Units': (24,1),
            'User Interface': (25,1),
            'Handle Style': (26,1),
            'Action': (27,1),
            'Decks': (28,1),
            'Test Switch Cover': (29,1),
            'Lamp Color': (30,1),
            'Lens Color': (31,1),
            'Length': [(32,1), (32,2)],
            'Standard Inputs': [(8,5), (8,6), (9,5), (9,6)],
            'Standard Outputs': [(10,5), (10,6), (11,5), (11,6)],
            'Additional Inputs': [(13,5), (13,6), (14,5), (14,6), (18,5), (18,6), (19,5), (19,6), (23,5), (23,6), (24,5), (24,6)],
            'Standard Outputs': [(15,5), (15,6), (16,5), (16,6), (20,5), (20,6), (21,5), (21,6), (25,5), (25,6), (25,5), (26,6)],
            'Catalog Cut Included': (28,6),
            'Photo on file': (32,6),
            'Check for the on each contract': (32,6),
            'Major Functions': (2,7),
            'Comm. Interface': [(7,10), (7,11), (8,10),(8,11),(9,10),(9,11),(10,10),(10,11),(11,10),(11,11),(12,10),(12,11),(13,10),(13,11),(14,10),(14,11)],
            'Communications Protocals': (15,11),
            'Material Status': (17,10),
            'Itemized Pricing': (18,10),
            'Short Name': (20,9),
            'Inventory Qty': (2,13),
            'Inventory Location': (4,12)
        }
        
        self.itemDict = {
        }
        
        for i,key in enumerate(self.gridFieldDict):
            keyValue = self.gridFieldDict[key]
            # print(type(keyValue))
            if type(keyValue) is list:
                # print(keyValue)
                keyText = ''
                for j,val in enumerate(keyValue):
                    textValue = (self.currentTextValue(self.grid[val[0]][val[1]]))
                    keyText = keyText + textValue
                        
            elif type(keyValue) is tuple:
                keyText = self.currentTextValue(self.grid[keyValue[0]][keyValue[1]])
            
            if keyText == '' or keyText == None or keyText == 'False':
                pass
            else: 
                self.itemDict[key] = keyText
                
        self.createItemDescription()
        
    def createItemDescription(self):
        # self.description = f"{self.itemDict['Major Functions']}<br/>Mounting: {self.itemDict['Mounting']}, {self.itemDict['Rack Units']} RU<br/>Power supply Voltage: {self.itemDict['Power Supply Voltage']}<br/>Control Voltage: {self.itemDict['Control Voltage']}<br/>Current input rating: {self.itemDict['AC Current Input']}<br/>Voltage input rating: {self.itemDict['AC Voltage Input']}<br/>Standard I/O: (standardinputs), (standardoutputs)<br/>"
        '''
        Additional I/O: (additionalinputs), (aditionaloutputs)<br/
        User interface: (userinterface)<br/>
        Comm. interface: (comminterface)<br/>
        Comm. protocol: (protocol)<br/>
        Handle style: (handlestyle)<br/>
        Coil rating: (coilrating)<br/>
        Number of decks: (decks)
        Action: (action)<br/>
        Meter form: (meterform)<br/>
        Phases: (phases)<br/>
        Wires: (wires)<br/>
        <Position A:><Arrangement:> (positiona)<br/>
        Position B: (positionb)<br/>
        Position C: (positionc)<br/>
        Cover: (cover)<br/>
        Lamp voltage: (lampvolts)<br/>
        Lamp color: (lampcolor)<br/>
        Lens color: (lenscolor)<br/>
        Length: (length) (lengthunits)<br/>
        (manufacturer) (model)<br/>
        See catalog cut
        '''
        # print(self.itemDict['Major Functions'])
                  
    def keyPressEvent(self, event):
        #F8 Toggle Display grid
        if event.key() == Qt.Key_F3:
            self.addMaterialtoDict()
        if event.key() == Qt.Key_F8:
            if self.displayGrid == False:
                self.displayGrid = True
            else:
                self.displayGrid = False
            
            if self.displayGrid == True:
                for i, row in enumerate(self.grid):            
                    for j, cell in enumerate(row):
                        label = QLabel(str(i) + ',' + str(j))
                        self.gridCoords.append(label)
                        label.setStyleSheet('color: rgb(200,200,200); border: 1px solid rgb(200,200,200)')
                        self.addMaterialDialogLayout.addWidget(label, i, j)
            if self.displayGrid == False:            
                for i in self.gridCoords:
                    i.setHidden(True)
                    i.setStyleSheet('color: rgb(200,200,200); border: 1px solid rgb(200,200,200)')
                    self.columnSpan = 1
        
            for i,row in enumerate(self.grid):
                for j,cell in enumerate(row):
                    if type(cell) is not str:
                        self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                    elif cell == '0':
                        self.addMaterialDialogLayout.addItem(QSpacerItem(self.columnWidth, self.rowHeight), i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])     
            
if  __name__ == "__main__":
    app = QApplication(sys.argv)
    application = AddMaterial()
    application.show()
    sys.exit(app.exec())