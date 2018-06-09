# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 11:15:00 2017

@author: Prashant Kumar

@mail: kr.prashant94@gmail.com

@supervision: Dr. Dilip Kumar

"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import csv
import time
import datetime
import random
import numpy as np
import matplotlib.animation as animation
import threading
import pandas
import os

class LineAnalysis:
    """
    Description
    -------
    **pyAnalysis** class provides the functionality for generating real time __graph form continuous input.
    """
    __dataColumns = ['Time','Data','Average','SD']
    __dataALog = pandas.DataFrame(columns = __dataColumns)
    __dataBLog = pandas.DataFrame(columns = __dataColumns)
    
    __fig = plt.figure()
    __fig.subplots_adjust(hspace = 0.8, wspace = 0.4)
    plt.rc('font', size=8)          # controls default text sizes
    
    __ax1 = __fig.add_subplot(2,3,1)
    __ax2 = __fig.add_subplot(2,3,2)
    __ax3 = __fig.add_subplot(2,3,3)
    __ax4 = __fig.add_subplot(2,3,4)
    __ax5 = __fig.add_subplot(2,3,5)
    __ax6 = __fig.add_subplot(2,3,6)
    
    __ax6.get_xaxis().set_visible(False)
    __ax6.get_yaxis().set_visible(False)
    plt.axis('off')
    
    __xdata, __dataA, __dataB, __dataAmean, __dataBmean, __dataAsd, __dataBsd = [0], [0], [0], [0], [0], [0], [0]
    __labels = ['0:0']
    __ln1, = __ax1.plot([0], [0], 'red', linewidth = 1 )
    __ln2, = __ax1.plot([0], [0], 'green', linewidth = 1 )
    __ln3, = __ax2.plot([0], [0], 'red', linewidth = 1 )
    __ln4, = __ax2.plot([0], [0], 'blue', linestyle = '--', linewidth = 1)
    __ln5, = __ax3.plot([0], [0], 'green', linewidth = 1 )
    __ln6, = __ax3.plot([0], [0], 'blue', linestyle = '--', linewidth = 1)
    __ln7, = __ax4.plot([0], [0], 'red', linewidth = 1 )
    __ln8, = __ax4.plot([0], [0], 'black', linestyle = '--', linewidth = 1)
    __ln9, = __ax5.plot([0], [0], 'green', linewidth = 1 )
    __ln10, = __ax5.plot([0], [0], 'black', linestyle = '--', linewidth = 1)
    
    __red_patch = patches.Patch(color='red', label='Data A')
    __green_patch = patches.Patch(color='green', label='Data B')
    __avg_patch = patches.Patch(color='blue', label='Avgerage')
    __sd_patch = patches.Patch(color='black', label='SD')
        
    __initTime = time.time()
    __threads = []
    
    __yLimits = 100

    def __init__(self):
        #Initilize the dataBase.csv file to Start writing
        if(os.path.isfile(os.path.dirname(__file__)+"/dataBaseA.csv")):
            self.__fetchDatabase()
            self.__dataA[0] = self.__dataALog.iloc[-1]['Data']
            self.__dataB[0] = self.__dataBLog.iloc[-1]['Data']
            
            self.__dataAmean[0] = self.__dataALog.iloc[-1]['Average']
            self.__dataBmean[0] = self.__dataBLog.iloc[-1]['Average']
            
            self.__dataAsd[0] = self.__dataALog.iloc[-1]['SD']
            self.__dataBsd[0] = self.__dataBLog.iloc[-1]['SD']
        else:
            self.__createCSV()
        return

    #Data function    
    def __getNewData(self, number, error):
        """
        Description:
        -------
        **__getNewData()** genreats a new random float. The genreated number(float) is in the range of *+/- (number*error)/100*. The gunction round-up upto *2 decimal digit* and gives a float output.
        """
        error = random.uniform(-error, error)
        if(number == 0):
            return random.randint(1, 100)
        return round((number+((number*error)/100)), 2)
    
    def __average(self, data, log, n):
        if(len(log) > n-1):
            dataList = list(log.iloc[-n:-1]['Data'])
            dataList.append(data)
            return round(np.mean(dataList, axis=0), 2)
        else:
            return 0
    
    def __sd(self, data, log, n):
        if(len(log) > n-1):
            dataList = list(log.iloc[-n:-1]['Data'])
            dataList.append(data)
            return round(np.std(dataList, axis=0),2)
        else:
            return 0
    
    
    def __Save(self, inputDataA, inputDataB):
        """
        Description
        --------
        **__Save()** save the input data into .CSV database
        """
        #os.system('cls')
        #print(pandas.concat([self.__dataALog, self.__dataBLog], axis=1))
        with open('dataBaseA.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar=' ', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(inputDataA)
        
        with open('dataBaseB.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar=' ', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(inputDataB)
    
    
    def __createCSV(self):
        """
        Description
        --------
        **__createCSV()** create two .CSV file dataBaseA.csv and dataBaseB.csv for data logging
        """
        with open('dataBaseA.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar=' ', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.__dataColumns)
            writer.writerow([''])
        with open('dataBaseB.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar=' ',lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.__dataColumns)
            writer.writerow([''])
    def __fetchDatabase(self):
        """
        Description
        --------
        **__fetchDatabase()** fetch the data in pandas.DataFrame format and save it to __dataALog and __dataBLog
        """
        self.__dataALog = pandas.read_csv(os.path.dirname(__file__)+"/dataBaseA.csv")
        self.__dataBLog = pandas.read_csv(os.path.dirname(__file__)+"/dataBaseB.csv")

    def __init(self):
        self.__ax1.set_title('Data A vs Data B')
        self.__ax2.set_title('Data A vs Average A')
        self.__ax3.set_title('Data B vs Average B')
        self.__ax4.set_title('Data A vs SD A')
        self.__ax5.set_title('Data B vs SD B')
        
        self.__setAxisLimits(self.__ax1)
        self.__setAxisLimits(self.__ax2)
        self.__setAxisLimits(self.__ax3)
        self.__setAxisLimits(self.__ax4)
        self.__setAxisLimits(self.__ax5)
        
        self.__ax1.legend(handles=[self.__red_patch, self.__green_patch])
        self.__ax2.legend(handles=[self.__red_patch, self.__avg_patch])
        self.__ax3.legend(handles=[self.__green_patch, self.__avg_patch])
        self.__ax4.legend(handles=[self.__red_patch, self.__sd_patch])
        self.__ax5.legend(handles=[self.__green_patch, self.__sd_patch])
        return
    
    def __graph(self, frame):
        #Time Sync.
        dateTime = time.time()
        time.sleep(1 - (dateTime-self.__initTime - int(dateTime-self.__initTime)))
        #Inputs
        inputDataA = self.__getNewData(self.__dataA[-1], 5)
        inputDataB = self.__getNewData(self.__dataB[-1], 10)
        dateTime = time.time() #Timestamp
        dateTimeNow = str(datetime.datetime.fromtimestamp(dateTime).strftime('%H:%M:%S ')) # Time in Calander format
        timeWhole = int(dateTime-self.__initTime)
        #change Y-axis
        if(inputDataA >= self.__yLimits or inputDataB >= self.__yLimits):
            self.__yLimits = inputDataA+5 if (inputDataA > inputDataB) else inputDataB+5
            self.__ax1.set_ylim(0, self.__yLimits)
            self.__ax2.set_ylim(0, self.__yLimits)
            self.__ax3.set_ylim(0, self.__yLimits)
            self.__ax4.set_ylim(0, self.__yLimits)
            self.__ax5.set_ylim(0, self.__yLimits)
        #Change X-axis
        if timeWhole > 11:
            self.__labels.pop(0)
            self.__xdata.pop(0)
            self.__dataA.pop(0)
            self.__dataB.pop(0)
            self.__dataAmean.pop(0)
            self.__dataBmean.pop(0)
            self.__dataAsd.pop(0)
            self.__dataBsd.pop(0)
            self.__ax1.set_xlim(timeWhole-10, timeWhole)
            self.__ax2.set_xlim(timeWhole-10, timeWhole)
            self.__ax3.set_xlim(timeWhole-10, timeWhole)
            self.__ax4.set_xlim(timeWhole-10, timeWhole)
            self.__ax5.set_xlim(timeWhole-10, timeWhole)

        self.__dataALog = self.__dataALog.append({'Time':dateTimeNow,'Data':round(inputDataA,2),'Average':self.__average(inputDataA, self.__dataALog, 10),'SD':self.__sd(inputDataA, self.__dataALog, 10)}, ignore_index=True)
        self.__dataBLog = self.__dataBLog.append({'Time':dateTimeNow,'Data':inputDataB,'Average':self.__average(inputDataB, self.__dataBLog, 10),'SD':self.__sd(inputDataB, self.__dataBLog, 10)}, ignore_index=True)
        self.__ax6.clear()
        self.__ax6.text(0.1, 0, '$Status$ \nTime    : '+dateTimeNow+' \nData A : '+str(inputDataA)+' \nData B : '+str(inputDataB)+' \nAvg A  : '+str(self.__dataALog.iloc[-1]['Average'])+' \nAvg B  : '+str(self.__dataBLog.iloc[-1]['Average'])+' \nSD A    : '+str(self.__dataALog.iloc[-1]['SD'])+' \nSD B    : '+str(self.__dataBLog.iloc[-1]['SD'])+' ', fontsize=10)
        plt.axis('off')

        self.__xdata.append(timeWhole)
        self.__dataA.append(inputDataA)
        self.__dataB.append(inputDataB)
        self.__dataAmean.append(self.__dataALog.iloc[-1]['Average'])
        self.__dataBmean.append(self.__dataBLog.iloc[-1]['Average'])
        self.__dataAsd.append(self.__dataALog.iloc[-1]['SD'])
        self.__dataBsd.append(self.__dataBLog.iloc[-1]['SD'])
        self.__labels.append(dateTimeNow)

        plt.setp(self.__ax1, xticks=self.__xdata, xticklabels=self.__labels)
        plt.setp(self.__ax2, xticks=self.__xdata, xticklabels=self.__labels)
        plt.setp(self.__ax3, xticks=self.__xdata, xticklabels=self.__labels)
        plt.setp(self.__ax4, xticks=self.__xdata, xticklabels=self.__labels)
        plt.setp(self.__ax5, xticks=self.__xdata, xticklabels=self.__labels)
        
        self.__ln1.set_data(self.__xdata, self.__dataA)
        self.__ln2.set_data(self.__xdata, self.__dataB)
        self.__ln3.set_data(self.__xdata, self.__dataA)
        self.__ln4.set_data(self.__xdata, self.__dataAmean)
        self.__ln5.set_data(self.__xdata, self.__dataB)
        self.__ln6.set_data(self.__xdata, self.__dataBmean)
        self.__ln7.set_data(self.__xdata, self.__dataA)
        self.__ln8.set_data(self.__xdata, self.__dataAsd)
        self.__ln9.set_data(self.__xdata, self.__dataB)
        self.__ln10.set_data(self.__xdata, self.__dataBsd)
        
        #Threaded Work
        t = threading.Thread(target=self.__Save, args=(list(self.__dataALog.iloc[-1]), list(self.__dataBLog.iloc[-1]),))
        self.__threads.append(t)
        t.start()
        
        return 
    
    def __setAxisLimits(self, ax):
        ax.set_xlim(0, 11)
        ax.set_ylim(0, self.__yLimits)
        self.__rotateLabel(ax)
    
    def __rotateLabel(self, ax):
        for label in ax.get_xmajorticklabels() + ax.get_xmajorticklabels():
            label.set_rotation(90)
            label.set_horizontalalignment("right")
    
    def genrateLineAnalysis(self):
        """
        Description
        -------
        **genrateLineAnalysis()** Genrate line __graph between two data and its Analysis in line __graph.
        
        Parameters
        ----------
        *self*
            
        Examples
        --------
        >>> p = pyAnalysis()
        >>> p.genrateLineAnalysis()
        """
        ani = animation.FuncAnimation(self.__fig, self.__graph, init_func=self.__init,
                                      interval=700, blit=False)
        plt.show()
