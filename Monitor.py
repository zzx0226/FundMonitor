'''
Description: 
Version: 1.0
Autor: Zhangzixu
Date: 2021-07-27 10:25:54
LastEditors: Zhangzixu
LastEditTime: 2021-07-27 13:01:29
'''
import requests
import splitvalue
#from bs4 import BeautifulSoup
import json
import csv
import time
import sys
from pyqtgraph.Qt import QtGui, QtCore
# import pyqtgraph as pg
import numpy as np

# headers = {"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"}
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

if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()