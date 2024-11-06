import sys
from PyQt5.QtWidgets import *

fakeapp = QApplication(sys.argv)


data = {
    #tab
    0: {
        'tabname': 'Relay',
        'rows': {
            0: {
                #column
                0: {
                    'type': QLabel(),
                    'text': 'Item No.'
                },
                1: {
                    'type': QLineEdit(),
                    'text': '0'
                },
                2: {
                    'type': QLineEdit()
                },
                3: {
                    'type': QLineEdit()
                },
                4: {
                    'type': QLabel(),
                    'text': 'Major Functions'
                },
                5: {
                    'type': QLabel(),
                    'text': 'Inventory',
                    'rowspan': 2
                }
            },
            #row
            1: {
                #column
                0: {
                    0: {
                        'type': QLabel(),
                        'text': 'Manufacture'
                    },
                    1: {
                        'type': QLineEdit(),
                        'rowspan': 3
                    },
                    5: {
                        'type': QPlainTextEdit()
                    },
                    6: {
                        'type': QLabel(),
                        'text': 'Qty'
                    },
                    7: {
                        'type': QLineEdit()
                    }
                }
            },
        #row
        2: {
            #column
            0:{
                0:{
                    'type': QLabel(),
                    'text': 'Series'
                },
                1:{
                    'type': QLineEdit(),
                    'rowspan': 3
                },
                6:{
                    'type': QLabel(),
                    'text': 'Location',
                    'rowspan': 2
                },
            }
        }
    }
    },
    #tab
    1: {
        'tabname': 'Test Switch',
            #row
            0:{
                #column
                0:{
                    'type': QLabel(),
                    'text': 'Itemn No.'
                }
            }
    }
}


# data = {
#             'Relay': {
#                 'Item No.': {
#                 'type': QLineEdit(),
#                 'column': 0,
#                 'row': 0
#             },
            
#             'Manufacture': {
#                 'type': QLineEdit(),
#                 'column': 0,
#                 'row': 1
#             },
#             'Part Number': {
#                 'type': QLineEdit(),
#                 'column': 0,
#                 'row': 2
#             },
#             'Electrical Properties': {
#                 'type': QLabel(),
#                 'column': 0,
#                 'row': 4,
#                 'columnspan': 2
#             },
#             'Power Supply Voltage': {
#                     'type': QLineEdit(),
#                     'column':  0,
#                     'row': 5,
#                     'columnspan': 3
#                 },
#             'Control Voltage': {
#                     'type': QComboBox(),
#                     'column':  0,
#                     'row': 6
#                 },
#             'AC Current Input': {
#                     'type': QLineEdit(),
#                     'column':  0,
#                     'row': 7
#                 },
#             'AC Voltage Input': {
#                     'type': QLineEdit(),
#                     'column':  0,
#                     'row': 8
#                 },
#             'Zones of Protection': {
#                     'type': QLineEdit(),
#                     'column':  0,
#                     'row': 9
#                 },
#             'Coil Operation Voltage': {
#                     'type': QLineEdit(),
#                     'column':  0,
#                     'row': 10
#                 },
#             'Reset': {
#                     'type': QComboBox(),
#                     'column':  0,
#                     'row': 11
#                 },
#             'Meter Form': {
#                     'type': QComboBox(),
#                     'column':  0,
#                     'row': 12
#                 },
#             'Number of Phase': {
#                     'type': QSpinBox(),
#                     'column':  0,
#                     'row': 13
#                 },
#             'Number of Wires': {
#                     'type': QSpinBox(),
#                     'column':  0,
#                     'row': 14
#                 },
#             'Physical Properties': {
#                     'type': QLabel(),
#                     'column':  0,
#                     'row': 15
#                 },
#             'Orientation': {
#                     'type': QComboBox(),
#                     'column':  0,
#                     'row': 16
#                 },
#             'Mounting': {
#                     'type': QComboBox(),
#                     'column':  0,
#                     'row': 17
#                 },
#             'Rack Units': {
#                     'type': QSpinBox(),
#                     'column':  0,
#                     'row': 18
#                 },
#             'User Interface': {
#                     'type': QComboBox(),
#                     'column':  0,
#                     'row': 19
#                 },
#                 #Column 4
#             'Major Functions': {
#                 'type': QPlainTextEdit(),
#                 'column': 4,
#                 'row': 0,
#                 'rowspan': 2
#             },
#             'I/O Details': {
#                     'type': QLabel(),
#                     'column': 4,
#                     'row': 4,
#                     'columnspan': 2
#                 },
#             'Standard I/O': {
#                     'type': QLabel(),
#                     'column': 4,
#                     'row': 5,
#                     'columnspan': 2
#                 },
#             'Standard Inputs A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 6
#                 },
#             'Standard Inputs B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 7
#                 },
#             'Standard Outputs A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 8
#                 },
#             'Standard Outputs B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 9
#                 },
#             'Addition I/O 1': {
#                     'type': QLabel(),
#                     'column': 4,
#                     'row': 10,
#                     'columnspan': 2
#                 },
#             'Addition Inputs 1A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 11
#                 },
#             'Addition Inputs 1B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 12
#                 },
#             'Addition Outputs 1A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 13
#                 },
#             'Addition Outputs 1B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 14
#                 },
#             'Addition I/O 2': {
#                     'type': QLabel(),
#                     'column': 4,
#                     'row': 15,
#                     'columnspan': 2
#                 },
#             'Addition Inputs 2A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 16
#                 },
#             'Addition Inputs 2B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 17
#                 },
#             'Addition Outputs 2A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 18
#                 },
#             'Addition Outputs 2B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 19
#                 },
#             'Addition I/O 3': {
#                     'type': QLabel(),
#                     'column': 4,
#                     'row': 20,
#                     'columnspan': 2
#                 },
#             'Addition Inputs 3A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 21
#                 },
#             'Addition Inputs 3B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 22
#                 },
#             'Addition Outputs 3A': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 23
#                 },
#             'Addition Outputs 3B': {
#                     'type': QLineEdit(),
#                     'column': 4,
#                     'row': 24
#                 },
#                 'Catalog cut included': {
#                     'type': QCheckBox(),
#                     'column': 4,
#                     'row': 25
#                 },
#                 'Photo on file': {
#                     'type': QCheckBox(),
#                     'column': 4,
#                     'row': 26
#                 },
#                 'Check for this on each contract': {
#                     'type': QCheckBox(),
#                     'column': 4,
#                     'row': 27
#                 }
            
#             },
#             'Test Switch': {
#              'Item No.': {
#                 'type': QLineEdit(),
#                 'column': 0,
#                 'row': 0
#             },
#              'Test Switch Arrangement A': {
#                 'type': QComboBox(),
#                 'column': 0,
#                 'row': 1
#             }
#             },
#             'Lock Out Relay': {
#              'Item No.': {
#                 'type': QLineEdit(),
#                 'column': 0,
#                 'row': 0
#             },
#              'Decks': {
#                 'type': QSpinBox(),
#                 'column': 0,
#                 'row': 1
#             }   
#             },
            
#         }