# -*- coding: UTF-8 -*-
import xlrd

class Execl(object):

    def __init__(self,config_path):
        self.config_path =config_path

    def readexcel(self):
        wb = xlrd.open_workbook(filename=self.config_path)  # 打开文件
        sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格
        rownum = sheet1.nrows
        datalist = []
        for i in range(rownum):
            datalist.append(sheet1.row_values(i))
        return datalist



