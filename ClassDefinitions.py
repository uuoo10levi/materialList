import sys
from screeninfo import get_monitors
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame, QApplication, QMainWindow, QDialog, QWidget, QTableWidget, QDockWidget, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QPlainTextEdit, QSpacerItem


class mainProgram(QMainWindow):
    def __init__(self):
        super(mainProgram, self).__init__()
        
        self.data = [["","","","","",""]]
        self.tableHeaders = ['Item No.','Description','Total','Panel B1','Panel B2', 'Panel B3']
        
        self.buildMainWindow()
        self.buildTable()   
        self.buildRightDock()



    def buildMainWindow(self):
        self.monitor = get_monitors()
        self.monitorXSize = int(self.monitor[0].width)
        self.monitorYSize = int(self.monitor[0].height)
        self.xShift = int(self.monitorXSize*.25)
        self.yShift = int(self.monitorYSize*.25)
        self.xSize = int(self.monitorXSize/2)
        self.ySize = int(self.monitorYSize/2)
        self.setGeometry(QtCore.QRect(self.xShift,self.yShift,self.xSize,self.ySize))
        self.setWindowTitle('Add Material to Contract')

    def buildTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(len(self.data[0])) 
        for i in range(len(self.data[0])):
            self.tableWidget.setColumnWidth(i,200)
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setHorizontalHeaderLabels(self.tableHeaders)
        self.tableWidget.itemChanged.connect(self.recordTableChange)
        self.setCentralWidget(self.tableWidget)
        self.refreshTable() 

    def recordTableChange(self, item):
        self.data[item.row()][item.column()] = item.text()

    def buildRightDock(self):
        self.dock = QDockWidget('Menu')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dockMenu = QWidget()
        self.dockLayout = QFormLayout(self.dockMenu)
        self.dockMenu.setLayout(self.dockLayout)
        self.fields = []
        for i in self.tableHeaders:
            field = QLineEdit(self.dockMenu)
            field.setPlaceholderText(i)
            self.fields.append(field)
            self.dockLayout.addRow(self.fields[-1])
        self.addButton = QPushButton('Add Entry', clicked=self.addEntry)
        self.dockLayout.addRow(self.addButton)
        self.deviceNames = QPlainTextEdit(self.dockMenu)
        self.dockLayout.addRow(self.deviceNames)
        self.spacer = QSpacerItem(50,200)
        self.dockLayout.addItem(self.spacer)
        self.dock.setWidget(self.dockMenu)

    def refreshTable(self):
        #Iterate over each entry
        for row in range(len(self.data)):
        #Iterate over each entry's data points
            for col in range(len(self.data[row])):
        #Make cell object
                tableWidgetItem = QTableWidgetItem(str(self.data[row][col]))
        #Hide cells in password column  
                # if self.tableHeaders[col] == 'Password':
                #     tableWidgetItem.setForeground(QtGui.QBrush(QtGui.QColor(255,255,255)))
        #Add cell to table
                self.tableWidget.setItem(row, col, tableWidgetItem)

    def addEntry(self):
        validInput = True
        for i in self.fields:
            if i.text() == '':
                validInput = False
        if validInput:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.data.append([i.text() for i in self.fields])
            for i in self.fields:
                i.setText('')
        self.refreshTable()



if  __name__ == "__main__":
    app = QApplication([])
    application = mainProgram()
    application.show()
    sys.exit(app.exec())