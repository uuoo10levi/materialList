import sys
from screeninfo import get_monitors
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QAbstractScrollArea, QSpinBox, QCheckBox, QInputDialog, QLabel, QGridLayout, QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem, QTabWidget
import json
import addmaterialfields


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import styles
from reportlab.pdfgen.canvas import Canvas

class GridLayoutCell():
    def __init__(self, type, row, column, value=''):
        
        self.type = type
        self.row = row
        self.column = column
        self.value = value

class ItemTab(QWidget):
    def __init__(self, fields={}):
        super().__init__()
        
        
        
        
        self.fields = fields
        
        self.itemTabLayout = QGridLayout()
        self.itemTabLayout.setSpacing(10)
        # self.itemTabLayout.columnCount(3)
        self.itemTabLayout.columnMinimumWidth(50)
        
        # for i, field in enumerate(self.fields):
            
            
        
         
        # for i, field in enumerate(self.fields.keys()):
        #     label = field
        #     widgettype = fields[field]['type']
        #     column = fields[field]['column']
        #     row = fields[field]['row']
            
        #     if 'columnspan' in list(fields[field].keys()):
        #         columnspan = fields[field]['columnspan']
        #         alignment = Qt.AlignCenter
        #     else:
        #         columnspan = 1
        #         alignment = Qt.AlignRight
        #     if 'rowspan' in list(fields[field].keys()):
        #         rowspan = fields[field]['rowspan']
        #     else:
        #         rowspan = 1
            
        #     Label = QLabel(label)
        #     Label.setAlignment(alignment)
            
                        
        #     editBox = widgettype
        #     # editBox.setStyleSheet('max-width: 200')
            
        #     self.itemTabLayout.addWidget(Label, row, (column * 2) + 1, 1, columnspan)
        #     self.itemTabLayout.addWidget(editBox, row, (column * 2) + 2, rowspan, columnspan)

        self.setLayout(self.itemTabLayout)
        

class AddMaterial(QMainWindow):
    def __init__(self):
        super(AddMaterial, self).__init__()

        self.addMaterialDialog = QDialog()
        self.addMaterialDialog.setWindowTitle('New Material List?')
        self.addMaterialDialog.setMinimumSize(800,800)
        self.addMaterialDialogLayout = QGridLayout()
        # self.addMaterialDialogLayout.setVerticalSpacing()
        self.addMaterialDialogLayout.setSpacing(5)
        # self.addMaterialDialogLayout.setSizeConstraint()
        # self.addMaterialDialogLayout.rowCount = 50
        
        
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
        
        # self.gridArray()
        # exit()
        
        self.grid = self.layoutGrid()
        
        # columnSpan = self.setColumnSpan(self.grid, 0, 5)
        # self.centralWidget(tabs)
        # self.addMaterialDialogLayout.addWidget(self.buildItemMainInfo(), 0,0)
        # self.addMaterialDialogLayout.addWidget(self.buildElectricalProperties(), 1,0)
        # self.addMaterialDialogLayout.addWidget(QLabel('Item No.'), 0, 0)
        
        # self.addMaterialDialogLayout.addWidget(QLabel('Item No.'), 0, 0)
        # self.addMaterialDialogLayout.addWidget(QLineEdit('0'), 0, 1)
        # self.addMaterialDialogLayout.addWidget(QLineEdit(), 0, 2)
        # self.addMaterialDialogLayout.addWidget(QLineEdit(), 0, 3)
        
        self.setWidgetToLayout(self.addMaterialDialogLayout, self.grid)
        
        self.widget = QWidget()
        self.widget.setLayout(self.addMaterialDialogLayout)
        
        self.setCentralWidget(self.widget)
        
        self.buildMainWindow()
        
    def gridArray(self):
        rows = 30
        columns = 30
        self.grid = []
        
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append([i,j])
            self.grid.append(row)
            
        print(self.grid)
        
    def layoutGrid(self):
        return [
            [[0,0,QLabel('Item No.')], [0,1,QLineEdit()], [0,2], [0,3,QLineEdit()], [0,4], [0,5,QLineEdit()], [0,6], [0,7,QLabel('Device Type')], [0, 8], [0, 9, QLabel('Major Functions')], [0, 10], [0, 11], [0, 12], [0, 13], [0, 14], [0, 15], [0, 16], [0, 17], [0, 18], [0, 19], [0, 20], [0, 21], [0, 22], [0, 23], [0, 24], [0, 25], [0, 26], [0, 27], [0, 28], [0, 29]],
            [[1, 0,QLabel('Manufacture')], [1, 1,QLineEdit()], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10], [1, 11], [1, 12], [1, 13], [1, 14], [1, 15], [1, 16], [1, 17], [1, 18], [1, 19], [1, 20], [1, 21], [1, 22], [1, 23], [1, 24], [1, 25], [1, 26], [1, 27], [1, 28], [1, 29]],
            [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10], [2, 11], [2, 12], [2, 13], [2, 14], [2, 15], [2, 16], [2, 17], [2, 18], [2, 19], [2, 20], [2, 21], [2, 22], [2, 23], [2, 24], [2, 25], [2, 26], [2, 27], [2, 28], [2, 29]],
            [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14], [3, 15], [3, 16], [3, 17], [3, 18], [3, 19], [3, 20], [3, 21], [3, 22], [3, 23], [3, 24], [3, 25], [3, 26], [3, 27], [3, 28], [3, 29]],
            [[4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15], [4, 16], [4, 17], [4, 18], [4, 19], [4, 20], [4, 21], [4, 22], [4, 23], [4, 24], [4, 25], [4, 26], [4, 27], [4, 28], [4, 29]],
            [[5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [5, 12], [5, 13], [5, 14], [5, 15], [5, 16], [5, 17], [5, 18], [5, 19], [5, 20], [5, 21], [5, 22], [5, 23], [5, 24], [5, 25], [5, 26], [5, 27], [5, 28], [5, 29]],
            [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8], [6, 9], [6, 10], [6, 11], [6, 12], [6, 13], [6, 14], [6, 15], [6, 16], [6, 17], [6, 18], [6, 19], [6, 20], [6, 21], [6, 22], [6, 23], [6, 24], [6, 25], [6, 26], [6, 27], [6, 28], [6, 29]],
            [[7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7], [7, 8], [7, 9], [7, 10], [7, 11], [7, 12], [7, 13], [7, 14], [7, 15], [7, 16], [7, 17], [7, 18], [7, 19], [7, 20], [7, 21], [7, 22], [7, 23], [7, 24], [7, 25], [7, 26], [7, 27], [7, 28], [7, 29]],
            [[8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7], [8, 8], [8, 9], [8, 10], [8, 11], [8, 12], [8, 13], [8, 14], [8, 15], [8, 16], [8, 17], [8, 18], [8, 19], [8, 20], [8, 21], [8, 22], [8, 23], [8, 24], [8, 25], [8, 26], [8, 27], [8, 28], [8, 29]],
            [[9, 0], [9, 1], [9, 2], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7], [9, 8], [9, 9], [9, 10], [9, 11], [9, 12], [9, 13], [9, 14], [9, 15], [9, 16], [9, 17], [9, 18], [9, 19], [9, 20], [9, 21], [9, 22], [9, 23], [9, 24], [9, 25], [9, 26], [9, 27], [9, 28], [9, 29]],
            [[10, 0], [10, 1], [10, 2], [10, 3], [10, 4], [10, 5], [10, 6], [10, 7], [10, 8], [10, 9], [10, 10], [10, 11], [10, 12], [10, 13], [10, 14], [10, 15], [10, 16], [10, 17], [10, 18], [10, 19], [10, 20], [10, 21], [10, 22], [10, 23], [10, 24], [10, 25], [10, 26], [10, 27], [10, 28], [10, 29]],
            [[11, 0], [11, 1], [11, 2], [11, 3], [11, 4], [11, 5], [11, 6], [11, 7], [11, 8], [11, 9], [11, 10], [11, 11], [11, 12], [11, 13], [11, 14], [11, 15], [11, 16], [11, 17], [11, 18], [11, 19], [11, 20], [11, 21], [11, 22], [11, 23], [11, 24], [11, 25], [11, 26], [11, 27], [11, 28], [11, 29]],
            [[12, 0], [12, 1], [12, 2], [12, 3], [12, 4], [12, 5], [12, 6], [12, 7], [12, 8], [12, 9], [12, 10], [12, 11], [12, 12], [12, 13], [12, 14], [12, 15], [12, 16], [12, 17], [12, 18], [12, 19], [12, 20], [12, 21], [12, 22], [12, 23], [12, 24], [12, 25], [12, 26], [12, 27], [12, 28], [12, 29]],
            [[13, 0], [13, 1], [13, 2], [13, 3], [13, 4], [13, 5], [13, 6], [13, 7], [13, 8], [13, 9], [13, 10], [13, 11], [13, 12], [13, 13], [13, 14], [13, 15], [13, 16], [13, 17], [13, 18], [13, 19], [13, 20], [13, 21], [13, 22], [13, 23], [13, 24], [13, 25], [13, 26], [13, 27], [13, 28], [13, 29]],
            [[14, 0], [14, 1], [14, 2], [14, 3], [14, 4], [14, 5], [14, 6], [14, 7], [14, 8], [14, 9], [14, 10], [14, 11], [14, 12], [14, 13], [14, 14], [14, 15], [14, 16], [14, 17], [14, 18], [14, 19], [14, 20], [14, 21], [14, 22], [14, 23], [14, 24], [14, 25], [14, 26], [14, 27], [14, 28], [14, 29]],
            [[15, 0], [15, 1], [15, 2], [15, 3], [15, 4], [15, 5], [15, 6], [15, 7], [15, 8], [15, 9], [15, 10], [15, 11], [15, 12], [15, 13], [15, 14], [15, 15], [15, 16], [15, 17], [15, 18], [15, 19], [15, 20], [15, 21], [15, 22], [15, 23], [15, 24], [15, 25], [15, 26], [15, 27], [15, 28], [15, 29]],
            [[16, 0], [16, 1], [16, 2], [16, 3], [16, 4], [16, 5], [16, 6], [16, 7], [16, 8], [16, 9], [16, 10], [16, 11], [16, 12], [16, 13], [16, 14], [16, 15], [16, 16], [16, 17], [16, 18], [16, 19], [16, 20], [16, 21], [16, 22], [16, 23], [16, 24], [16, 25], [16, 26], [16, 27], [16, 28], [16, 29]],
            [[17, 0], [17, 1], [17, 2], [17, 3], [17, 4], [17, 5], [17, 6], [17, 7], [17, 8], [17, 9], [17, 10], [17, 11], [17, 12], [17, 13], [17, 14], [17, 15], [17, 16], [17, 17], [17, 18], [17, 19], [17, 20], [17, 21], [17, 22], [17, 23], [17, 24], [17, 25], [17, 26], [17, 27], [17, 28], [17, 29]],
            [[18, 0], [18, 1], [18, 2], [18, 3], [18, 4], [18, 5], [18, 6], [18, 7], [18, 8], [18, 9], [18, 10], [18, 11], [18, 12], [18, 13], [18, 14], [18, 15], [18, 16], [18, 17], [18, 18], [18, 19], [18, 20], [18, 21], [18, 22], [18, 23], [18, 24], [18, 25], [18, 26], [18, 27], [18, 28], [18, 29]],
            [[19, 0], [19, 1], [19, 2], [19, 3], [19, 4], [19, 5], [19, 6], [19, 7], [19, 8], [19, 9], [19, 10], [19, 11], [19, 12], [19, 13], [19, 14], [19, 15], [19, 16], [19, 17], [19, 18], [19, 19], [19, 20], [19, 21], [19, 22], [19, 23], [19, 24], [19, 25], [19, 26], [19, 27], [19, 28], [19, 29]],
            [[20, 0], [20, 1], [20, 2], [20, 3], [20, 4], [20, 5], [20, 6], [20, 7], [20, 8], [20, 9], [20, 10], [20, 11], [20, 12], [20, 13], [20, 14], [20, 15], [20, 16], [20, 17], [20, 18], [20, 19], [20, 20], [20, 21], [20, 22], [20, 23], [20, 24], [20, 25], [20, 26], [20, 27], [20, 28], [20, 29]],
            [[21, 0], [21, 1], [21, 2], [21, 3], [21, 4], [21, 5], [21, 6], [21, 7], [21, 8], [21, 9], [21, 10], [21, 11], [21, 12], [21, 13], [21, 14], [21, 15], [21, 16], [21, 17], [21, 18], [21, 19], [21, 20], [21, 21], [21, 22], [21, 23], [21, 24], [21, 25], [21, 26], [21, 27], [21, 28], [21, 29]],
            [[22, 0], [22, 1], [22, 2], [22, 3], [22, 4], [22, 5], [22, 6], [22, 7], [22, 8], [22, 9], [22, 10], [22, 11], [22, 12], [22, 13], [22, 14], [22, 15], [22, 16], [22, 17], [22, 18], [22, 19], [22, 20], [22, 21], [22, 22], [22, 23], [22, 24], [22, 25], [22, 26], [22, 27], [22, 28], [22, 29]],
            [[23, 0], [23, 1], [23, 2], [23, 3], [23, 4], [23, 5], [23, 6], [23, 7], [23, 8], [23, 9], [23, 10], [23, 11], [23, 12], [23, 13], [23, 14], [23, 15], [23, 16], [23, 17], [23, 18], [23, 19], [23, 20], [23, 21], [23, 22], [23, 23], [23, 24], [23, 25], [23, 26], [23, 27], [23, 28], [23, 29]],
            [[24, 0], [24, 1], [24, 2], [24, 3], [24, 4], [24, 5], [24, 6], [24, 7], [24, 8], [24, 9], [24, 10], [24, 11], [24, 12], [24, 13], [24, 14], [24, 15], [24, 16], [24, 17], [24, 18], [24, 19], [24, 20], [24, 21], [24, 22], [24, 23], [24, 24], [24, 25], [24, 26], [24, 27], [24, 28], [24, 29]],
            [[25, 0], [25, 1], [25, 2], [25, 3], [25, 4], [25, 5], [25, 6], [25, 7], [25, 8], [25, 9], [25, 10], [25, 11], [25, 12], [25, 13], [25, 14], [25, 15], [25, 16], [25, 17], [25, 18], [25, 19], [25, 20], [25, 21], [25, 22], [25, 23], [25, 24], [25, 25], [25, 26], [25, 27], [25, 28], [25, 29]],
            [[26, 0], [26, 1], [26, 2], [26, 3], [26, 4], [26, 5], [26, 6], [26, 7], [26, 8], [26, 9], [26, 10], [26, 11], [26, 12], [26, 13], [26, 14], [26, 15], [26, 16], [26, 17], [26, 18], [26, 19], [26, 20], [26, 21], [26, 22], [26, 23], [26, 24], [26, 25], [26, 26], [26, 27], [26, 28], [26, 29]],
            [[27, 0], [27, 1], [27, 2], [27, 3], [27, 4], [27, 5], [27, 6], [27, 7], [27, 8], [27, 9], [27, 10], [27, 11], [27, 12], [27, 13], [27, 14], [27, 15], [27, 16], [27, 17], [27, 18], [27, 19], [27, 20], [27, 21], [27, 22], [27, 23], [27, 24], [27, 25], [27, 26], [27, 27], [27, 28], [27, 29]],
            [[28, 0], [28, 1], [28, 2], [28, 3], [28, 4], [28, 5], [28, 6], [28, 7], [28, 8], [28, 9], [28, 10], [28, 11], [28, 12], [28, 13], [28, 14], [28, 15], [28, 16], [28, 17], [28, 18], [28, 19], [28, 20], [28, 21], [28, 22], [28, 23], [28, 24], [28, 25], [28, 26], [28, 27], [28, 28], [28, 29]],
            [[29, 0], [29, 1], [29, 2], [29, 3], [29, 4], [29, 5], [29, 6], [29, 7], [29, 8], [29, 9], [29, 10], [29, 11], [29, 12], [29, 13], [29, 14], [29, 15], [29, 16], [29, 17], [29, 18], [29, 19], [29, 20], [29, 21], [29, 22], [29, 23], [29, 24], [29, 25], [29, 26], [29, 27], [29, 28], [29, 29]]
            ]
        
    def setWidgetToLayout(self, layout, grid):
        self.grid = grid
        self.gridLayout = layout
        
        for i,row in enumerate(self.grid):
            for j,cell in enumerate(row):
                if len(cell) != 2:
                    print(cell)
                    self.gridLayout.addWidget(cell[2], cell[0], cell[1], 1, self.setColumnSpan(self.grid, i, j))
                
        
    def setColumnSpan(self, grid, row, column):
        self.grid = grid
        self.row = grid[row]
        self.column = column
        self.columnSpan = 1
        looking = True
        # print(self.row[column:])
        
        while looking:
            if self.column + 1 + self.columnSpan == len(self.row): 
                looking = False
            elif len(self.row[column + self.columnSpan]) == 2:
                self.columnSpan += 1
            else:
                looking = False
        
    def buildMainWindow(self):
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xSize = int(self.monitorXSize*.4)
        self.ySize = int(self.monitorYSize*.6)
        self.xShift = int((self.monitorXSize - self.xSize) / 2)
        self.yShift = int((self.monitorYSize - self.ySize) / 2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Item to Master Material List')
        
    
        
        
if  __name__ == "__main__":
    app = QApplication(sys.argv)
    application = AddMaterial()
    application.show()
    sys.exit(app.exec())