# -*- coding: utf-8 -*-
"""
Created on 2021-05-14

@author: rg

doubleMan.py

Das Programm 'doubleRep.py' erzeugt unter anderem eine CSV-Datei,
die dieses Programm einlädt und zur Berabeitung präsentiert.
Jede Doublette besteht aus 2 oder mehreren vermeintlich identischen Filmen,
die in diesem Programm - analysiert, umbenannt, angeschaut oder gelöscht werden können.

"""
from PyQt5.QtWidgets import (QMainWindow, 
                             QMenu,
                             QAction,
                             QLabel, 
                             QLineEdit, 
                             QPushButton,
                             QWidget,
                             QApplication, 
                             QMessageBox,
                             QFileDialog,
                             QTableWidgetItem,
                             QAbstractItemView,
                             QHeaderView,
                             QInputDialog )

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, Qt, QDir, QModelIndex
from PyQt5.QtGui import QIcon, QColor

import sys
import os
import time
import subprocess
from bitsNbytes import format_size

# die fenster wurden mit dem qtdesigner entworfen und per pyuic5 konvertiert
import doubleManUI

# das soll die Importe aus dem Ordner Liste mit einschließen...
sys.path.append(".\\liste")
import liste.liste as liste
import filmAnalyse
import doubleRep

# Handle high resolution displays (thx 2 https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution):
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class Konstanten():
    vpath = "Y:\\video\\"
    delBasket = "__del"

class doublette():
    """
    beinhaltet eine Datei mit allen ihren Doubletten
    """

    def __init__(self, dID, lfd, FilmName, FilmExt, FullPath):
        self.dID = dID
        self.lfd = lfd
        self.FilmName = FilmName    # normierter Filmname
        self.FilmExt = FilmExt
        self.FullPath = FullPath
        self.exist = True

    def __str__(self):
        return "dID={0}, lfd={1}, DateiName={2}, Ext={3}, \nfullPath={4}".format(self.dID, self.lfd, self.FilmName, self.FilmExt, self.FullPath)


# --------------------------------------------------------------------------------
# Main App class
# --------------------------------------------------------------------------------
class MainApp(QMainWindow, doubleManUI.Ui_MainWindow):
    # suchAnfrage = pyqtSignal(str, str, str)

    def __init__(self):
        super(self.__class__, self).__init__()

        QMainWindow.__init__(self)
        doubleManUI.Ui_MainWindow.__init__(self)

        self.setupUi(self)  # This is defined in the UI.py file automatically
                            # It sets up layout and widgets that are defined
        # Instanz-Variablen                
        self.delBasket = "__del"
        self.dbls = liste.liste()
        
        # Icon versorgen
        scriptDir = str(os.path.dirname(os.path.realpath(__file__)))
        # self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'doubleMan.ico'))        

        self.buttonSchalter(False)
        self.btn_exit.setEnabled(True)        
        
        self.tbl_fname.currentItemChanged.connect(self.zeigeDetails)

        # self.le_rename.visible(False)

        # tbl_fname
        self.tbl_fname.setColumnCount(1)
        self.tbl_fname.setHorizontalHeaderLabels(['FilmName'])
        self.tbl_fname.setAlternatingRowColors(True)
        header = self.tbl_fname.horizontalHeader()
        # header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.Stretch)     # ResizeToContents
        # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tbl_fname.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbl_fname.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_fname.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_fname.setRowCount(0)
        self.tbl_fname.doubleClicked.connect(self.analyse)
        self.tbl_fname.setEnabled(False)

        # tbl_details
        self.tbl_details.setHorizontalHeaderLabels(('lfd.Nr', 'FilmDatei', 'Typ', 'Größe', 'Datum', 'VideoAuflösung', 'Audio-Streams', 'Subtitles'))
        self.tbl_details.setAlternatingRowColors(True)
        header = self.tbl_details.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # self.tbl_details.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbl_details.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_details.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_details.setRowCount(0)
        self.tbl_details.setColumnCount(8)
        self.tbl_details.setEnabled(False)
        
        # connects
        self.btn_analyse.clicked.connect(self.analyse)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_exit.clicked.connect(self.close)
        self.btn_rename.clicked.connect(self.rename)
        self.btn_show.clicked.connect(self.zeigen)
        self.btn_laden.clicked.connect(self.neueDateiLaden)
        self.btn_erzeugen.clicked.connect(self.neueDatei)
        self.tbl_fname.itemSelectionChanged.connect(self.zeigeDetails)

        # context Menu in der details-tabelle--------------------------------------
        # Actions definieren
        zeigAct = QAction('Film zeigen', self.tbl_details, triggered=self.zeigen)
        renAct = QAction('Film umbenennen', self.tbl_details, triggered=self.rename)
        delAct =  QAction('Film löschen', self.tbl_details, triggered=self.delete)
        # Policy zufügen
        self.tbl_details.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Actions zum Kontextmenü zufügen
        self.tbl_details.addAction(zeigAct)
        self.tbl_details.addAction(renAct)
        self.tbl_details.addAction(delAct)
                
        # popDet.addSeparator()
        # quitAct = popDet.addAction(QAction('Quit', self, triggered=self.close))        

        self.statusMeldung("Ready")
        self.buttonSchalter(True)
        self.show()
        # QApplication.processEvents()
        self.doublesLaden()

    # emuliert den default-key
    def keyPressEvent(self, event):
        w = self.focusWidget()
        modifiers = QApplication.keyboardModifiers()

        if event.key() == Qt.Key_F6:
            if w == self.tbl_details:
                self.rename()
        elif event.key() == Qt.Key_Delete:
            if w == self.tbl_details:
                self.delete()
        elif event.key() == Qt.Key_Return:            
            if w == self.tbl_fname:
                self.analyse()                
            elif w == self.tbl_details:
                self.zeigen()     # self.lst_erg.currentRow, 1
        elif event.key() == Qt.Key_F2:
             self.analyse()
        # elif event.key() == Qt.Key_F4:  # Split Feld 1
        #     self.suchFeldSplit()
        # elif event.key() == Qt.Key_F5:  # Paste, wie ctrl+m
        #     self.suchFeldLeer2()
        # elif event.key() == Qt.Key_X:
        #     # modifiers = QApplication.keyboardModifiers()
        #     if modifiers == Qt.ControlModifier:
        #         self.suchFeldLeer()
        # elif event.key() == Qt.Key_M:       # ctrl+m, um die Zwischenablage einzufügen
        #     if modifiers == Qt.ControlModifier:
        #         self.suchFeldLeer2()
        # elif event.key() == Qt.Key_S:       # ctrl+s, den Text in dem 1. Suchfeld zu splitten
        #     if modifiers == Qt.ControlModifier:
        #         self.suchFeldSplit()        

        return
    
    def buttonSchalter(self, OnOff):
        self.btn_analyse.setEnabled(OnOff)
        self.btn_show.setEnabled(OnOff)
        self.btn_delete.setEnabled(OnOff)
        self.btn_rename.setEnabled(OnOff)
        self.tbl_fname.setEnabled(OnOff)
        self.tbl_details.setEnabled(OnOff)


    def analyse(self):
        for zle in range(self.tbl_details.rowCount()):
            film = self.tbl_details.item(zle, 1).text()
            # print(film)
            if os.path.isfile(film):
                self.statusMeldung("Lese Video-Infos...")
                QApplication.processEvents()
                x = filmAnalyse.getFilmDetails(film)

                if x is None or x == "":
                    self.statusMeldung("Video-Infos konnten nicht gelesen werden!")
                else:
                    vid, aud, sub = x
                    self.tbl_details.setItem(zle, 5, QTableWidgetItem(vid))
                    self.tbl_details.setItem(zle, 6, QTableWidgetItem(aud))
                    self.tbl_details.setItem(zle, 7, QTableWidgetItem(sub))
                    self.statusMeldung("Video-Infos gelesen!")
                self.buttonSchalter(True)
        return

    def delete(self):
        film = self.getCurrentFilm()
        delVideo = film
        filmBaseName = os.path.basename(film)
        delTarget = Konstanten.vpath + os.sep + self.delBasket + os.sep + filmBaseName
        if delTarget == film:
            self.statusMeldung("Kann einen Film im Papierkorb nicht nochmals löschen")
            return
        try:
            os.rename(delVideo, delTarget)
        except OSError as err:
            self.statusMeldung("Fehler! ({})".format(err.strerror))
        finally:                
            self.statusMeldung(f"Der Film [{filmBaseName}] wurde aus dem Archiv nach [{delTarget}] verschoben!")
                # Anpassung der Tabellen
            obj = self.dbls.find("FullPath", film)
            if obj is None:
                self.statusMeldung("AnzeigeFehler! Kann den Doubletten-Satz nicht aktualisieren!")
            else:
                obj.FullPath = delTarget
                self.markiereFilm()
                self.zeigeDetails()           
        return

    def markiereFilm(self):
        aktrow = self.tbl_fname.currentRow()
        self.tbl_fname.item(aktrow, 0).setForeground(QColor(250, 0, 250))

    def rename(self):
        film = self.getCurrentFilm()
        if film is None:
            self.statusMeldung("Sorry, kann den aktuellen Film nicht bestimmen!")
            return 
        
        film_head, film_tail = os.path.split(film)
        alterName = film_head
        neuerName, ok = QInputDialog.getText(self, 'Film umbenennen', 'Neuer Name:',
                                             QLineEdit.Normal, film_tail)
        if ok and not (neuerName == ''):
            neuerFullName = film_head + os.sep + neuerName
            alterFullName = film
            try:
                os.rename(alterFullName, neuerFullName)
            except OSError as err:
                self.statusMeldung("Fehler! ({})".format(err.strerror))
            finally:
                # Anzeige aktualisieren
                self.statusbar.showMessage("Video umbenannt in: {}".format(neuerName))                
                # Anpassung der Tabellen
                obj = self.dbls.find("FullPath", film)
                if obj is None:
                    self.statusMeldung("AnzeigeFehler! Kann den Doubketten-Satz nicht aktualisieren!")
                else:
                    obj.FullPath = neuerFullName
                    self.zeigeDetails()                
        return


    def zeigen(self):        
        film = self.getCurrentFilm()
        if film is None:
            self.statusMeldung("Sorry, kann den aktuellen Film nicht bestimmen!")
            return 
        else:
            # film = self.tbl_details.item(self.tbl_details.currentRow(), 1)
            self.videoStart(film)

    
    def getCurrentFilm(self):
        # sucht den in der Tabelle tbl_detail aktuellen Film heraus
        # gibt bei Fehler None zurück

        aktrow = self.tbl_details.currentRow()
        if aktrow is None or aktrow < 0:
            return None
        else:
            if self.tbl_details.item(aktrow, 1) is None:
                return None
            else:
                # print(type(self.tbl_film.item(row, 0)))
                return(self.tbl_details.item(aktrow, 1).text())

    
    def getCurrentDbl(self):
        # sucht den in der Tabelle tbl_fname die aktuelle Doublette heraus        
        # gibt bei Fehler None zurück

        aktrow = self.tbl_fname.currentRow()
        if aktrow is None or aktrow < 0:
            return None
        else:
            if self.tbl_fname.item(aktrow, 0) is None:
                return None
            else:
                # print(type(self.tbl_film.item(row, 0)))
                # return(self.tbl_fname.item(aktrow, 0).text())
                return aktrow + 1

    def getCurrentDblDetail(self):
        aktrow = self.tbl_details.currentRow()
        if aktrow is None or aktrow < 0:
            return None
        else:
            film = self.tbl_fname.item(aktrow, 1).text()
            if film is None:
                return None
            else:
                # doubletten-Satz suchen
                obj = self.dbls.find("FullPath", film)
                if obj is None:
                    return None
                else:
                    return obj

    def neueDateiLaden(self):
        self.tbl_details.clear()
        self.tbl_fname.clear()
        self.dbls.zap()
        self.doublesLaden(csvDatei=None)
    

    def openFileNameDialog(self)->str:
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "eine CSV-Datei aussuchen", os.getcwd(),"CSV-Dateien (*.csv);;All Files (*)", options=options)
        # fileName, _ = QFileDialog.getOpenFileName(self, "einen Film aussuchen", "E:\\Filme\\", "All Files (*);;Filme (*.mkv *.mpg *.mp4 *.ts *.avi)", options=options)
        if fileName:
            return fileName
        else:
            return None


    def doublesLaden(self, csvDatei=None):
        # gibt eine Dateiauswahl für eine Doubletten-Liste,
        # lädt diese in den Speicher und aktualisiert die TableWidgets
        if csvDatei is None:                        
            csvDatei = self.openFileNameDialog()
        print(csvDatei)
        if csvDatei is None:
            # self.statusMeldung("Oops! Kann keine CSV-Datei laden!")
            return            
            # self.close()
        else:
            self.datenEinlesen(csvDatei)
        
        # jetzt die Tabellen füllen
        self.tbl_details.clearContents()
        self.tbl_fname.clearContents()
        lastId = "-1"
        cnt = 0

        obj = self.dbls.findLast()
        self.tbl_fname.setRowCount(int(obj.dID))        
        obj = self.dbls.findFirst()
        zle = 0
        for obj in self.dbls.liste:
            if obj is None:
                break
            if obj.dID == lastId:
                 continue
            else:
                lastId = obj.dID
                zle = int(lastId)-1
                # self.tbl_fname.setItem(zle, 0, QTableWidgetItem(zle))
                self.tbl_fname.setItem(zle, 0, QTableWidgetItem(obj.FilmName))
                # print(f"lade {zle}: {lastId}, {(obj.FilmName)}")

        # if row > 0:
        #     self.tbl_fname.setRowCount(row)
            # print(f"Anzahl {row}")
        self.tbl_fname.setSortingEnabled(False)
        self.tbl_fname.setCurrentCell(0,0)
        self.tbl_fname.setEnabled(True)
        self.tbl_fname.setCurrentCell(0, 0)
        self.zeigeDetails()                        


    def datenEinlesen(self, datei):
        # liest die übergebene CSV-Datei ein
        cnt = 0        
        with open(datei, "r", encoding='utf8') as inFile:
            for line in inFile:
                cnt += 1
                line = line.strip()
                # # erste Zeile überspringen, die enthält Überschriften                
                if cnt == 1:                    
                    continue
                felder = line.split(";")
                # Felder: Nr;lfd Nr;Name;Typ;FullPath
                #          0;    1 ;  2 ; 3 ;   4
                dbl = doublette(felder[0], felder[1], felder[2], felder[3], felder[4])
                self.dbls.append(dbl)


    def zeigeDetails(self):
        self.tbl_details.clearContents()
        nr = self.getCurrentDbl()
        if nr is None:
            return
        else:
            # print(nr)
            lst = self.dbls.findAll("dID", str(nr))
            # print(lst)
            if lst is None:
                return            
            anz = len(lst)
            if anz == 0:
                return

            self.tbl_details.setRowCount(0)
            self.tbl_details.setColumnCount(8)            
            # self.tbl_details.setHorizontalHeaderLabels(('lfd.Nr', 'FilmDatei', 'Typ', 'Größe', 'Datum', 'VideoAuflösung', 'Audio-Streams', 'Subtitles'))

            for pos in reversed(lst):
                obj = self.dbls.liste[pos]
                # print(obj)
                vid = obj.FullPath
                self.tbl_details.insertRow(0)
                self.tbl_details.setItem(0, 0, QTableWidgetItem(str(obj.lfd)))
                self.tbl_details.setItem(0, 1, QTableWidgetItem(str(obj.FullPath)))
                self.tbl_details.setItem(0, 2, QTableWidgetItem(str(obj.FilmExt)))
                # vlen = format_size(os.stat(vid).st_size)
                # vdat = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(vid).st_ctime))                
                vlen, vdat = getFilmSizeDat(vid)
                if vlen is None:
                    self.dbls.liste[pos].exist = False
                    self.tbl_details.item(0, 1).setForeground(QColor(250, 0, 0))
                    self.tbl_details.setItem(0, 3, QTableWidgetItem(" "))
                    self.tbl_details.setItem(0, 4, QTableWidgetItem(" "))                    
                else:
                    self.tbl_details.item(0, 1).setForeground(QColor(0, 0, 0))
                    self.tbl_details.setItem(0, 3, QTableWidgetItem(str(vlen)))                    
                    self.tbl_details.setItem(0, 4, QTableWidgetItem(str(vdat)))
                self.tbl_details.setItem(0, 5, QTableWidgetItem("-"))
                self.tbl_details.setItem(0, 6, QTableWidgetItem("-"))
                self.tbl_details.setItem(0, 7, QTableWidgetItem("-"))

            self.analyse()

    def videoStart(self, video):
        '''
        startet ein Video
        :param video: das zu startende Video
        :return:
        '''
        try:
            os.startfile(video)
        except:
            self.statusMeldung("Fehler: Kann das Video [{}] nicht starten!".format(video))            
        return
            
    def neueDatei(self):
        doubleRep.main(True)    # simple = True
        self.tbl_details.clear()
        self.tbl_fname.clear()
        self.dbls.zap()
        self.doublesLaden(csvDatei="doubleRep.csv")



    def statusMeldung(self, meldung):
        self.statusbar.showMessage(meldung)

    

# ------------------------------------------------------------------------------------------------------
# allg. Funktionen
# ------------------------------------------------------------------------------------------------------

def getFilmSizeDat(film):
    if os.path.isfile(film):
        vlen = format_size(os.stat(film).st_size)
        vdat = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(film).st_ctime))
    else:
        vlen = None
        vdat = None
    return vlen, vdat
                


if __name__ == '__main__':        
    app = QApplication(sys.argv)
    w = QMainWindow()
    form = MainApp()
#     form.show()
    app.exec_()
