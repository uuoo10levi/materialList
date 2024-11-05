from PyQt5.QtWidgets import QCheckBox, QSpinBox, QGridLayout, QApplication, QMainWindow, QWidget, QTableWidget, QLineEdit
import sys


class customTableWidgetItem(QWidget):
    def __init__(self,deviceNames=[]):
        super(customTableWidgetItem,self).__init__()
        self.layout1 = QGridLayout()
        self.countSelect = QSpinBox()
        self.countSelect.valueChanged.connect(self.updateDeviceNameSlots)
        self.layout1.addWidget(self.countSelect,0,0)
        

        self.countSelect.setValue(len(deviceNames))
        self.deviceNames = [QLineEdit() for i in range(self.countSelect.value())]
        for index, Name in enumerate(self.deviceNames):
            Name.setText(deviceNames[i])

        self.checkBox = QCheckBox()
        self.checkBox.clicked.connect(self.oneLot)
        self.checkBox.setText('1 LOT')
        self.layout1.addWidget(self.checkBox,0,1)
        
        self.widget = QWidget()
        self.widget.setLayout(self.layout1)
        self.setLayout(self.layout1)

    def updateDeviceNameSlots(self):
        for i in range(len(self.deviceNames)):
            self.layout1.removeWidget(self.deviceNames[i])
        self.deviceNames = [QLineEdit() for i in range(self.countSelect.value())]
        for i in range(self.countSelect.value()):
            self.layout1.addWidget(self.deviceNames[i],i+1,0,1,2)
    def oneLot(self):
        self.countSelect.setValue(0)
        self.updateDeviceNameSlots


app = QApplication(sys.argv)
application = QMainWindow()



cell = customTableWidgetItem()
table = QTableWidget()
table.setRowCount(2)
table.setColumnCount(2)


table.setCellWidget(1,1,cell)


application.setCentralWidget(table)


application.show()
sys.exit(app.exec())



