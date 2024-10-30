from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import styles

import json

# print(contract['material'])
# def add_items(lst, item, value):
#     add = True
#     for row in lst:
#         for cell in row:
#             if cell == item:
#                 sublist = lst[lst.index(row)]
#                 sublist.append(value)
#                 add = False
                
#     if add:
#         lst.append([item, value])
#     return lst

def comparelist (lst1, lst2):
    counter = 0
    for i in [0, 1, 2]:
        if lst1[i] == lst2[i]:
            counter += 1
            
    if counter == 3:
        return True
    else:
        return False
    
def itemnumberfromlist (lst):
    return str(lst[0]) + lst[1] + lst[2]
            

class PanelObjects:
    def __init__(self, id='', name=''):
        self.items = []
        self.id = id
        self.name = name
        
    # def addItem(self,item):
    #     self.items.append(item)
    
    
class Items:
    def __init__(self, itemtype=[], count=1, names=[]):
        self.count = count
        self.names = names
        self.itemtype = itemtype
        
        if type(names) is int:
            self.names = ['' for i in range(names)]
            
        
        self.itemtype[0] = int(self.itemtype[0])
        
    def addName(self,name):
        self.names.append(name)
        self.count = len(self.names)

class pdf:
    def __init__(self, data, name = '_.pdf'):
        
        self.styleSheet = getSampleStyleSheet()
        self.pagesize = (11 * inch, 8.5 * inch)  # 20 inch width and 10 inch height.doc = SimpleDocTemplate('sample.pdf', pagesize=pagesize)
        self.customstyle1 = ParagraphStyle(name='BodyText', parent=self.styleSheet['BodyText'], spaceBefore=6, alignment=1)
        self.doc = SimpleDocTemplate(name, pagesize=self.pagesize)
        self.elements = []

        for i in range(len(data[0])):
            data[0][i] = Paragraph(data[0][i], self.customstyle1)
        
        self.pdftable = Table(data, colWidths= 100, style=[
            ('BOX',(0,0),(-1,-1),1,colors.black),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'TOP')]
                              )

        self.elements.append(self.pdftable)

    def exportPDF(self):
        self.doc.build(self.elements)
        

with open('R:\Python\Relaying Database\json\contract.json', 'r') as file:
    contract = json.load(file)

panelList = [PanelObjects(i,name=contract['panels'][i]) for i in contract['panels'].keys()]

for j in panelList:
    itemList = [Items(i.split('-'),names=contract['material'][j.id][i]) for i in contract['material'][j.id].keys()]
    for i in range(len(itemList)):
        itemList[i].count = len(itemList[i].names)
    panelList[int(j.id)].items = itemList


headers = ['Item Number', 'Description', 'Total']

for i in range(len(panelList)):
    headers.append(panelList[i].name)

masterList = []
    
for i in panelList:
    for j in i.items:
        if j.itemtype not in masterList:
            masterList.append(j.itemtype)

masterList.sort()
grid = [[0 for j in range(len(panelList)+3)] for i in range(len(masterList)+2)]


for panel in range(len(panelList)):
    
    for item in range(len(panelList[panel].items)):
        
        for item2 in range(len(masterList)):
            
            if comparelist(panelList[panel].items[item].itemtype, masterList[item2]):
                grid[item2+1][0] = str(masterList[item2][0]) + ''.join(masterList[item2][1:2])
                # print(panelList[panel].items[item].names['names'])
                grid[item2+1][panel+3] = str(len(panelList[panel].items[item].names['names'])) + '\n' + '\n'.join(panelList[panel].items[item].names['names'])
                # grid[item2+2][panel+3] = panelList[panel].items[item]["count"] + '\n' + '\n'.join(panelList[panel].items[item]["names"].names)
                # grid[item2+2][panel+3] = grid[item2+2][panel+3].rstrip('\n')

for row in range(len(grid)):
    count = 0
    for column in range(2,len(grid[row])):
        print(grid[row][column])
        count += int(str(grid[row][column]).split('\n')[0])
        grid[row][2] = count
                    
grid[0] = headers

# print(grid)

matList = pdf(grid, 'TST.pdf')
matList.exportPDF()