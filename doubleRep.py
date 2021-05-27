# -*- coding: utf-8 -*-
'''
Created on 2021-02-17
@author: rg
doubleRep.py
Sucht Film-Doubletten

Version 1 :     rg 2021-02-17
        1.1:    rg 2021-04-18
                *_cut im dateinamen ignoriert
Erstelle eine Liste der Doubletten im VideoOrdner als Text-Datei und als CSV-Datei
Parameter:  "simple"    - Dateiname nur doubleRep.csv oder doubleRep.txt

'''

import sys
import os
import datetime

# das soll die Importe aus dem Ordner Liste mit einschließen...
sys.path.append(".\\liste")
import liste.liste as liste

# Dictionary, um ANSI-Sequenzen in der Ausgabe zu kapseln
ANSI = {
    "CYAN": "\033[95m",     # bright CYAN
    "BLUE": "\033[94m",     # bright BLUE
    "YELLOW": "\033[93m",   # bright YELLOW
    "GREEN": "\033[92m",    # bright GREEN
    "RED": "\033[91m",      # bright RED
    "ENDC": "\033[0m",      # Reset color
}

class const():
    vpath = "Y:\\video\\"
    skipExt = ["vdr", "conf", "py", "txt", "idx", "", "mp2", "BUP", "IFO", "VOB", ".", "DS Store", "srt"]

class dirInhalt():
    """
    die Inhalte der zu durchsuchenden Ordner werden hier vorgeladen
    """
    def __init__(self, FilmId, FilmName, FilmExt, FullPath):
        self.FilmId = FilmId        # laufende Nr
        self.FilmName = FilmName    # normierter Filmname
        self.FilmExt = FilmExt      # Ext ohne Punkt
        self.FullPath = FullPath    # kompletter Pfad
        self.Fertig = False         # Merker

    def __str__(self):
         return f"FilmID={self.FilmId}, FilmName={self.FilmName}, Ext={self.FilmExt}, fullPath={self.FullPath }"

    def setFertig(self):
        self.Fertig = True
        
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

    def __str__(self):
        return f"dID={self.dID}, lfd={self.lfd}, FilmName={self.FilmName}, Ext={self.FilmExt}, \nfullPath={self.FullPath}"

# Globale Variablen
videodir = liste.liste()
dblAnz = 0

def Inhalte_vorladen(vdir):
    global videodir
    nr = 0 
    for root, dirs, files in os.walk( vdir ):
        print(ANSI["ENDC"] + f'\r{nr:5} Dateien gelesen',  flush=True, end="")   # Zeilen-Nr ausgeben
        for f in files:
            nr += 1
            full_f = os.path.join(root, f)
            # name = os.path.basename(f)
            fn = normalize_f(f)
            fname, fext = os.path.splitext(fn)
            fext = fext[1:]
            if fext in const.skipExt:   # unliebsame Dateien direkt überspringen
                continue
            dir_o = dirInhalt(nr, fname, fext, full_f)
            videodir.append(dir_o)
            # print(f"Lade ({full_f})")
            if nr % 100 == 0:
                print(f'\r{nr:5} Dateien gelesen',  flush=True, end="")   # Zeilen-Nr ausgeben

    print(ANSI["ENDC"])
    return

def zerlegeName(full, name):
    if not name:
        name = os.path.basename(full)
    fn = normalize_f(name)
    fname, fext = os.path.splitext(fn)
    fext = fext[1:] 
    return fname, fext

def normalize_f(f: str) -> str:
    # mit normalize werden Dateinamen vereinfacht, um sie vergleichen zu können
    f1 = f.replace("_-_", " ")
    f1 = f1.replace("_", " ")
    f1 = f1.replace(" - ", " ")
    f1 = f1.replace("_cut", "")
    f1 = f1.replace("  ", " ")
    return(f1)

def finde_doublette(vidName, FilmListe):
    # # benutzt den normierten Filmnamen,
    # # um die "FilmListe" seiner Doubletten zu ergänzen

    global videodir
    global dblAnz
    lfd = 0
    dbls = videodir.findAll("FilmName", vidName)
    if len(dbls) > 1:
        dblAnz += 1        
        # Doubletten gefunden
        for pos in dbls:
            lfd +=1
            obj = videodir.findPos(pos)
            FilmListe.append(doublette(dblAnz, lfd, obj.FilmName, obj.FilmExt, obj.FullPath))
            obj.setFertig()          # dID, lfd, FilmName, FilmExt, FullPath
    return lfd

def dbl_Ausgabe(dbl, DateiName, now):
    # gibt den Inhalt der Doubletten-Liste sowohl als Txt-Datei als auch als CSV aus
    # Parameter:
    #   dbl:        Liste der Doubletten
    #   Dateiname:  Name der Ausgabedatei ohne Extension    

    with open(DateiName + ".csv", 'w', encoding="utf-8") as f:
        print(f"Doubletten-Suche vom {now}", file=f)
        for d in dbl.liste:
            print(f"{d.dID};{d.lfd};{d.FilmName};{d.FilmExt};{d.FullPath}",file=f)       # dID, lfd, FilmName, FilmExt, FullPath

    with open(DateiName + ".txt", 'w', encoding="utf-8") as f:
        print(f"Doubletten-Suche vom {now}", file=f)
        nr = -1
        o = dbl.findFirst()
        while not o is None:
            if not o.dID == nr:
                # erste Doublette            
                nr = o.dID
                print(" ", file=f)
                print("-"*120, file=f)
            print(f"{o.dID:4} {o.FilmName:20}   -  {o.FilmExt:5}  -  {o.FullPath}", file=f)
            o = dbl.findNext()

def main(simple):
    # StartMessage
    print(ANSI["BLUE"] + "=" * 80)
    print(f"doubleRep.py: Doubletten in {const.vpath} finden")
    print(ANSI["BLUE"] + "=" * 80)
    print("rg, 02.2021" + " "*65 + "V1.1" + ANSI["ENDC"])

    print(ANSI["GREEN"] + "Inhalte vorladen..." + ANSI["ENDC"])

    Inhalte_vorladen(const.vpath)    # videodir ist eine Liste der Videofiles

    print(ANSI["ENDC"] + f"{videodir.size} Dateien vorgeladen!" + ANSI["ENDC"])

    fl = liste.liste()
    doubleNr = 0
    fnr = 0

    print(ANSI["GREEN"] + "Doubletten suchen..." + ANSI["ENDC"])
    for vid in videodir.liste:   # scan über alle files
        
        if vid.Fertig:
            continue
        
        i = finde_doublette(vid.FilmName, fl)
        if i:
            doubleNr += 1
            print(ANSI["YELLOW"] + f'\r{doubleNr:4}' + ANSI["ENDC"] + ' Doubletten gefunden',  flush=True, end="")   # Zeilen-Nr ausgeben

    print(ANSI["ENDC"])

    # exit()

    # Ausgabe der Ergebnisse    
    now = f"{datetime.datetime.now():%Y-%m-%d_%H-%M}"
    if simple:
        DateiName = "doubleRep"
    else:
        DateiName = "doubleRep" + f"-{now}"

    dbl_Ausgabe(fl, DateiName, now)
    print("OK")


if __name__ == '__main__':
    os.system('')   # magic Call to enable ANSi-Seq.

    simple = False
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "simple":
            simple = True        
    main(simple)

    


