import sys
import csv
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters


def SplitTimeValue(OriginValue):

    OriginValue = OriginValue.split(';')
    ref = OriginValue[2].split(",")
    ref = eval(ref[2])
    OriginValue = OriginValue[2:]

    ValueArray = np.array([])
    Price = np.array([])
    TimeList = []
    for i in OriginValue:
        SignalValue = i.split(",", 3)
        Value = SignalValue[1]
        TimeVal = SignalValue[0]
        Value = eval(Value)
        Price = np.append(Price, Value)
        Value = ((Value - ref) / ref) * 100
        ValueArray = np.append(ValueArray, Value)
        TimeVal = list(TimeVal)
        TimeVal.insert(2, ":")
        if ((TimeVal[-2] == '0' and TimeVal[-1] == '0') or (TimeVal[-2] == '3' and TimeVal[-1] == '0') or (TimeVal == ['0', '9', ':', '3', '1'])):
            pass
        else:
            TimeVal = ''

        if TimeVal == ['1', '1', ':', '3', '0']:
            TimeVal = ''

        TimeVal = ''.join(TimeVal)
        TimeList.append(TimeVal)
    Rate = f'{Value:.2f} %'
    xdict = dict(enumerate(TimeList))

    return xdict, ValueArray, Rate, ref, Price


def SlectColor(rate):
    if rate > 0:
        color = "#F00"
    else:
        color = "#0F0"
    return color


def ReturnTriangle(rate):
    if rate > 0:
        triangle = "▲"
    else:
        triangle = "▼"
    return triangle


def PlotCurve(xdict, StockData, TitleName, Rate, Price):

    win.nextRow()
    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)
    stringaxis = pg.AxisItem(orientation='bottom')
    stringaxis.setTicks([xdict.items()])
    Price = np.array(Price)
    x = len(StockData) - 1
    color = SlectColor(StockData[-1])
    triangle = ReturnTriangle(StockData[-1])
    plot = win.addPlot(title='<div style="text-align: center"><span style="color: {}; font-size: 25pt;">'.format(color) + '<b>' + TitleName + str(f'      {triangle}{StockData[x]:.2f}%') + '</b>',
                       axisItems={'bottom': stringaxis})

    ShowRate = '<div style="text-align: center"><span style="color: #FFF; font-size: 18pt;">' + str(f'{Price[x]:.2f} RMB') + '</span><br><span style="color: {}; font-size: 18pt;">'.format(
        color) + str(f'{StockData[x]:.2f}%') + '</span></div>'
    text = pg.TextItem(html=ShowRate, anchor=(0, 0), angle=0)
    plot.addItem(text)
    text.setPos(x, StockData[x])

    x = np.where(Price == Price.max())[0][0]
    color = SlectColor(StockData[x])
    ShowMax = '<div style="text-align: center"><span style="color: #FFF; font-size: 18pt;">' + str(f'{Price[x]:.2f} RMB') + '</span><br><span style="color: {}; font-size: 18pt;">'.format(color) + str(
        f'{StockData[x]:.2f}%') + '</span></div>'
    TextMax = pg.TextItem(html=ShowMax, anchor=(-0.3, 0.5))
    plot.addItem(TextMax)

    TextMax.setPos(x, StockData[x])

    x = np.where(Price == Price.min())[0][0]
    color = SlectColor(StockData[x])
    ShowMin = '<div style="text-align: center"><span style="color: #FFF; font-size: 18pt;">' + str(f'{Price[x]:.2f} RMB') + '</span><br><span style="color: {}; font-size: 18pt;">'.format(color) + str(
        f'{StockData[x]:.2f}%') + '</span></div>'
    TextMin = pg.TextItem(html=ShowMin, anchor=(-0.3, 0.5))
    plot.addItem(TextMin)

    TextMin.setPos(x, StockData[x])

    curve = plot.plot(StockData, pen=pg.mkPen(color='w', width=2))
    ex = pyqtgraph.exporters.ImageExporter(win.scene())
    ex.export(fileName="/home/pi/MagicMirror/modules/MMM-EasyPix/pix/1.jpg")


def ConfirmRow():
    sFileName = open('list.csv', encoding='UTF-8')
    rows = csv.reader(sFileName)
    for i, row in enumerate(rows):
        pass
    return i


win = pg.GraphicsWindow()
win.resize(1500, 1200)

if __name__ == '__main__':
    StocksValue = open("1.txt")
    StocksValue1 = open("2.txt")

    xdictValue = np.load('xdict.npy', allow_pickle=True).item()
    # np.save('xdict.npy', xdict)

    sFileName = open('list.csv', encoding='UTF-8')
    rows = csv.reader(sFileName)

    #SotckList = [][]
    TimeValue = StocksValue.read()
    TimeValue1 = StocksValue1.read()

    xdict, StockData, Rate, ref, Price = SplitTimeValue(TimeValue)

    xdict1, StockData1, Rate1, ref1, Price1 = SplitTimeValue(TimeValue1)

    TitleName = [0 for _ in range(ConfirmRow() + 1)]

    for j, row in enumerate(rows):
        TitleName[j] = row[0]

    PlotCurve(xdictValue, StockData, TitleName[0], Rate, Price)

    PlotCurve(xdictValue, StockData1, TitleName[1], Rate1, Price1)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
