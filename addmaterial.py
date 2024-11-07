import sys
from screeninfo import get_monitors
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAbstractScrollArea, QSpinBox, QCheckBox, QInputDialog, QLabel, QGridLayout, QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem, QTabWidget, QListWidget


class AddMaterial(QMainWindow):
    def __init__(self):
        super(AddMaterial, self).__init__()

        self.addMaterialDialog = QDialog()
        self.addMaterialDialog.setWindowTitle('New Material List?')
        self.addMaterialDialog.setMinimumSize(800,800)
        self.addMaterialDialogLayout = QGridLayout()

        self.addMaterialDialogLayout.setSpacing(5)
        
        
        self.monitor = get_monitors()
        'Defines monitor object that allows automatic screen window sizing per screen size'
        # self.monitorXSize = int()
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        'Defines width of user''s monitor'
        # self.monitorYSize = int()
        'Defines height of user''s monitor'
        self.xShift = int()
        'Defines x shift used to center window'
        self.yShift = int()
        'Defines y shift used to center window'
        self.xSize = self.monitorYSize * .8
        'Defines width of window'
        self.ySize = self.monitorYSize * .6
        'Defines height of window'
        
        self.deviceItemNumber = QComboBox(self)
        self.deviceType = QListWidget(self)
        
        self.deviceType.addItems(['Relay','Test Switch','Lock Out Relay','Control Switch'])
        self.deviceType.currentItemChanged.connect(self.currentDeviceChanged)
        
        self.grid = [
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            [QLabel('Item No.'), self.deviceItemNumber, '', QLineEdit(), '', QLineEdit(), '', QLabel('Device Type'), '', '', '', '', QLabel('Major Functions'), '', '', '', '', QLabel('Inventory'), '', ''],
            [QLabel('Manufacture'), QLineEdit(), '', '', '', '', '', self.deviceType, '', '', '', '', QPlainTextEdit(), '', '', '', '', QLabel('Qty.'), QLineEdit(), ''],
            [QLabel('Series'), QLineEdit(),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Part Number'), QLineEdit(),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Electrical Properties'), '', '', '', '', '', '', QLabel('I/O Details'), '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Power Supply Voltage'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Control Voltage'), QLineEdit(), QLabel('V'), QComboBox(),'',  '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('AC Current Input'), QLineEdit(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('AC Voltage Input'),  QLineEdit(), QLabel('V AC'), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Zones of Protection'), QSpinBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Coil Operation Volt.'), QLineEdit(), QLabel('V'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Reset'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Meter Form'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Number of Phases'), QSpinBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Number of Wires'), QSpinBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Test Switch Arr. Frist 10'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Test Switch Arr. Middle 10'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Test Switch Arr. Last 10'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Lamp Voltage'), QComboBox(), QLabel('V'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ]

        'grid'
        self.gridSpan = [
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1)],
            [(1,1), (2,1), '', (2,1), '', (2,1), '', (5,1), '', '', '', '', (5,1), '', '', '', '', (2,1), '', ''],
            [(1,1), (6,1), '', '', '', '', '', (5,3), '', '', '', '', (5,3), '', '', '', '', (1,1), (1,1), ''],
            [(1,1), (6,1),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (6,1),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(7,1),'', '', '', '', '', '', (7,1), '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        ]
            
        for i in self.grid:
            if len(i) != 20:
                print(i,len(i))
        for i in self.gridSpan:
            if len(i) != 20:
                print(i,len(i))
                    
        self.columnWidth = int(self.xSize / len(self.grid[0]))
        self.rowHeight = int(self.ySize / len(self.grid))
        
        self.columnSpan = 1
        
        for i, row in enumerate(self.grid):            
            for j, cell in enumerate(row):
                label = QLabel(str(i) + ',' + str(j),)
                label.setStyleSheet('color: rgb(200,200,200); border: 1px solid rgb(200,200,200)')
                self.addMaterialDialogLayout.addWidget(label, i, j)

        for i,row in enumerate(self.grid):
            for j,cell in enumerate(row):
                if cell not in ['', '0']:
                    print(i,j)
                    rowSpan = self.gridSpan[i][j][1]
                    columnSpan = self.gridSpan[i][j][0]
                    self.addMaterialDialogLayout.addWidget(cell, i, j, rowSpan, columnSpan)
                    
                elif cell == '0':
                    rowSpan = self.gridSpan[i][j][1]
                    columnSpan = self.gridSpan[i][j][0]
                    self.addMaterialDialogLayout.addItem(QSpacerItem(self.columnWidth, self.rowHeight), i, j, rowSpan, columnSpan)
                    
        self.widget = QWidget()
        self.widget.setLayout(self.addMaterialDialogLayout)
        
        self.setCentralWidget(self.widget)
        
        self.buildMainWindow()
        
    def currentDeviceChanged(self, device):
        deviceDict = {
            'Relay': [[1, 10],[(13,1), (14,1)]],
            'Test Switch': [[40, 49],[]],
            'Lock Out Relay': [[35, 39],[]],
            'Control Switch': [[30, 34],[]],
            'Light': [[74,77],[]]
        }
        
        self.deviceItemNumber.clear()
        
        itemNumRange = deviceDict[device.text()][0]
        hideFieldCords = deviceDict[device.text()][1]
        
        for i,row in enumerate(self.grid):
            for j,cell in enumerate(row):
                if cell not in ['', '0']:
                    cell.setDisabled(False)
                    self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                    
        for i in hideFieldCords:
            print(i)
            coordsx = i[0]
            coordsy = i[1]
            disableWidget = self.grid[coordsx][coordsy]
            disableWidget.setDisabled(True)
            self.addMaterialDialogLayout.addWidget(disableWidget, coordsx, coordsy)            
        
        for i in range(itemNumRange[0], itemNumRange[1]):
            self.deviceItemNumber.addItem(str(i))
        
    def buildMainWindow(self):
        self.xSize = int(self.xSize)
        self.ySize = int(self.ySize)
        self.xShift = int((self.monitorXSize - self.xSize) / 2)
        self.yShift = int((self.monitorYSize - self.ySize) / 2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Item to Master Material List')
        
    
        
        
if  __name__ == "__main__":
    app = QApplication(sys.argv)
    application = AddMaterial()
    application.show()
    sys.exit(app.exec())