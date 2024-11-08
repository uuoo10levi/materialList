import sys
from screeninfo import get_monitors
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAbstractScrollArea, QSpinBox, QCheckBox, QInputDialog, QLabel, QGridLayout, QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem, QTabWidget, QListWidget

# class QComboBox(QComboBox):
#         def __init__(self, parent=None, flag=''):
#             super().__init__(parent)
#             self.flag = flag
#             if self.flag == 'change':
#                 self.setStyleSheet('background: rgb(150,150,150)')

class CQLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.objType = 'label'
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet('background: rgb(150,150,150)')
        
# class CQSpacerItem(QSpacerItem):
#     def __init__(self, parent=None):
#         super().__init__(parent)
        
class AddMaterial(QMainWindow):
    def __init__(self):
        super(AddMaterial, self).__init__()

        self.addMaterialDialog = QDialog()
        self.addMaterialDialog.setWindowTitle('New Material List?')
        self.addMaterialDialog.setMinimumSize(800,800)
        self.addMaterialDialogLayout = QGridLayout()

        self.addMaterialDialogLayout.setSpacing(5)
        
        self.displayGrid = False        
        self.gridCoords = []
        
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
        self.xSize = self.monitorXSize * .8
        'Defines width of window'
        self.ySize = self.monitorYSize * .8
        'Defines height of window'
        
        self.deviceItemNumber = QComboBox(self)
        self.deviceType = QListWidget(self)
        
        self.deviceType.addItems(['Relay','Test Switch','Lock Out Relay','Control Switch'])
        self.deviceType.currentItemChanged.connect(self.currentDeviceChanged)
        
        self.grid = [
            #0-4
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            [QLabel('Item No.'), self.deviceItemNumber, QLineEdit(), QLineEdit(), CQLabel('Device Type'), '1,5', '1,6', CQLabel('Major Functions'), '1,8', '1,9', '1,10', '1,11', CQLabel('Inventory'), '1,13'],
            [QLabel('Manufacture'), QLineEdit(), '2,2', '2,3', self.deviceType, '2,5', '2,6', QPlainTextEdit(), '2,8', '2,9', '2,10', '2,11', QLabel('Qty.'), QLineEdit()],
            [QLabel('Series'), QLineEdit(),'3,2', '3,3', '3,4', '3,5', '3,6', '3,7', '3,8', '3,9', '3,10', '3,11', '3,12', '3,13'],
            [QLabel('Part Number'), QLineEdit(),'4,2', '4,3', '4,4', '4,5', '4,6', '4,7', '4,8', '4,9', '4,10', '4,11', '4,12', '4,13'],
            #5-10
            ['0', '5,1', '5,2', '5,3', '5,4', '5,5', '5,6', '5,7', '5,8', '5,9', '5,10', '5,11', '5,12', '5,13'],
            [CQLabel('Electrical Properties'), '6,1', '6,2', '6,3', CQLabel('I/O Details'), '6,5', '6,6', '6,7', '6,8', CQLabel('Communications'), '6,10', '6,11', '6,12', '6,13'],
            [QLabel('Power Supply Voltage'), QComboBox(), '7,2', '7,3', CQLabel('Standard I/O'), '7,5', '7,6', '7,7', '7,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '7,12', '7,13'],
            [QLabel('Control Voltage'), QLineEdit(), QLabel('V'), QComboBox(), QLabel('Standard Inputs'), QSpinBox(), QComboBox(), '8,7', '8,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '8,12', '8,13'],
            [QLabel('AC Current Input'), QLineEdit(), '9,2', '9,3', QLabel('Standard Inputs'), QSpinBox(), QComboBox(),'9,7', '9,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '9,12', '9,13'],
            [QLabel('AC Voltage Input'), QLineEdit(), QLabel('V AC'), '10,3', QLabel('Standard Outputs'), QSpinBox(), QComboBox(), '10,7', '10,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '10,12', '10,13'],
            #11-15
            [QLabel('Zones of Protection'), QSpinBox(), '11,2', '11,3', QLabel('Standard Outputs'), QSpinBox(), QComboBox(), '11,7', '11,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '11,12', '11,13'],
            [QLabel('Coil Operation Volt.'), QLineEdit(), QLabel('V'), QComboBox(), CQLabel('Additional I/O Set 1'), '12,5', '12,6', '12,7', '12,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '12,12', '12,13'],
            [QLabel('Reset'), QComboBox(), '13,2', '13,3', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '13,7', '13,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '13,12', '13,13'],
            [QLabel('Meter Form'), QComboBox(), '14,2', '14,3', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '14,7', '14,8', QLabel('Comm. Interface'), QSpinBox(), QComboBox(), '14,12', '14,13'],
            [QLabel('Number of Phases'), QSpinBox(), '15,2', '15,3', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '15,7', '15,8', QLabel('Commumincations<br/>Protocols'), QPlainTextEdit(), '15,13'],
            #16-20
            [QLabel('Number of Wires'), QSpinBox(), '16,2', '16,3', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '16,7', '16,8', '16,9', '16,10', '16,11', '16,12', '16,13'],
            [QLabel('Test Switch Arr. A'), QComboBox(), '17,2', '17,3,', CQLabel('Additional I/O Set 2'), '17,5', '17,6', '17,7', '17,8', QLabel('Material Status'), '17,10', '17,11', '17,12', '17,13'],
            [QLabel('Test Switch Arr. B'), QComboBox(), '18,2', '18,3', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '18,7', '18,8', QComboBox(), '18,10', '18,11', '18,12', '18,13'],
            [QLabel('Test Switch Arr. C'), QComboBox(), '19,2', '19,3', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '19,7', '19,8', '19,9', '19,10', '19,11', '19,12', '19,13'],
            [QLabel('Lamp Voltage'), QComboBox(), QLabel('V'), QComboBox(), QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '20,7', '20,8', '20,9', '20,10', '20,11', '20,12', '20,13'],
            #21-25
            [CQLabel('Physcial Properties'), '21,1', '21,2', '21,3', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '21,7', '21,8', '21,9', '21,10', '21,11', '21,12', '21,13'],
            [QLabel('Orientation'), QComboBox(), '22,2', '22,3', CQLabel('Additional I/O Set 3'), '22,5', '22,6', '22,7', '22,8', '22,9', '22,10', '22,11', '22,12', '22,13'],
            [QLabel('Mounting'), QComboBox(), '23,2', '23,3', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '23,7', '23,8', '23,9', '23,10', '23,11', '23,12', '23,13'],
            [QLabel('Rack Units'), QSpinBox(), '24,2', '24,3', QLabel('Additional Inputs'), QSpinBox(), QComboBox(), '24,7', '24,8', '24,9', '24,10', '24,11', '24,12', '24,13'],
            [QLabel('User Interface'), QComboBox(), '25,2', '25,3', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '25,7', '25,8', '25,9', '25,10', '25,11', '25,12', '25,13'],
            #26-30
            [QLabel('Handle Style'), QComboBox(), '26,2', '26,3', QLabel('Additional Outputs'), QSpinBox(), QComboBox(), '26,7', '26,8', '26,9', '26,10', '26,11', '26,12', '26,13'],
            [QLabel('Action'), QComboBox(), '27,2', '27,3', '27,4', '27,5', '27,6', '27,7', '27,8', '27,9', '27,10', '27,11', '27,12', '27,13'],
            [QLabel('Decks'), QSpinBox(), '28,2', '28,3', QLabel('Catalog cut included'), '28,5', '28,6', QCheckBox(), '28,8', '28,9', '28,10', '28,11', '28,12', '28,13'],
            [QLabel('Test Switch Cover'), QComboBox(), '29,2', '29,3', '29,4', '29,5', '29,6', '29,7', '29,8', '29,9', '29,10', '29,11', '29,12', '29,13'],
            [QLabel('Lamp Color'), QComboBox(), '30,2', '30,3', QLabel('Photo on file'), '30,5', '30,6', QCheckBox(), '30,8', '30,9', '30,10', '30,11', '30,12', '30,13'],
            #31-32
            [QLabel('Lens Color'), QComboBox(), '31,2', '31,3', '31,4', '31,5', '31,6', '31,7', '31,8', '31,9', '31,10', '31,11', '31,12', '31,13'],
            [QLabel('Length'), QLineEdit(), QComboBox(), '32,4', QLabel('Check for the on each contract'), '32,6', '32,7', QCheckBox(), '32,9', '32,10', '32,11', '32,12', '32,13'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        ]
        
        self.gridSpan = [
            #  0      1      2      3      4      5      6      7      8      9      10     11     12     13
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1)],
            [(1,1), (1,1), (1,1), (1,1), (3,1),    '',    '', (5,1),    '',    '',    '',    '', (2,1),    ''],
            [(1,1), (3,1),    '',    '', (3,3),    '',    '', (5,3),    '',    '',    '',    '', (1,1), (1,1)],
            [(1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            #5-10
            [(1,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(4,1),    '',    '',    '', (5,1),    '',    '',    '',    '', (5,1),    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (5,1),    '',    '',    '',    '', (1,1), (1,1), (3,1),    '',    ''],
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (3,1), (1,1), (1,3), (1,1), (1,1), (3,1),    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    ''],
            [(1,1), (1,1), (1,1),    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    ''],
            #11-15
            [(1,1), (1,1),    '', (1,1), (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    ''],
            [(1,1), (1,1), (1,1), (1,1), (5,1),    '',    '',    '',    '', (1,1), (1,1), (3,1),    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,2), (5,12),    '',    '',    ''],
            #16-20
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (5,1),    '',    '',    '',    '', (1,1),    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '', (1,1),    '',    '',    '',    ''],
            [(1,1), (3,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            #21-25
            [(4,1),    '',    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (5,1),    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            #26-30
            [(1,1), (1,1),    '',    '', (1,1), (1,1), (3,1),    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (3,1),    '',    '', (1,1),    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1),    '',    '', (3,1),    '',    '', (1,1),    '',    '',    '',    '',    '',    ''],
            #31-32
            [(1,1), (1,1),    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1), (1,1),    '', (3,1),    '',    '', (1,1),    '',    '',    '',    '',    '',    ''],
            [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1)]
        ]
            
        # error = 0

        # for i, row in enumerate(self.grid):
        #     for j, cell in enumerate(row):
        #         if type(cell) == type('') and type(self.gridSpan[i][j]) == type((0,0)):
        #             print('gridspan need fixed at ' + str(i) + ',' + str(j))
        #             error = 1

        # if error == 1:
        #     exit()
                    
        self.columnWidth = int(self.xSize / len(self.grid[0]))
        self.rowHeight = int(self.ySize / len(self.grid))
        
        for i,row in enumerate(self.grid):
                for j,cell in enumerate(row):
                    # if cell not in ['', '0']:
                    if type(cell) != type(''):
                        self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                        
                    elif cell == '0':
                        self.addMaterialDialogLayout.addItem(QSpacerItem(self.columnWidth, self.rowHeight), i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                            
        self.widget = QWidget()
        self.widget.setLayout(self.addMaterialDialogLayout)
        
        self.setCentralWidget(self.widget)
        
        self.buildMainWindow()
        
    def currentDeviceChanged(self, device):
        deviceDict = {
            'Relay': [[1, 10],[(13, 1), (14, 1), (17, 0), (17, 1), (18, 0), (18, 1), (19, 0), (19, 1)]],
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
                if type(cell) != type():
                    cell.setDisabled(False)
                    cell.setHidden(False)
                    self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                    
        for i in hideFieldCords:
            cordsx = i[0]
            cordsy = i[1]
            print(cordsx, cordsy)
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
        
    def keyPressEvent(self, event):
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
                    print(i)
                    i.setHidden(True)
                    i.setStyleSheet('color: rgb(200,200,200); border: 1px solid rgb(200,200,200)')
                    # self.addMaterialDialogLayout.addWidget(i, i, j)
                    
                    self.columnSpan = 1
        
            for i,row in enumerate(self.grid):
                for j,cell in enumerate(row):
                    if type(cell) != type(''):
                        self.addMaterialDialogLayout.addWidget(cell, i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
                    elif cell == '0':
                        self.addMaterialDialogLayout.addItem(QSpacerItem(self.columnWidth, self.rowHeight), i, j, self.gridSpan[i][j][1], self.gridSpan[i][j][0])
            
            
if  __name__ == "__main__":
    app = QApplication(sys.argv)
    application = AddMaterial()
    application.show()
    sys.exit(app.exec())