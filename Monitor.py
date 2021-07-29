'''
Description: 
Version: 1.0
Autor: Zhangzixu
Date: 2021-07-28 11:42:20
LastEditors: Zhangzixu
LastEditTime: 2021-07-29 10:33:56
'''
'''
Description: 
Version: 1.0
Autor: Zhangzixu
Date: 2021-07-28 11:42:20
LastEditors: Zhangzixu
LastEditTime: 2021-07-28 15:16:19
'''
'''
Description: 
Version: 1.0
Autor: Zhangzixu
Date: 2021-07-28 11:42:20
LastEditors: Zhangzixu
LastEditTime: 2021-07-28 11:42:35
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
StockData = [0 for _ in range(RowNum + 1)]
Rate = [0 for _ in range(RowNum + 1)]
# ref = [0 for _ in range(RowNum + 1)]
Price = [0 for _ in range(RowNum + 1)]
Values = [0 for _ in range(RowNum + 1)]

# TimeValue = [0 for _ in range(RowNum + 1)]

sFileName = open('list.csv', encoding='UTF-8-sig')
rows = csv.reader(sFileName)

for j, row in enumerate(rows):
    try:
        FundNum = row[0].zfill(6)
        data = requests.get('http://fund.10jqka.com.cn/data/client/myfund/{}/'.format(FundNum))
        FundData = json.loads(data.text)['data'][0]
        FundName = FundData['name']
        hqcode = FundData['hqcode']
        url = "http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_{}&start=0930&".format(hqcode)

        data = requests.get(url)
        # TimeValue[j] = data.content.decode('utf-8')
        TitleName[j] = FundName
        xdict, StockData[j], Rate[j], Price[j], Values[j] = splitvalue.SplitTimeValue(data.content.decode('utf-8'))
        print(TitleName[j], Rate[j])

    except:
        print(FundNum, "error")
        
NewSort = sorted(Values, reverse=True)
Values = np.array(Values)

for Value in NewSort:
    try:
        PlotNum = np.where(Values == Value)[0][0]
        splitvalue.PlotCurve(xdict, StockData[PlotNum], TitleName[PlotNum], Price[PlotNum])
        print(TitleName[PlotNum], Rate[PlotNum])
    except:
        print(PlotNum, "error")

if ((sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION')) and sys.platform == 'win32':
    QtGui.QApplication.instance().exec_()