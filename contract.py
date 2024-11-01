from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import styles

import json

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
    def __init__(self, id='', name='', description='', items=''):
        self.items = items
        self.id = id
        self.name = name
        self.description = description
        
    # def __str__(self):
    #     return f'id: {self.id}\nname: {self.name}\ndescription: {self.description}'
        
    # def addItem(self,item):
    #     self.items.append(item)
    
    
class Items:
    def __init__(self, itemno='', description='', count=1, names=[]):
        self.count = count
        self.names = names
        self.itemno = itemno
        self.description = description
        
        # if type(names) is int:
        #     self.names = ['' for i in range(names)]
            
        
        # self.itemno[0] = int(self.itemno[0])
        
    # def __str__(self):
    #     return f'count: {self.count}\nnames: {self.names}\nitemno: {self.itemno}\ndescription: {self.description}'
        
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
        

with open('contract.json', 'r') as file:
    contract = json.load(file)

panelList = [PanelObjects(i,name=name) for i, name in enumerate(contract)]


for i,obj in enumerate(panelList):
    obj.description = contract[obj.name]['description']


def filterdesc(var):
    filters = ['description']
    if (var not in filters):
        return True
    else:
        return False
    
projectList = []

# for i, panel in enumerate(panelList):
#     # print(panelList[i].keys())
#     # print(contract[panel.name].items())
#     for i, item in enumerate(contract[panel.name]):
#         panelitemlist = [item]
#         if item != 'description':
#             panelitemlist.append(contract[panel.name][item])
#         if item != 'description':
#             projectList.append(panelitemlist)

print(panelList)

for j, pnlobj in enumerate(panelList):
    pnlname = pnlobj.name
    itemList = [Items(itemno=i,description=contract[pnlname][i]['description'],count=contract[pnlname][i]['count'],names=contract[pnlname][i]['names']) for i in contract[pnlname].keys() if i not in ('description')]
    panelList[j].items = itemList
        
'''from previous file'''
# for j in panelList:
#         itemList = [Items(i.split('-'),names=contract['material'][j.id][i]['names'],description=contract['material'][j.id][i]['description']) for i in contract['material'][j.id].keys()]
#         for i in range(len(itemList)):
#             itemList[i].count = len(itemList[i].names)
#         panelList[int(j.id)].items = itemList
        
# itemObjList = []

# for j, panelobj in enumerate(panelList):
#     for i, key in enumerate(contract[panelobj.name].keys()):
#         if key not in ['description']:
#             panelobj.names = contract[panelobj.name][key]
#             itemObjList.append(Items(itemno=key,names=item['names'],description=item['description'],count=item['count'],))
    # itemList = [Items(i,names=contract[panelobj.name][i]['names']) for i in filter(filterdesc, contract[panelobj.name].keys())]


# itemList = [Items(i,names=contract[panelobj.name])]

# print(itemList)

# print(itemList[0].names)
# print(itemList[1].names)
    
# # for i in itemList:
# #     print(i)
    
# for j in panelList:
#     itemList = [Items(i.split('-'),names=contract['material'][j.id][i]) for i in contract['material'][j.id].keys()]
#     for i in range(len(itemList)):
#         itemList[i].count = len(itemList[i].names)
#     panelList[int(j.id)].items = itemList


# headers = ['Item Number', 'Description', 'Total']

# for i in range(len(panelList)):
#     headers.append(panelList[i].name)

# masterList = []
    
# for i in panelList:
#     print(i)
#     for j in i.items:
#         print(j)
#         if j.itemno not in masterList:
#             masterList.append(j.itemno)
            
# print(masterList)

# # # masterList.sort()
# title = ['SHOAL CREEK RELAY EQUPIMENT<br/>MATERIAL LIST']
# subtitle = ['', '', 'QUANTITY/DEVICE NAME']
# headers = ['Item Number', 'Description', 'Total']
    
# grid = [[0 for j in range(len(panelList)+3)] for i in range(len(itemObjList)+2)]

# # print(grid)

# for i in range(len(panelList)+2):
#     title.append("")
        
# for i in range(len(panelList)):
#     subtitle.append("")
    
# for i in range(len(panelList)):
#     headers.append(panelList[i].name + '<br/>' + panelList[i].description) 

# # print(headers)

# grid[0] = title
# grid[1] = subtitle
# grid[2] = headers

# itemList = [[item.itemno for i, item in enumerate(itemObjList)] for j in item.keys()]

# # print(itemList)
# # for i, item in enumerate(itemList):
# #     print(item.itemno)
# #     for j, keys in enumerate(item.keys()):
# #         print(keys)
# #     for j, item in enumerate(panel.name)
    

# for panel in range(len(panelList)):
    
#     for item in range(len(panelList[panel].items)):
#         print(panelList[panel].items)
        
#         for item2 in range(len(masterList)):
#             pass
            
# #             if comparelist(panelList[panel].items[item].itemtype, masterList[item2]):
# #                 grid[item2+1][0] = str(masterList[item2][0]) + ''.join(masterList[item2][1:2])
# #                 grid[item2+1][panel+3] = str(len(panelList[panel].items[item].names['names'])) + '\n' + '\n'.join(panelList[panel].items[item].names['names'])

# # # for row in range(len(grid)):
# # #     count = 0
# # #     for column in range(2,len(grid[row])):
# # #         print(grid[row][column])
# # #         count += int(str(grid[row][column]).split('\n')[0])
# # #         grid[row][2] = count
                    
# # # grid[0] = headers

# # # matList = pdf(grid, 'TST.pdf')
# # # matList.exportPDF()