import sys
from screeninfo import get_monitors
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QAbstractScrollArea, QSpinBox, QCheckBox, QInputDialog, QLabel, QGridLayout, QComboBox, QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem, QTabWidget
import json


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import styles
from reportlab.pdfgen.canvas import Canvas

class ItemTab(QWidget):
    def __init__(self, fields={}):
        super().__init__()
        
        
        
        
        self.fields = fields
        
        self.itemTabLayout = QGridLayout()
        self.itemTabLayout.setSpacing(10)
        # self.itemTabLayout.columnCount(3)
        self.itemTabLayout.columnMinimumWidth(50)
        
        
         
        for i, field in enumerate(self.fields.keys()):
            label = field
            widgettype = fields[field]['type']
            column = fields[field]['column']
            row = fields[field]['row']
            
            if 'columnspan' in list(fields[field].keys()):
                columnspan = fields[field]['columnspan']
                alignment = Qt.AlignCenter
            else:
                columnspan = 1
                alignment = Qt.AlignRight
            
            Label = QLabel(label)
            Label.setAlignment(alignment)
                        
            editBox = widgettype
            editBox.setStyleSheet('max-width: 200')
            
            self.itemTabLayout.addWidget(Label, row, (column * 2) + 1, 1, columnspan)
            self.itemTabLayout.addWidget(editBox, row, (column * 2) + 2)

        self.setLayout(self.itemTabLayout)
        

class AddMaterial(QMainWindow):
    def __init__(self):
        super(AddMaterial, self).__init__()

        self.addMaterialDialog = QDialog()
        self.addMaterialDialog.setWindowTitle('New Material List?')
        self.addMaterialDialog.setMinimumSize(800,800)
        self.addMaterialDialogLayout = QGridLayout()
        
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
        
        # self.centralWidget(tabs)
        # self.addMaterialDialogLayout.addWidget(self.buildItemMainInfo(), 0,0)
        # self.addMaterialDialogLayout.addWidget(self.buildElectricalProperties(), 1,0)
        
        self.widget = QWidget()
        self.widget.setLayout(self.addMaterialDialogLayout)
        self.setCentralWidget(self.widget)
        
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)
        
        # for color in ['red', 'blue', 'green', 'yellow']:
            # tabs.addTab(Color(color), color)
        self.tabs = {
            'Relay': {
                'Item No.': {
                'type': QLineEdit(),
                'column': 0,
                'row': 0
            },
            'Manufacture': {
                'type': QLineEdit(),
                'column': 0,
                'row': 1
            },
            'Part Number': {
                'type': QLineEdit(),
                'column': 0,
                'row': 2
            },
            'Electrical Properties': {
                'type': QLabel(),
                'column': 0,
                'row': 4,
                'columnspan': 2
            },
            'Power Supply Voltage': {
                    'type': QLineEdit(),
                    'column':  0,
                    'row': 5
                },
            'Control Voltage': {
                    'type': QComboBox(),
                    'column':  0,
                    'row': 6
                },
            'AC Current Input': {
                    'type': QLineEdit(),
                    'column':  0,
                    'row': 7
                },
            'AC Voltage Input': {
                    'type': QLineEdit(),
                    'column':  0,
                    'row': 8
                },
            'Zones of Protection': {
                    'type': QLineEdit(),
                    'column':  0,
                    'row': 9
                },
            'Coil Operation Voltage': {
                    'type': QLineEdit(),
                    'column':  0,
                    'row': 10
                },
            'Reset': {
                    'type': QComboBox(),
                    'column':  0,
                    'row': 11
                },
            'Meter Form': {
                    'type': QComboBox(),
                    'column':  0,
                    'row': 12
                },
            'Number of Phase': {
                    'type': QSpinBox(),
                    'column':  0,
                    'row': 13
                },
            'Number of Wires': {
                    'type': QSpinBox(),
                    'column':  0,
                    'row': 14
                },
            'Physical Properties': {
                    'type': QLabel(),
                    'column':  0,
                    'row': 15
                },
            'Orientation': {
                    'type': QComboBox(),
                    'column':  0,
                    'row': 16
                },
            'Mounting': {
                    'type': QComboBox(),
                    'column':  0,
                    'row': 17
                },
            'Rack Units': {
                    'type': QSpinBox(),
                    'column':  0,
                    'row': 18
                },
            'User Interface': {
                    'type': QComboBox(),
                    'column':  0,
                    'row': 19
                },
            #Column 2
            'I/O Details': {
                    'type': QLabel(),
                    'column':  1,
                    'row': 4,
                    'columnspan': 2
                },
            'Standard I/O': {
                    'type': QLabel(),
                    'column':  1,
                    'row': 5,
                    'columnspan': 2
                }
            
            },
            'Test Switch': {
             'Item No.': {
                'type': QLineEdit(),
                'column': 0,
                'row': 0
            },
             'Test Switch Arrangement A': {
                'type': QComboBox(),
                'column': 0,
                'row': 1
            }
            },
            'Lock Out Relay': {
             'Item No.': {
                'type': QLineEdit(),
                'column': 0,
                'row': 0
            },
             'Decks': {
                'type': QSpinBox(),
                'column': 0,
                'row': 1
            }   
            },
            
        }
        
        for i, tab in enumerate(self.tabs.keys()):
            tabs.addTab(ItemTab(self.tabs[tab]), tab)
        
        self.buildMainWindow()
        self.setCentralWidget(tabs)
        # self.setCentralWidget(self.columnA)
        # self.addMaterialDialogLayout.addWidget(self.buildColumnA())
        
    def buildMainWindow(self):
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xSize = int(self.monitorXSize*.4)
        self.ySize = int(self.monitorYSize*.4)
        self.xShift = int((self.monitorXSize - self.xSize) / 2)
        self.yShift = int((self.monitorYSize - self.ySize) / 2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Item to Master Material List')
        
        
if  __name__ == "__main__":
    app = QApplication(sys.argv)
    application = AddMaterial()
    application.show()
    sys.exit(app.exec())