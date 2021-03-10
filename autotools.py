# -*- coding: utf-8 -*-
#pragma execution_character_set("utf-8")
# Form implementation generated from reading ui file 'autotools.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog,QWidget,QInputDialog,QLineEdit,QAbstractItemView
from PyQt5.QtCore import QStringListModel
import os
import json
import sys
import re
from massage import error_no_device,error_device_offline,error_no_selected,error_path
from replacefile import Execl

class Ui_MainWindow(QWidget):

    def __init__(self, name = 'MainForm',):
        super().__init__()
        self.cwd = os.getcwd() # 获取当前程序文件位置
        self.device = None
        self.output_path = None
        self.output_dir = None
        self.slm = None
        self.file_count = 0
        self.selected_file = False
        self.device_online = False

    #问配置文件
    def write_config_file(self,json_config):
        jsondata = json.dumps(json_config, ensure_ascii=False)
        f = open('config_info.json', 'w', encoding="utf-8")
        f.write(jsondata)
        f.close()

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(446, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 446, 480))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.tabWidget.addTab(self.tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 446, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tab_UI_init()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def tab_UI_init(self):
        self.btn_connect = QtWidgets.QPushButton(self.tab)
        self.btn_connect.setGeometry(QtCore.QRect(20, 10, 75, 31))
        self.btn_connect.setObjectName("btn_connect")
        self.label_current = QtWidgets.QLabel(self.tab)
        self.label_current.setGeometry(QtCore.QRect(110, 10, 150, 31))
        self.label_current.setObjectName("label_current")
        self.label_file_type = QtWidgets.QLabel(self.tab)
        self.label_file_type.setGeometry(QtCore.QRect(20, 60, 131, 21))
        self.label_file_type.setObjectName("label_file_type")
        self.comboBox_file_type = QtWidgets.QComboBox(self.tab)
        self.comboBox_file_type.setGeometry(QtCore.QRect(160, 60, 121, 21))
        self.comboBox_file_type.setObjectName("comboBox_file_type")
        self.btn_download = QtWidgets.QPushButton(self.tab)
        self.btn_download.setGeometry(QtCore.QRect(310, 56, 91, 31))
        self.btn_download.setObjectName("btn_download")
        self.listView = QtWidgets.QListView(self.tab)
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listView.setGeometry(QtCore.QRect(20, 110, 401, 330))

        self.listView.setObjectName("listView")
        self.label_file_list = QtWidgets.QLabel(self.tab)
        self.label_file_list.setGeometry(QtCore.QRect(20, 90, 54, 12))
        self.label_file_list.setObjectName("label_file_list")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "文件导出工具（测试专用）"))
        MainWindow.setWindowIcon(QIcon('tools.png'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "ADB工具"))
        self.btn_connect.setText(_translate("MainWindow", "连接/刷新"))
        self.label_current.setText(_translate("MainWindow", "当前无设备链接"))
        self.label_file_type.setText(_translate("MainWindow", "选择要导出的文件类型："))
        self.btn_download.setText(_translate("MainWindow", "导出文件"))
        self.label_file_list.setText(_translate("MainWindow", "文件列表："))
        self.init_comboBox()

        #绑定信号
        self.bind_event()

        self.slm = QStringListModel()
        self.slm.setStringList([])
        self.listView.setModel(self.slm)

    def init_comboBox(self):
        config_list = read_execl()
        for item in config_list:
            self.comboBox_file_type.addItem(item[0])
        self.output_path = config_list[0][1]
        self.output_dir = self.cwd+"\\"+config_list[0][0]

    def bind_event(self):
        self.btn_connect.clicked.connect(self.slot_btn_connect)
        self.btn_download.clicked.connect(self.slot_btn_download)
        self.comboBox_file_type.currentIndexChanged.connect(self.slot_combox_change)

    def slot_btn_connect(self):
        res = os.popen("adb devices").read()
        res = re.sub("List of devices attached\n","",res)
        if re.findall(".*?device",res):
            print(res)
            device = str(res.split("\t")[0])
            self.label_current.setText("当前设备："+device+" 已连接")
            self.device = device
            self.device_online = True
            self.loading_file()
        else:
            self.label_current.setText("当前无设备链接")
            self.device_online = False
            self.device = None
            if self.slm:
                self.slm.removeRows(0,self.file_count)
                self.file_count = 0

    def slot_btn_download(self):
        selectedfile_list = self.listView.selectionModel().selectedIndexes()
        if selectedfile_list and self.device_online:
            for item in selectedfile_list:
                print(item.data())
                if not os.path.exists(self.output_dir):
                    os.system("mkdir %s"%self.output_dir)
                ret = os.popen("adb -s %s pull %s %s"%(self.device,self.output_path+"/"+item.data(),self.output_dir))
                if not re.findall(".*?not found", ret.read()):
                    ret.readlines()
                else:
                    error_device_offline()
                    self.slot_btn_connect()
        elif not self.device_online:
            error_no_device()
        else:
            error_no_selected()

    def slot_combox_change(self):
        config_list = read_execl()
        self.output_path = config_list[self.comboBox_file_type.currentIndex()][1]
        self.output_dir = self.cwd + "\\" + config_list[self.comboBox_file_type.currentIndex()][0]
        self.loading_file()

    def loading_file(self):
        if self.slm:
            self.slm.removeRows(0, self.file_count)
            self.file_count = 0
        file_list = self.file_list()
        if file_list:
            file_list.sort(reverse=True)
            self.file_count = len(file_list)
            self.slm.setStringList(file_list)
            self.listView.setModel(self.slm)
        else:
            error_path()

    def file_list(self):
        print("adb -s %s shell ls %s" % (self.device,self.output_path))
        pip = os.popen("adb -s %s shell ls %s" % (self.device,self.output_path))
        file_list = pip.buffer.read().decode(encoding="utf8")
        file_list = file_list.split("\n")
        file_list.pop(-1)
        print(file_list)
        return file_list

def read_execl():
    filepath = sys.argv[0]
    realpath = os.path.realpath(filepath)
    current_path = os.path.dirname(realpath)
    os.chdir(current_path)
    cwd = os.getcwd()
    execl_object = Execl(cwd + "\\config.xlsx")
    config_list = execl_object.readexcel()
    return config_list