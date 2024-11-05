from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QVBoxLayout, QSlider
import sys

class Example(QWidget):

    def __init__(self,signalFunction,signalList):
        super().__init__()
        self.signalFunction = signalFunction
        self.signals = signalList

        self.initUI()


    #@QtCore.pyqtSlot(int)
    def on_sld_valueChanged(self, value):
        self.lcd.display(value)
        self.signals.signal1.emit()

    def pressed(self):
        self.signals.signal2.emit()

    def initUI(self):
        self.lcd = QLCDNumber(self)
        self.sld = QSlider(Qt.Horizontal, self)
        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)
        vbox.addWidget(self.sld)
        self.setLayout(vbox)

        self.sld.valueChanged.connect(self.on_sld_valueChanged)
        self.sld.sliderPressed.connect(self.pressed)
        self.signals.signal1.connect(self.printS)
        self.signals.signal2.connect(self.printV)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()
        
    
    def printS(self):
        print(self.signals.signal1)
        print(self.signalFunction)
    def printV(self):
        print(self.signalFunction)
        print('Hello')


class signals(QWidget):
    signal1 = pyqtSignal()
    signal2 = pyqtSignal()
    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    signalList = signals()
    ex = Example('emit',signalList)
    ex2 = Example('receive',signalList)
    sys.exit(app.exec_())