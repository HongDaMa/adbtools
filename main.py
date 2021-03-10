# -*- coding: UTF-8 -*-
#pragma execution_character_set("utf-8")
import sys
import autotools
from PyQt5.QtWidgets import QApplication, QMainWindow

import ctypes

def hideConsole():
    """
    Hides the console window in GUI mode. Necessary for frozen application, because
    this application support both, command line processing AND GUI mode and theirfor
    cannot be run via pythonw.exe.
    """

    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        # if you wanted to close the handles...
        #ctypes.windll.kernel32.CloseHandle(whnd)

def showConsole():
    """Unhides console window"""
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 1)

if __name__ == '__main__':
    hideConsole()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = autotools.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())