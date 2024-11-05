from PyQt5.QtWidgets import QCheckBox, QSpinBox, QGridLayout, QApplication, QMainWindow, QWidget, QTableWidget, QLineEdit
import sys

  
class customTableWidgetItem(QWidget):
    def __init__(self,deviceNames=['Test']):
        super(customTableWidgetItem,self).__init__()
        self.layout1 = QGridLayout()
        self.countSelect = QSpinBox()
        self.checkBox = QCheckBox()
        self.widget = QWidget()
        self.oneLotSelected = False

        
        

        self.countSelect.setValue(len(deviceNames))
        self.deviceNames = [QLineEdit() for i in deviceNames]
        for i in range(len(deviceNames)):
            self.deviceNames[i].setText(deviceNames[i])
        
        for index in range(len(self.deviceNames)):
            print(deviceNames[index])
            self.deviceNames[index].setText(deviceNames[index])



        self.countSelect.valueChanged.connect(self.updateDeviceNameSlots)
        self.checkBox.clicked.connect(self.oneLot)
        self.checkBox.setText('1 LOT')


        self.layout1.addWidget(self.countSelect,0,0)
        self.layout1.addWidget(self.checkBox,0,1)
        for i in range(self.countSelect.value()):
            self.layout1.addWidget(self.deviceNames[i],i+1,0,1,2)
        
        
        self.widget.setLayout(self.layout1)
        self.setLayout(self.layout1)

    def updateDeviceNameSlots(self):
        while self.countSelect.value() != len(self.deviceNames):
            if self.countSelect.value() > len(self.deviceNames):
                self.addDeviceNameSlot()
            if self.countSelect.value() < len(self.deviceNames):
                self.removeDeviceNameSlot()

    def addDeviceNameSlot(self):
        self.deviceNames.append(QLineEdit())
        self.layout1.addWidget(self.deviceNames[-1],len(self.deviceNames)+1,0,1,2)
        if self.oneLotSelected:
            self.countSelect.setValue(0)
            self.deviceNames = []


    def removeDeviceNameSlot(self):
        self.layout1.removeWidget(self.deviceNames[-1])
        self.deviceNames.pop()
        

    def oneLot(self):
        self.oneLotSelected = self.checkBox.isChecked()
        if self.oneLotSelected:
            for i in reversed(range(len(self.deviceNames))):
                self.layout1.removeWidget(self.deviceNames[i])
            self.countSelect.setValue(0)
            self.updateDeviceNameSlots()


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



