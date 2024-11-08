import sys
from screeninfo import get_monitors
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAbstractScrollArea, QSpinBox, QCheckBox, QInputDialog, QLabel, QGridLayout, QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem, QTabWidget, QListWidget

# class QComboBox(QComboBox):
#         def __init__(self, parent=None):
#             super().__init__(parent)
#             self.setStyleSheet('QComboBox::disabled {visibility: hidden;}')

        
class AddMaterial(QMainWindow):
    class CQLabel(QLabel):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.objType = 'label'
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet('background: rgb(150,150,150)')
        
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
        self.xSize = self.monitorXSize * .6
        'Defines width of window'
        self.ySize = self.monitorYSize * .8
        'Defines height of window'
        
        self.deviceItemNumber = QComboBox(self)
        self.deviceType = QListWidget(self)
        
        self.deviceType.addItems(['Relay','Test Switch','Lock Out Relay','Control Switch'])
        self.deviceType.currentItemChanged.connect(self.currentDeviceChanged)
        
        self.grid = [
            #0-4
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            [QLabel('Item No.'), self.deviceItemNumber, QLineEdit(), QLineEdit(), self.CQLabel('Device Type'), '', '', '', '', self.CQLabel('Major Functions'), '', '', '', '', self.CQLabel('Inventory'), '', '', '', '' ,''],
            [QLabel('Manufacture'), QLineEdit(), '', '', self.deviceType, '', '', '', '', QPlainTextEdit(), '', '', '', '', QLabel('Qty.'), QLineEdit(), '', '', '', ''],
            [QLabel('Series'), QLineEdit(),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Part Number'), QLineEdit(),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #5-10
            ['0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [self.CQLabel('Electrical Properties'), '', '', '', self.CQLabel('I/O Details'), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Power Supply Voltage'), QComboBox(), '', '', self.CQLabel('Standard I/O'),'', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Control Voltage'), QLineEdit(), QLabel('V'), QComboBox(), QLabel('Standard Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('AC Current Input'), QLineEdit(), '', '', QLabel('Standard Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '' '', '', '', '', '', '', ''],
            [QLabel('AC Voltage Input'),  QLineEdit(), QLabel('V AC'), '', QLabel('Standard Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #11-15
            [QLabel('Zones of Protection'), QSpinBox(), '', '', QLabel('Standard Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Coil Operation Volt.'), QLineEdit(), QLabel('V'), QComboBox(), self.CQLabel('Additional I/O Set 1'), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Reset'), QComboBox(), '', '', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Meter Form'), QComboBox(), '', '', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Number of Phases'), QSpinBox(), '', '', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #16-20
            [QLabel('Number of Wires'), QSpinBox(), '', '', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Test Switch Arr. Frist 10'), QComboBox(), '', '', self.CQLabel('Additional I/O Set 2'), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Test Switch Arr. Middle 10'), QComboBox(), '', '', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Test Switch Arr. Last 10'), QComboBox(), '', '', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Lamp Voltage'), QComboBox(), QLabel('V'), QComboBox(), QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #21-25
            [self.CQLabel('Physcial Properties'), '', '', '', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Orientation'), QComboBox(), '', '', self.CQLabel('Additional I/O Set 3'), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Mounting'), QComboBox(), '', '', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Rack Units'), QSpinBox(), '', '', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('User Interface'), QComboBox(), '', '', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #26-30
            [QLabel('Handle Style'), QComboBox(), '', '', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Action'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Decks'), QSpinBox(), '', '', QLabel('Catalog cut included'), '', '', QCheckBox(), '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Test Switch Cover'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Lamp Color'), QComboBox(), '', '', QLabel('Photo on file'), '', '', QCheckBox(), '', '', '', '', '', '', '', '', '', '', '', ''],
            #31-32
            [QLabel('Lens Color'), QComboBox(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [QLabel('Length'), QLineEdit(), QComboBox(), '', QLabel('Check for the on each contract'), '', '', QCheckBox(), '', '', '', '', '', '', '', '', '', '', '', ''],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        ]
        
        self.gridSpan = [
            #0-4
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1)],
            [(1,1), (1,1), (1,1), (1,1), (5,1), '', '', '', '', (5,1), '', '', '', '', (2,1), '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', (5,3), '', '', '', '', (5,3), '', '', '', '', (1,1), (1,1), '', '', '', '', ''],
            [(1,1), (3,1),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1),'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #5-10
            [(1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(4,1),'', '', '', (5,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', (5,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #11-15
            [(1,1), (1,1), '', (1,1), (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), (1,1), (5,1), '', '',  '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #16-20
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', (5,1), '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (3,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #21-25
            [(4,1), '', '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (5,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            #26-30
            [(1,1), (1,1), '', '', (1,1), (1,1), (3,1), '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (3,1), '', '', (1,1), '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), '', '', (3,1), '', '', (1,1), '', '', '', '', '', '', '', '', '', '', '', ''],
            #31-32
            [(1,1), (1,1), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), '', (3,1), '', '', (1,1), '', '', '', '', '', '', '', '', '', '', '', ''],
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1)]
        ]
            
        error = 0

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell != '' and self.gridSpan[i][j] == '':
                    print('gridspan need fixed at ' + str(i) + ',' + str(j))
                    error = 1

        if error == 1:
            exit()
                    
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
                    self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                    
                elif cell == '0':
                    self.addMaterialDialogLayout.addItem(QSpacerItem(self.columnWidth, self.rowHeight), i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                    
        self.widget = QWidget()
        self.widget.setLayout(self.addMaterialDialogLayout)
        
        self.setCentralWidget(self.widget)
        
        self.buildMainWindow()
        
    def currentDeviceChanged(self, device):
        deviceDict = {
            'Relay': [[1, 10],[(13, 1), (14, 1), (17, 1), (18, 1), (19, 1)]],
            'Test Switch': [[40, 49],[(7,1), (8, 1), (8, 3), (12, 3), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (20, 1), (20, 3)]],
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
            cordsx = i[0]
            cordsy = i[1]
            print(cordsx, cordsy)
            disableWidget = self.grid[cordsx][cordsy]
            disableWidget.setDisabled(True)
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
            
if  __name__ == "__main__":
    app = QApplication(sys.argv)
    application = AddMaterial()
    application.show()
    sys.exit(app.exec())