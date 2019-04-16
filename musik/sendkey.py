import win32gui
import sys

from ctypes import *
import win32service
import win32serviceutil
import win32api
import win32event
import win32evtlogutil
import os
import win32con

from win32con import SWP_FRAMECHANGED
from win32con import SWP_NOMOVE
from win32con import SWP_NOSIZE
from win32con import SWP_NOZORDER
from win32con import SW_HIDE
from win32con import SW_FORCEMINIMIZE
from win32con import SW_SHOWNORMAL

from win32con import GW_OWNER
from win32con import GWL_STYLE
from win32con import GWL_EXSTYLE

from win32con import WM_CLOSE

from win32con import WS_CAPTION
from win32con import WS_EX_APPWINDOW
from win32con import WS_EX_CONTROLPARENT
from win32con import WS_EX_TOOLWINDOW
from win32con import WS_EX_WINDOWEDGE
from win32con import WS_EX_LAYERED
from win32con import LWA_ALPHA

import win32gui
import winxpgui

EnumWindows = windll.user32.EnumWindows
EnumWindowsProc = WINFUNCTYPE(c_bool, c_int, POINTER(c_int))
GetWindowText = windll.user32.GetWindowTextW
GetWindowTextLength = windll.user32.GetWindowTextLengthW
IsWindowVisible = windll.user32.IsWindowVisible
GetClassName = windll.user32.GetClassNameW
BringWindowToTop = windll.user32.BringWindowToTop
GetForegroundWindow = windll.user32.GetForegroundWindow

titles = []


def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        classname = create_unicode_buffer(100 + 1)
        GetClassName(hwnd, classname, 100 + 1)
        buff = create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append((hwnd, buff.value.encode, classname.value, windll.user32.IsIconic(hwnd)))
    return True


EnumWindows(EnumWindowsProc(foreach_window), 0)


def refresh_wins():
    del titles[:]
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles


def find_window(title):
    title = title.encode('utf8')
    newest_titles = refresh_wins()
    for item in newest_titles:
        if title in item[1]():
            return item
    return False


# test
title = find_window("Chrome")
if title:
    print("found")
else:
    print("not found")


hwndMain = win32gui.FindWindow(None, 'Document1 - Word')
hwndEdit = win32gui.FindWindowEx( 0, 0, None, 'Document1 - Word' )
if(hwndMain != 0):
    win32api.PostMessage(hwndEdit, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32api.PostMessage(hwndEdit, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

titles = []


def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
    return True


EnumWindows(EnumWindowsProc(foreach_window), 0)

print(titles)

import win32gui
import win32con
import win32api
from time import sleep
#[hwnd] No matter what people tell you, this is the handle meaning unique ID,
#["Notepad"] This is the application main/parent name, an easy way to check for examples is in Task Manager
#["test - Notepad"] This is the application sub/child name, an easy way to check for examples is in Task Manager clicking dropdown arrow
#hwndMain = win32gui.FindWindow("Notepad", "test - Notepad") this returns the main/parent Unique ID
hwndMain = win32gui.FindWindow(None, "untitled - Notepad")
#["hwndMain"] this is the main/parent Unique ID used to get the sub/child Unique ID
#[win32con.GW_CHILD] I havent tested it full, but this DOES get a sub/child Unique ID, if there are multiple you'd have too loop through it, or look for other documention, or i may edit this at some point ;)
#hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD) this returns the sub/child Unique ID
hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
#print(hwndMain) #you can use this to see main/parent Unique ID
#print(hwndChild)  #you can use this to see sub/child Unique ID
#While(True) Will always run and continue to run indefinitely
while(True):
    #[hwndChild] this is the Unique ID of the sub/child application/proccess
    #[win32con.WM_CHAR] This sets what PostMessage Expects for input theres KeyDown and KeyUp as well
    #[0x44] hex code for D
    #[0]No clue, good luck!
    #temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x44, 0) returns key sent
    temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x44, 0)
    #print(temp) prints the returned value of temp, into the console
    print(temp)
    #sleep(1) this waits 1 second before looping through again
    sleep(1)