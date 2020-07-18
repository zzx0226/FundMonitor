import sys
import csv
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import requests
import json

def GetTitle():
    title = "Fund Monitor     上证指数 ："+ str(GetSZ())
    return title
def GetSZ():
    url='https://hq.sinajs.cn/?list=sh000001,sz39'
    headers={"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"}
    data=requests.get(url).text
    Shangzheng = data.split(",")[1]
    Shangzheng=f'{eval(Shangzheng):.2f}'
    return Shangzheng

def SplitTimeValue(OriginValue):

    OriginValue = OriginValue.split(';')
    ref = OriginValue[2].split(",")
    ref = eval(ref[2])
    OriginValue = OriginValue[2:]

    ValueArray =np.array([])
    Price =np.array([])
    TimeList = []
    for i in OriginValue:
        SignalValue = i.split(",",3)
        Value=SignalValue[1]
        TimeVal = SignalValue[0]
        Value=eval(Value)
        Price=np.append(Price,Value)
        Value = ((Value-ref)/ref)*100
        ValueArray=np.append(ValueArray,Value)
        TimeVal = list(TimeVal)
        TimeVal.insert(2,":")
        if((TimeVal[-2]=='0' and TimeVal[-1]=='0') or (TimeVal[-2]=='3' and TimeVal[-1]=='0') or (TimeVal==['0','9',':','3','1'])):
            pass
        else :
            TimeVal = ''

        if TimeVal==['1','1',':','3','0'] :
            TimeVal = ''

        TimeVal = ''.join(TimeVal)
        TimeList.append(TimeVal)
    Rate = f'{Value:.2f} %'
    xdict = dict(enumerate(TimeList)) 
    return xdict,ValueArray,Rate,ref,Price

def PlotCurve(xdict,StockData,TitleName,Rate,Price):

    win.nextRow()
    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)
    stringaxis = pg.AxisItem(orientation='bottom')
    stringaxis.setTicks([xdict.items()])
    plot = win.addPlot(title='<b>'+TitleName+'</b>',axisItems={'bottom': stringaxis})

    x = len(StockData)-1
    ShowRate = '<div style="text-align: center"><span style="color: #FFF; font-size: 10pt;">'+str(f'{Price[x]:.2f} RMB')+'</span><br><span style="color: #FF0; font-size: 10pt;">'+str(f'{StockData[x]:.2f}%')+'</span></div>'
    text = pg.TextItem(html=ShowRate, anchor=(0,0), angle=0)
    plot.addItem(text)
    text.setPos(x, StockData[x])

    Price=np.array(Price)

    x=np.where(Price==Price.max())[0][0]
    ShowMax = '<div style="text-align: center"><span style="color: #FFF; font-size: 10pt;">'+str(f'{Price[x]:.2f} RMB')+'</span><br><span style="color: #FF0; font-size: 10pt;">'+str(f'{StockData[x]:.2f}%')+'</span></div>'
    TextMax = pg.TextItem(html=ShowMax, anchor=(-0.3,0.5))
    plot.addItem(TextMax)
   
    TextMax.setPos(x, StockData[x])


    x=np.where(Price==Price.min())[0][0]
    ShowMin = '<div style="text-align: center"><span style="color: #FFF; font-size: 10pt;">'+str(f'{Price[x]:.2f} RMB')+'</span><br><span style="color: #FF0; font-size: 10pt;">'+str(f'{StockData[x]:.2f}%')+'</span></div>'
    TextMin = pg.TextItem(html=ShowMin, anchor=(-0.3,0.5))
    plot.addItem(TextMin)
    
    TextMin.setPos(x, StockData[x])
    
    curve = plot.plot(StockData,pen=(255,0,0), name="Red curve")

def ConfirmRow():
    sFileName=open('list.csv', encoding='UTF-8')
    rows=csv.reader(sFileName)
    for i,row in enumerate(rows):
        pass
    return i

win = pg.GraphicsLayoutWidget(show=True, title=GetTitle())
win.resize(1500,1000)
