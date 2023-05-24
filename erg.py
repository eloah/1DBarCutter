import sys
import os
import time
import subprocess
from PySide.QtGui import *
from PySide.QtCore import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Flowable, Image, Paragraph, SimpleDocTemplate, Table, TableStyle, Spacer, KeepTogether, CondPageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab import platypus
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import black
from pulp import *


class warningWindow(QWidget):
        
    def __init__(self, parent = None):
        super(warningWindow, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Warning')
        self.setWindowIcon(QIcon(QPixmap('Icons/log.png')))
        self.setMinimumSize(450, 150)
        self.setMaximumSize(450, 150)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.label = QLabel("", self)
        self.label.setGeometry(0, 20, 430, 50)
        self.label.setStyleSheet("font-size:20px; font-family:Calibri; color:black; font-weight:bold;")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.okBtn = QPushButton("", self)
        self.okBtn.setGeometry(200, 80, 50, 50)
        self.okBtn.setCursor(Qt.PointingHandCursor)
        self.okBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}"
        	                     "QPushButton::hover{image: url('Icons/okhov.png'); background:transparent;}")
                     
        self.okBtn.clicked.connect(self.close)

    def openWarningWindow(self, status):
        if status == 1:
            self.label.setText("Data can be only numbers!")
        elif status == 2:
            self.label.setText("   Add all the data!")
        elif status == 3:
            self.label.setText("     Dimension is bigger than lenght!\n     Data can be only numbers!")
        self.show()


'''class statusWindow(QDialog):
       
    def __init__(self, parent = None):
        super(statusWindow, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Προυπολογισμός')
        self.setWindowIcon(QIcon(QPixmap('Icons/log.png')))
        self.setMinimumSize(450, 150)
        self.setMaximumSize(450, 150)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.label = QLabel("Προυπολογισμός υλικού", self)
        self.label.setGeometry(0, 20, 450, 50)
        self.label.setStyleSheet("font-size:20px; font-family:Calibri; color:black; font-weight:bold;")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.timeLbl = QLabel("20", self)
        self.timeLbl.setGeometry(200, 70, 50, 50)
        self.timeLbl.setStyleSheet("background-color:black; font-size:20px; font-family:Calibri; color:white; font-weight:bold; border:2px solid black; border-radius:10px;")
        self.timeLbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.cancelBtn = QPushButton("", self)
        self.cancelBtn.setGeometry(250, 80, 50, 50)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}"
        	                     "QPushButton::hover{image: url('Icons/okhov.png'); background:transparent;}")
                     
        self.cancelBtn.clicked.connect(self.close)

    def openStatusWindow(self):
        self.exec_()
        self.signal.emit()

    def showTime(self):
        self.timer.start()

    def stopTime(self):
    	self.timer.stop()

    def closeStatusWindow(self, close):
    	if close == True:
            self.close()'''
           
class Ergo(QMainWindow):
    
    def __init__(self, parent = None):
        super(Ergo, self).__init__(parent)
        self.initUI()

    def initUI(self):
    	
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle('Cutting Optimizer')
        #self.setWindowIcon(QIcon(QPixmap('Icons/log.png')))
        self.setMinimumSize(1200, 710)
        self.setMaximumSize(1200, 710)
        self.setStyleSheet("QMainWindow{background-color: none;}"
        	               "QTableWidget{gridline-color:black; border:2px solid black; border-radius:12px; font-size:20px; font-family:Calibri; font-weight:bold}"
                           "QHeaderView::section{font-size:18px; border-right:2px solid black; font-weight:bold; color:black; font-weight:bold;}"
                           "QHeaderView::section:horizontal{padding:10px; font-size:14px; font-weight:bold; border-bottom:2px solid black;}"
                           "QHeaderView::section:vertical{font-size:12px; padding:6px; border-bottom:2px solid black;}")
        
        self.name = QLabel(self.centralWidget)
        self.name.setGeometry(110, 30, 100, 30)
        self.name.setText("Name")
        self.name.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black;")

        self.nameLbl = QLineEdit(self.centralWidget)
        self.nameLbl.setGeometry(40, 60, 200, 30)
        self.nameLbl.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black; border:2px solid black; border-radius:8px;")

        self.dim = QLabel(self.centralWidget)
        self.dim.setGeometry(40, 90, 100, 30)
        self.dim.setText("Dimension")
        self.dim.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black;")

        self.x = QLabel(self.centralWidget)
        self.x.setGeometry(135, 118, 20, 30)
        self.x.setText("x")
        self.x.setStyleSheet("font-size:28px; font-family:Calibri; font-weight:bold; color:black;")

        self.dimLbl = QLineEdit(self.centralWidget)
        self.dimLbl.setGeometry(40, 120, 80, 30)
        self.dimLbl.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black; border:2px solid black; border-radius:8px;")
        self.dimLbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.quantity = QLabel(self.centralWidget)
        self.quantity.setGeometry(190, 90, 100, 30)
        self.quantity.setText("Qty")
        self.quantity.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black;")

        self.quanLbl = QLineEdit(self.centralWidget)
        self.quanLbl.setGeometry(160, 120, 80, 30)
        self.quanLbl.setText("1")
        self.quanLbl.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black; border:2px solid black; border-radius:8px;")
        self.quanLbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.material = QLabel(self.centralWidget)
        self.material.setGeometry(40, 150, 100, 30)
        self.material.setText("Lenght")
        self.material.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black;")


        self.materialLbl = QLineEdit(self.centralWidget)
        self.materialLbl.setGeometry(40, 180, 65, 30)
        self.materialLbl.setText("6000")
        self.materialLbl.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black; border:2px solid black; border-radius:8px;")
        self.materialLbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.cut = QLabel(self.centralWidget)
        self.cut.setGeometry(175, 150, 100, 30)
        self.cut.setText("Cut")
        self.cut.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black;")


        self.cutLbl = QLineEdit(self.centralWidget)
        self.cutLbl.setGeometry(175, 180, 65, 30)
        self.cutLbl.setText("5")
        self.cutLbl.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black; border:2px solid black; border-radius:8px;")
        self.cutLbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.nLbl = QLabel(self.centralWidget)
        self.nLbl.setGeometry(290, 30, 400, 30)
        self.nLbl.setText("")
        self.nLbl.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black;")

        self.bLbl = QLabel(self.centralWidget)
        self.bLbl.setGeometry(1065, 30, 200, 30)
        self.bLbl.setText("Bars: ")
        self.bLbl.setStyleSheet("font-size:20px; font-family:Calibri; font-weight:bold; color:black;")

        self.table = QTableWidget(self.centralWidget)
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setGeometry(42, 295, 198, 370)
        self.colLabels = ['Dim/ns','Cancel']
        self.table.setHorizontalHeaderLabels(self.colLabels)
        self.horizHeader = self.table.horizontalHeader()
        self.horizHeader.setResizeMode(0, QHeaderView.Stretch)
        self.horizHeader.setResizeMode(1, QHeaderView.Stretch)

        self.addBtn = QPushButton(self.centralWidget)
        self.addBtn.setGeometry(40, 230, 40, 40)
        self.addBtn.setCursor(Qt.PointingHandCursor)
        self.addBtn.setStyleSheet("QPushButton{image: url('Icons/add.png'); background:transparent;}"
                                  "QPushButton::hover{image: url('Icons/addhov.png'); background:transparent; border-bottom:2px solid white;}")  

        self.startBtn = QPushButton(self.centralWidget)
        self.startBtn.setGeometry(95, 230, 40, 40)
        self.startBtn.setCursor(Qt.PointingHandCursor)
        self.startBtn.setStyleSheet("QPushButton{image: url('Icons/play.png'); background:transparent; border-bottom:2px solid white;}"
        	                        "QPushButton::hover{image: url('Icons/playhov.png'); background:transparent;}")      
        self.startBtn.setEnabled(False)

        self.resetBtn = QPushButton(self.centralWidget)
        self.resetBtn.setGeometry(148, 230, 40, 40)
        self.resetBtn.setCursor(Qt.PointingHandCursor)
        self.resetBtn.setStyleSheet("QPushButton{image: url('Icons/reset.png'); background:transparent;}"
                                    "QPushButton::hover{image: url('Icons/resethov.png'); background:transparent; border-bottom:2px solid white;}")

        self.saveBtn = QPushButton(self.centralWidget)
        self.saveBtn.setGeometry(200, 230, 40, 40)
        self.saveBtn.setCursor(Qt.PointingHandCursor)
        self.saveBtn.setStyleSheet("QPushButton{image: url('Icons/save.png'); background:transparent;}"
        	                       "QPushButton::hover{image: url('Icons/savehov.png'); background:transparent; border-bottom:2px solid white;}")
        self.saveBtn.setEnabled(False)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 870, 600)
        self.brush = QBrush()
        self.pen = QPen()
        self.pen.setWidth(2)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(280, 60, 880, 604)
        self.view.setStyleSheet("border:2px solid black; border-radius:10px;")
        
        self.warningWindow = warningWindow()
        #self.statusWindow = statusWindow()
      

        self.stockList = []
        self.cutList = []
     
        self.addBtn.clicked.connect(self.addData)
        self.startBtn.clicked.connect(self.cutSorting)
        self.resetBtn.clicked.connect(self.resetData)
        self.saveBtn.clicked.connect(self.saveData)

    def addData(self):
        name = self.nameLbl.text()
        dim = self.dimLbl.text()
        qu = self.quanLbl.text()
        self.size = self.materialLbl.text()
        self.kerf = self.cutLbl.text()

        if dim and qu and self.kerf and self.size: 
            try:
                dim = int(dim)
                qu = int(qu)
                self.size = int(self.size)
                self.kerf = int(self.kerf)

            except ValueError:
                status = 1    
                self.warningWindow.openWarningWindow(status)

        else:
            status = 2
            self.warningWindow.openWarningWindow(status)
        
        row = self.table.rowCount()
        if dim <= self.size:

            for i in range(0,qu):
                self.stockList.append(dim)
                self.table.insertRow(row)
                self.table.setItem(row, 0 , QTableWidgetItem(str(dim)))
                self.stockList.sort(reverse=True)
                print(self.stockList)
                rBtn = QPushButton(" x ")
                rBtn.clicked.connect(self.removeRow)
                rBtn.setStyleSheet("QPushButton{background:black; color:white; font-family:Calibri; font-size:26px;font-weight:bold;}"
                	               "QPushButton::hover{background:grey; color:white; font-family:Calibri; font-size:26px;font-weight:bold;}")
                rBtn.setCursor(Qt.PointingHandCursor)
                self.table.setCellWidget(row, 1, rBtn)
        else:
            status = 3
            self.warningWindow.openWarningWindow(status)
        self.startBtn.setEnabled(True)
        self.dimLbl.clear()
        self.quanLbl.setText("1")

    def cutSorting(self):
        print("start")          
        size = self.size
        kerf = self.kerf
        self.nLbl.setText(self.nameLbl.text())
        stock = []
        self.cutList = []
        
        for i in range(len(self.stockList)):
            it = self.stockList[i] + kerf*2
            stock.append((str(i),it))

        print(stock)
        count = len(stock)
        maxBar = len(stock)+2
        
        y = pulp.LpVariable.dicts('BinUsed', range(maxBar),
                            lowBound = 0,
                            upBound = 1,
                            cat = LpInteger)
        possible = [(itemTuple[0], binNum) for itemTuple in stock
                                            for binNum in range(maxBar)]
        x = pulp.LpVariable.dicts('itemInBin', possible,
                            lowBound = 0,
                            upBound = 1,
                            cat = LpInteger)

        model = LpProblem("BPP", LpMinimize)
        model += lpSum([y[i] for i in range(maxBar)]), "Objective: Minimize Bins Used"
        
        for j in stock:
            model += lpSum([x[(j[0], i)] for i in range(maxBar)]) == 1, ("An item can be in only 1 bin -- " + str(j[0]))
        
        for i in range(maxBar):
            model += lpSum([stock[j][1] * x[(stock[j][0], i)] for j in range(count)]) <= size*y[i], ("Smaller than the bin -- " + str(i))
        
        print("solving")
        model.writeLP("LP/BinPack.lp")
        curTime = time.time()
        pt = os.path.abspath("LP/cbc/cbc.exe")
        model.solve(COIN_CMD(path=pt))
        #model.solve(COIN_CMD(path="LP/cbc/cbc.exe"))

        print("%s seconds." % (time.time() - curTime))
        used = str(int(sum(([y[i].value() for i in range(maxBar)]))))
        print("Bars used: " + str(used))
        
        bars = {}
        for itemBinPair in x.keys():
            if(x[itemBinPair].value() == 1):
                itemNum = itemBinPair[0]
                binNum = itemBinPair[1]
                if binNum in bars:
                    bars[binNum].append(itemNum)
                else:
                    bars[binNum] = [itemNum]

        temp = {k:v for k,v in stock}
        
        for values in bars.values():
            inList = []
            for value in values:
                val = temp[value]
                inList.append(val-kerf*2)
            self.cutList.append(inList)
        #self.cutList.sort(reverse=True)   
        #self.cutList = [[temp.get(y) for y in x] for x in bars.values()]
        print(self.cutList)  

        if used != 0:    
            self.bLbl.setText("Bars:  " + used)
        #self.cutList.sort(reverse=True)
        if self.cutList:
            self.draw()
        stock = [] 

    def removeRow(self):
        print(self.stockList)
        currentRow = self.table.currentRow()
        text = self.table.item(currentRow,0)
        text = int(text.text())
        self.stockList.remove(text)
        print(self.stockList)
        self.table.removeRow(currentRow)

    def draw(self):
        self.scene.clear()
        top = 10 
        self.scene.setSceneRect(0, 0, 870, 20000)

        l = len(self.cutList)
        for i in range(0,l): 
            l2 = len(self.cutList[i])
            left = 10
            p = 820/self.size
            for j in range(0,l2):
                length = self.cutList[i][j]*p-4
                rect = self.scene.addRect(left, top, length, 26, self.pen, self.brush)
                text = self.scene.addText(str(self.cutList[i][j]), QFont('Calibri', 12, QFont.Bold))
                text.setPos(left,top)
                left += length + 4
            
            text = self.scene.addText(str(i+1), QFont('Calibri', 12, QFont.Bold))
            text.setPos(830,top) 
            line = self.scene.addLine(QLine(0,top+33, 870, top+33))
            top += 40
        self.saveBtn.setEnabled(True)

    def resetData(self):
        self.stockList = []
        self.cutList = []
        self.nameLbl.clear()
        self.dimLbl.clear()
        self.quanLbl.setText("1")
        self.materialLbl.setText("6000")
        self.cutLbl.setText("5")
        self.table.setRowCount(0)
        self.bLbl.setText("Bars: ")
        self.nLbl.setText("")
        self.scene.clear()
        self.startBtn.setEnabled(False)
        self.saveBtn.setEnabled(False)
        self.scene.setSceneRect(0, 0, 870, 600)

    def saveData(self):
        c = canvas.Canvas('PDF/'+self.nameLbl.text()+'.pdf', pagesize=A4)
        width, height = A4
        stylesheet = getSampleStyleSheet()
        pdfmetrics.registerFont(TTFont('Calibri', 'CALIBRIB.ttf'))
        c.setFont('Calibri', 14)
        c.setStrokeColor(black)
        c.drawString(20, 810, self.nLbl.text())
        c.drawString(510, 810, str(self.bLbl.text()))
        c.setFont('Calibri', 12)
        
        top = 770
        l = len(self.cutList)
        s = 540/self.size
        n = int(l/30)
        q = 0
        p = 0
        for k in range(0,n):
            c.setFont('Calibri', 12)
            top = 770
            for i in range(0,30): 
                l2 = len(self.cutList[i])
                left = 15
                for j in range(0,l2):
                    length = self.cutList[i][j]*s-4
                    c.rect(left, top, length, 16, stroke=1, fill=0)
                    c.drawString(left+3, top+4, str(self.cutList[i][j]))
                    c.line(0, top+21, 594, top+21)
                    left += length + 4
                q += 1
                c.drawString(565, top+4, str(q))
                top -= 25
            c.line(0, top+21, 594, top+21) 
            p += 1
            c.drawString(295, 20, str(p))      
            c.showPage()
        
        c.setFont('Calibri', 12)
        top = 770
        ca = l - n*30
        if ca != 0 and ca > 0:
            for i in range(0,ca): 
                l2 = len(self.cutList[i])
                left = 15
                for j in range(0,l2):
                    length = self.cutList[i][j]*s-4
                    c.rect(left, top, length, 16, stroke=1, fill=0)
                    c.drawString(left+3, top+4, str(self.cutList[i][j]))
                    c.line(0, top+21, 594, top+21)
                    left += length + 4
                q += 1
                c.drawString(565, top+4, str(q))
                top -= 25
            c.line(0, top+21, 594, top+21) 
            p += 1
            c.drawString(295, 20, str(p))      
            c.showPage()
        
        c.save()
        pt = os.path.abspath("PDF/"+self.nameLbl.text()+".pdf")
        #subprocess.Popen([pt], shell=True)
        self.cutList = []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ergo = Ergo()
    ergo.show()
    sys.exit(app.exec_())