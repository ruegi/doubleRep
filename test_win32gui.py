import win32gui
import win32clipboard as clip
from time import sleep
import sys
import subprocess
# import pyautogui
import keyboard

# Hinweis: beide Module, keyboard & pyautogui habe ich getestet und laufen. Ich hatte mich für keyboard entschieden, weil es leichgewichtiger ist,
#          aber pyautogui kann deutlich mehr (was ich hier nicht brauche)

SW_NORMAL = 1
SW_SHOW = 5
SW_RESTORE = 9

def find_window_movetop(name):
        hwnd = win32gui.FindWindow(None, name)
        if hwnd == 0:
            print("Das gefundene Handle ist 0!")
            return None
        else:
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, SW_RESTORE)
            win32gui.ShowWindow(hwnd,SW_SHOW)
            win32gui.SetForegroundWindow(hwnd)
            # rect = win32gui.GetWindowRect(hwnd)
            print("Handle gefunden!")
            return hwnd
        
        sleep(0.2)

def clipboard_put(hwnd, data):
    if sys.platform == "win32":        
        clip.OpenClipboard(hwnd)
        clip.EmptyClipboard()
        clip.SetClipboardText(data, clip.CF_UNICODETEXT)
        clip.CloseClipboard()
    # elif sys.platform.startswith("linux"):
    #     proc = subprocess.Popen(("xsel", "-i", "-b", "-l", "/dev/null"),
    #                             stdin=subprocess.PIPE)
    #     proc.stdin.write(data.encode("utf-8"))
    #     proc.stdin.close()
    #     proc.wait()
    # else:
    #     raise RuntimeError("Unsupported platform") 

hwnd = find_window_movetop("VidSuch - Suche von Videos im Archiv")
if not hwnd is None:
    # Zwischablage füllen und anzeigen per F5
    clipboard_put(hwnd, "James Bond")
#    pyautogui.press('f5')
    keyboard.send("F5")
    sleep(0.5)
#    pyautogui.press('enter')
    keyboard.send("enter")


