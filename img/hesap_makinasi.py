import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import  QColor
from PyQt5.QtWidgets import QMainWindow,QApplication,QGraphicsDropShadowEffect,QSizeGrip

# Arayüz dahil etme
from calculate import *


## ==> GLOBALS Durum değerlendirme sabitleri
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.text = ""

        

    ## WINDOW SIZE ==> Varsayılan ekran boyutları
        startSize = QSize(500, 600)
        self.resize(startSize)
        self.setMinimumSize(startSize)

    ##  LOAD DEFINITIONS ==> Arayüz dışındaki çerçevenin kaldırılması
        ########################################################################
        self.uiDefinitions()
        ## ==> END ##
    
    ## CLİCKED BUTTON ==> Arayüzdeki butonlara basılması durumları
        self.ui.pushButton.clicked.connect(self.Button)
        self.ui.pushButton_2.clicked.connect(self.Button)
        self.ui.pushButton_3.clicked.connect(self.Button)
        self.ui.pushButton_4.clicked.connect(self.Button)
        self.ui.pushButton_5.clicked.connect(self.Button)
        self.ui.pushButton_6.clicked.connect(self.Button)
        self.ui.pushButton_7.clicked.connect(self.Button)
        self.ui.pushButton_8.clicked.connect(self.Button)
        self.ui.pushButton_9.clicked.connect(self.Button)
        self.ui.pushButton_10.clicked.connect(self.Button)
        self.ui.pushButton_11.clicked.connect(self.Button)
        self.ui.pushButton_12.clicked.connect(self.Button)
        self.ui.pushButton_13.clicked.connect(self.Button)
        self.ui.pushButton_14.clicked.connect(self.Button)
        self.ui.pushButton_15.clicked.connect(self.Button)
        self.ui.pushButton_16.clicked.connect(self.Button)
        self.ui.pushButton_17.clicked.connect(self.Button)
        self.ui.pushButton_18.clicked.connect(self.Button)
        self.ui.pushButton_19.clicked.connect(self.Button)
        self.ui.pushButton_20.clicked.connect(self.Button)
    ## ==> END ##

    ## SHOW ==> Arayüz gösterme
        ########################################################################
        self.show()
    ## ==> END ##

    
    ## TRANSACTİON ==> Sonuç üretme
        ########################################################################
    
    def islem(self):
        if not self.text:
            pass
        else :
            try:
                float(self.text)

                self.ui.label_2.setText(self.text)
            except ValueError:
                if "*" in self.text:
                    a = self.text.replace(",",".").split("*")
                    self.ui.label_2.setText(str(float(a[0])*float(a[1])))
                elif "/" in self.text:
                    a = self.text.replace(",",".").split("/")
                    self.ui.label_2.setText(str(float(a[0])/float(a[1])))
                
                elif "+" in self.text:
                    a = self.text.replace(",",".").split("+")
                    self.ui.label_2.setText(str(float(a[0])+float(a[1])))
                elif "-" in self.text:
                    a = self.text.replace(",",".").split("-")
                    self.ui.label_2.setText(str(float(a[0])-float(a[1])))
                

         ## ==> END ##

    
    ## MENUS ==> Butonlara basılma durumları
        ########################################################################
    def Button(self):
         # GET BT CLICKED ==> Hangi butona basıldığını bulma
        btnWidget = self.sender()

        if btnWidget.text() =="AC":
            self.text = ""
            self.ui.label_2.setText("0")
        elif btnWidget.text() =="=":
            self.islem()
        elif btnWidget.text() =="+/-":
            a = float(self.text.replace(",","."))
            a *= -1
            self.text = str(a)
                
        else:
            self.text += btnWidget.text()
        
        self.ui.label.setText(self.text)

     ## ==> END ##

    ## EVENT ==> Klavye üzerindeki butonlar ile işlem yapma
        ########################################################################
    def keyPressEvent(self, event):
        if str(event.key()) =="16777220":
            self.islem()
        elif str(event.key()) =="16777219":
            self.text = self.text[:-1]
            self.ui.label.setText(self.text)
        else:
            self.text += str(event.text())
            self.ui.label.setText(self.text)
    ## ==> END ##



    ##MAXIMIZE/RESTORE ==> Tam ekran yapma
        ########################################################################
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()


    ## UI DEFINITIONS==> Arayüz ve üzerindeki butonlarla ilgili işlemler
        ########################################################################
    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS ==> Üst kısıma 2 kere basıldığında tam ekran yapma
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: self.maximize_restore())

        ## REMOVE ==> STANDARD TITLE BAR ==> standart ekran boyutu
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()


        ## SHOW ==> DROP SHADOW ==> gölge düşürme
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        ## ==> RESIZE WINDOW ==>Ana Ekran Boyutlandırma
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        ### ==> MINIMIZE ==> Minumum butonuna basıldığında
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## ==> MAXIMIZE/RESTORE ==> Maximum butonuna basıldığında
        self.ui.btn_maximize_restore.clicked.connect(lambda: self.maximize_restore())

        ## SHOW ==> CLOSE APPLICATION ==> Kapatma butonuna basıldığında
        self.ui.btn_close.clicked.connect(lambda: self.close())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())