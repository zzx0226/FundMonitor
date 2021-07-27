'''
Description: 
Version: 1.0
Autor: Zhangzixu
Date: 2020-07-18 16:34:11
LastEditors: Zhangzixu
LastEditTime: 2021-07-27 13:04:05
'''
import requests
import splitvalue
import json
import csv
import time
import sys
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
xdictValue = np.load('xdict.npy', allow_pickle=True).item()

print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))

RowNum = splitvalue.ConfirmRow()

TitleName = [0 for _ in range(RowNum + 1)]
TimeValue = [0 for _ in range(RowNum + 1)]

sFileName = open('list.csv', encoding='UTF-8-sig')
rows = csv.reader(sFileName)

j = 0
for row in rows:
    try:
        data = requests.get('http://fund.10jqka.com.cn/data/client/myfund/{}/'.format(row[0]))
        FundData = json.loads(data.text)['data'][0]
        FundName = FundData['name']
        hqcode = FundData['hqcode']
        url = "http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_{}&start=0930&".format(hqcode)

        data = requests.get(url)
        TimeValue[j] = data.content.decode('utf-8')
        TitleName[j] = FundName
        j += 1
    except:
        print(row, "error")

#splitvalue.DrawSZ()
for k in range(len(TimeValue)):
    try:
        xdict, StockData, Rate, ref, Price = splitvalue.SplitTimeValue(TimeValue[k])
        splitvalue.PlotCurve(xdictValue, StockData, TitleName[k], Rate, Price)
    except:
        print(k, "error")

# if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#     QtGui.QApplication.instance().exec_()