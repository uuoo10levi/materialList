#akljdsfaskdf
#and
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import styles
from reportlab.pdfgen.canvas import Canvas

import json
import subprocess

            

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
    def __init__(self, itemno='', description='', pnltotal=1, names=[]):
        self.pnltotal = pnltotal
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

class NumberedPageCanvas(Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    http://www.blog.pythonlibrary.org/2013/08/12/reportlab-how-to-add-page-numbers/
    """

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            self.draw_rev_number()
            super().showPage()

        super().save()

    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 8)
        self.drawRightString(10.75 * inch, 0.25 * inch, page)
        
    def draw_rev_number(self):
        self.setFont("Helvetica", 8)
        self.drawString(0.25 * inch, 0.25 * inch, 'Rev. 0')
        
class pdf:
    def __init__(self, data, name = '_.pdf'):
        
        self.styleSheet = getSampleStyleSheet()
        self.pagesize = (11 * inch, 8.5 * inch)  # 20 inch width and 10 inch height.doc = SimpleDocTemplate('sample.pdf', pagesize=pagesize)
        self.styleCustomCenterJustified = ParagraphStyle(name='BodyText', parent=self.styleSheet['BodyText'], spaceBefore=6, alignment=1, fontSize=8)
        self.styleCustomLeftJustified = ParagraphStyle(name='BodyText', parent=self.styleSheet['BodyText'], spaceBefore=6, alignment=0, fontSize=8)
        self.doc = SimpleDocTemplate(name, pagesize=self.pagesize)
        self.doc.__setattr__('topMargin', 0.25*inch)
        self.doc.__setattr__('leftMargin', 0.25*inch)
        self.doc.__setattr__('rightMargin', 0.25*inch)
        self.doc.__setattr__('bottomMargin', 0.25*inch)
        self.elements = []
        

        for i in range(len(data)):
            for j in range(len(data[i])):
                if j != 1:
                    data[i][j] = Paragraph(str(data[i][j]), self.styleCustomCenterJustified)
                
        for i in range(len(data)):
            if i > 2:
                data[i][1] = Paragraph(str(data[i][1]), self.styleCustomLeftJustified)
            
        # data[2][1] = Paragraph(str(data[2][1]), self.styleCenterJustified)
        # data[2][1] = Paragraph(str(data[2][1]), self.styleCenterJustified)
                
        
        self.pdftable = Table(data, colWidths= (50,200,50,100,100,100), repeatRows=3, style=[
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('SPAN', (0,0), (-1, 0)),
            ('SPAN', (0,1), (1, 1)),
            ('SPAN', (2,1), (-1, 1)),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'TOP')]
                              )

        self.elements.append(self.pdftable)

    def exportPDF(self):
        self.doc.build(self.elements, canvasmaker=NumberedPageCanvas)
        

def pdfer(contractfile=''):
    with open(contractfile, 'r') as file:
        contract = json.load(file)

    panelList = [PanelObjects(i,name=name) for i, name in enumerate(contract)]


    for i,obj in enumerate(panelList):
        obj.description = contract[obj.name]['description']


    for j, pnlobj in enumerate(panelList):
        pnlname = pnlobj.name
        itemList = [Items(itemno=i,description=contract[pnlname][i]['description'],pnltotal=contract[pnlname][i]['count'],names=contract[pnlname][i]['names']) for i in contract[pnlname].keys() if i not in ('description')]
        panelList[j].items = itemList


    headers = ['Item Number', 'Description', 'Total']

    for i in range(len(panelList)):
        headers.append(panelList[i].name)

    title = ['SHOAL CREEK RELAY EQUPIMENT\nMATERIAL LIST']
    subtitle = ['', '', 'QUANTITY/DEVICE NAME']
    headers = ['Item Number', 'Description', 'Total']
        
    grid = [[0 for j in range(len(panelList)+3)] for i in range(len(panelList)+2)]

    for i in range(len(panelList)+2):
        title.append("")
            
    for i in range(len(panelList)):
        subtitle.append("")
        
    for i in range(len(panelList)):
        headers.append(panelList[i].name + '<br/>' + panelList[i].description) 

    # print(headers)

    grid[0] = title
    grid[1] = subtitle
    grid[2] = headers

    allheaders = [title, subtitle, headers]
    
    for i, panel in enumerate(panelList):
        for j, items in enumerate(panel.items):
            '''Fill Item Number'''
            grid[j+len(allheaders)][0] = items.itemno
            '''Fill description'''
            grid[j+len(allheaders)][1] = items.description
            '''Fill Item Count and Names in Each Panel Column'''
            grid[j+len(allheaders)][i+3] = items.pnltotal + '<br/>' + '<br/>'.join(items.names)
                    
    '''Fill 'total count' column'''
    for row in range(len(allheaders),len(grid)):
        count = 0
        for column in range(2,len(grid[row])):        
            count += int(str(grid[row][column]).split('<br/>')[0])
            grid[row][2] = count

    matList = pdf(grid, 'TST.pdf')
    matList.exportPDF()
    subprocess.Popen('"C:/Program Files/Tracker Software/PDF Editor/PDFXEdit.exe" "C:/Users/lwooten/Desktop/Relaying Material Python/materialList/TST.pdf"', shell=True) 

if __name__ == '__pdfer__':
    pdfer()
    
