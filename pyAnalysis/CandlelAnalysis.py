# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 12:45:42 2018

@author: Prashant Kumar

@mail: kr.prashant94@gmail.com

@supervision: Mr. Dilip Kumar
"""
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.animation as animation

import numpy as np
import datetime as dt
import time
import os

class CandlelAnalysis:
    """
    Description
    -------
    **pyAnalysis** class provides the functionality for generating real time __graph form continuous input.
    """
    __fig1 = plt.figure(1)
    __fig2 = plt.figure(2)
    __ax1 = __fig1.add_subplot(1,1,1)
    __ax2 = __fig2.add_subplot(1,1,1)
    __stock_data, __x_index = [], []
    __ohlc = []
    __ohlcHA = []
    __date = []
    __pos = 20
    __dataBase = ''
    def __init__(self, ploatDelay, dataBase):
        self.initTime = time.time()
        self.ploatDelay = ploatDelay
        self.__dataBase = dataBase

    def __initGraph(self):
        plt.figure(1)
        self.__stock_data = np.load(os.path.dirname(__file__)+"/"+self.__dataBase)
        closep = []
        highp = []
        lowp = []
        openp = []
        volume = []
        dtformat = '%Y-%m-%dT%H:%M:%S%z'
        dformat= '%Y-%m-%d %H:%M'
        for i in range(0, len(self.__stock_data)):
            ld = dt.datetime.strptime(self.__stock_data[i]['date'], dtformat)
            self.__date.append(ld.strftime(dformat))
            self.__x_index.append(i)
            closep.append(self.__stock_data[i]['close'])
            highp.append(self.__stock_data[i]['high'])
            lowp.append(self.__stock_data[i]['low'])
            openp.append(self.__stock_data[i]['open'])
            volume.append(self.__stock_data[i]['volume'])
            
        x = 0
        y = len(self.__date)
        while x < y:
            append_me = self.__x_index[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
            self.__ohlc.append(append_me)
            x+=1
            
        candlestick_ohlc(self.__ax1, self.__ohlc[0:self.__pos], width=0.4, colorup='#77d879', colordown='#db3f3f')
    
        for label in self.__ax1.xaxis.get_ticklabels():
            label.set_rotation(90)
    
        self.__ax1.grid(True)
        plt.xlim(0, self.__pos)
        plt.setp(self.__ax1, xticks=self.__x_index[0:self.__pos], xticklabels=self.__date[0:self.__pos])
#        self.__ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title("Candle")
        plt.legend(("Down", "Up"))
        plt.subplots_adjust(left=0.09, bottom=0.40, right=0.94, top=0.90, wspace=0.2, hspace=0)
        return
    def __graph(self, frame):
        plt.figure(1)
        
        for label in self.__ax2.xaxis.get_ticklabels():
            label.set_rotation(90)
        candlestick_ohlc(self.__ax1, self.__ohlc[0:self.__pos], width=0.4, colorup='#77d879', colordown='#db3f3f')
        plt.setp(self.__ax1, xticks=self.__x_index[0:self.__pos], xticklabels=self.__date[0:self.__pos])
#        self.__ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        plt.xlim(self.__pos-20, self.__pos)
        self.__pos+=1
        return
    
    def __initHACandel(self):
        plt.figure(2)        
        closep = []
        highp = []
        lowp = []
        openp = []
        volume = []
        dtformat = '%Y-%m-%dT%H:%M:%S%z'
        dformat= '%Y-%m-%d %H:%M'
        for i in range(0, len(self.__stock_data)):
            ld = dt.datetime.strptime(self.__stock_data[i]['date'], dtformat)
            self.__date.append(ld.strftime(dformat))
            self.__x_index.append(i)
            closep.append(self.__stock_data[i]['close'])
            highp.append(self.__stock_data[i]['high'])
            lowp.append(self.__stock_data[i]['low'])
            openp.append(self.__stock_data[i]['open'])
            volume.append(self.__stock_data[i]['volume'])
        
        x = 1
        y = len(closep)
        xOpen = [openp[0]]
        xClose = [closep[0]]
        while x < y:
            xOpen.append((xOpen[x-1]+xClose[x-1])/2)
            xClose.append((openp[x]+closep[x]+highp[x]+lowp[x])/4)
            xMax = np.amax([highp[x], xOpen[x], xClose[x]])
            xMin = np.amin([highp[x], xOpen[x], xClose[x]])
            append_me = self.__x_index[x], xOpen[x], xMax, xMin, xClose[x], volume[x]
            self.__ohlcHA.append(append_me)
            x+=1
        
        self.__ax2.grid(True)
        candlestick_ohlc(self.__ax2, self.__ohlcHA[0:self.__pos], width=0.4, colorup='#77d879', colordown='#db3f3f')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title("HA Candle")
        plt.legend(("Down", "Up"))
        plt.subplots_adjust(left=0.09, bottom=0.40, right=0.94, top=0.90, wspace=0.2, hspace=0)
        return
    def __updateHA(self, frame):
        plt.figure(2)
        candlestick_ohlc(self.__ax2, self.__ohlcHA[0:self.__pos], width=0.4, colorup='#77d879', colordown='#db3f3f')
        plt.setp(self.__ax2, xticks=self.__x_index[0:self.__pos], xticklabels=self.__date[0:self.__pos])
#        self.__ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        plt.xlim(self.__pos-20, self.__pos)
        self.__pos+=1
        return
        return
    def genrateCandlelAnalysis(self):
        """
        Description
        -------
        **genrateCandlelAnalysis()** two figure. using FuncAnimation().
        Need to import matplotlib.animation as animation.
        *fugure 1* : Candlel Analysis of data
        *fugure 2* : HA Candlel Analysis of data
        
        Parameters
        ----------
        ploatDelay *int*
            Time delay form ploting __graph.
        dataBase *string*
            Database name (must be in .npy format)
        
        Examples
        --------
        >>> box_plot.genrateGraph()
        """
        plt.figure(1)
        ani1 = animation.FuncAnimation(self.__fig1, self.__graph, init_func=self.__initGraph, interval=1000, blit=False)
        plt.figure(2)
        ani2 = animation.FuncAnimation(self.__fig2, self.__updateHA, init_func=self.__initHACandel, interval=1000, blit=False)
        plt.show()
