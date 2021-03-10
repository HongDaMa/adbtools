# -- coding: utf-8 --
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets

def error_no_device():
    reply = QMessageBox()
    reply.setWindowTitle('错误')
    reply.setText('当前未连接设备！')
    reply.addButton(QtWidgets.QPushButton('好的'), QMessageBox.YesRole)
    reply.exec()

def error_device_offline():
    reply = QMessageBox()
    reply.setWindowTitle('错误')
    reply.setText('设备已断开链接！')
    reply.addButton(QtWidgets.QPushButton('好的'), QMessageBox.YesRole)
    reply.exec()

def error_no_selected():
    reply = QMessageBox()
    reply.setWindowTitle('错误')
    reply.setText('请选择要导出的文件！')
    reply.addButton(QtWidgets.QPushButton('好的'), QMessageBox.YesRole)
    reply.exec()

def error_path():
    reply = QMessageBox()
    reply.setWindowTitle('错误')
    reply.setText('当前路径无文件或者路径配置错误！')
    reply.addButton(QtWidgets.QPushButton('好的'), QMessageBox.YesRole)
    reply.exec()