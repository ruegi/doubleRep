# -*- coding: utf-8 -*-
"""
Created on 2020-05-19

@author: rg

Modul filmAnalyse.py

ermöglicht die Gewinnung von FilmInfos

rg, ab 05.2021
    ab 2021-05-20   Umstellung von csv auf json

"""
import subprocess
import json

def _runit(cmd):
    try:
        pobj = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="utf-8")
    except:
        print("Unbekannter Fehler beim run-Aufruf!")
        print("Unexpected error:{0}".format(sys.exc_info()[0]))
    return pobj

def getFilmDetails(filmname):
    cmd = 'C:\\ffmpeg\\bin\\ffprobe -hide_banner -show_streams -print_format json ' + '"' + filmname + '"'
    # print(cmd)
    pobj = _runit(cmd)
    ausg = pobj.stdout
    if pobj.returncode > 0:
        ausg = f'Fehler {pobj.returncode}\n' + ausg
        return None
    ausg = _FilmInfosLesen(ausg)
    return ausg


def _FilmInfosLesen(txt: str) -> str: 
    # liest die Ausgabe von ffprobe ein und gibt eine Liste mit 3 EInträgen aus:
    # - Video-Auflösung, Audio-Streams, Subtitles    
    # print(txt)
    if  txt is None:                        # txt.strip() == "":
        return [" "," "," "]

    video = ""    #txt + "\n\n"
    audio = ""
    subt = ""
    try:
        filmInfo = json.loads(txt)
    except ValueError:
        return [video, audio, subt]

    audioAnz = 0
    lfdnr = 0
    for stream in filmInfo['streams']:
        streamTyp = stream["codec_type"]
        if streamTyp == "video":
            video = video + stream["codec_name"] + " (" + str(stream["width"]) + "x" + str(stream["height"]) + ") "
        elif streamTyp == "audio":            
            audioAnz += 1
            lang = getStreamLang(stream)
            audio = "| ".join([audio, stream["codec_name"]]) + " (" + lang + ") " 
            if stream["codec_name"] in ["mp2","ac3"]:
                audio = audio + stream["bit_rate"][0:3] + "KHz "
                audio = audio + stream["channel_layout"]
            else:
                pass
        elif streamTyp == "subtitle":
            lang = getStreamLang(stream)
            subt = " | ".join([subt, lang])
        lfdnr +=1

    audio = "(" + str(audioAnz) + ") " + audio
    return [video, audio, subt]

def getStreamLang(stream):
    if "tags" in [*stream]:
        if "language" in list(stream["tags"].keys()):
            return stream["tags"]["language"]
    return "Nix"


if __name__ == '__main__':
    print(getFilmDetails( r"e:\Filme\schnitt\Der_Eid.mkv"))
    print(getFilmDetails( r"e:\Filme\schnitt\Harter_Brocken_-_Der_Waffendeal.mkv"))
    print(getFilmDetails( r"Y:\video\musik\klassik\Felix_Mendelssohn_Bartholdy_Ein_Sommernachtstraum.mpg"))
    print(getFilmDetails( r"Y:\video\Unterhaltung\Kinder\Asterix_&_Obelix_gegen_Cäsar.mpg"))