# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 11:05:45 2017

@author: Prashant Kumar

@mail: kr.prashant94@gmail.com

@supervision: Dr. Dilip Kumar

"""
import matplotlib.pyplot as plt
import csv
import time
import datetime
import random
import numpy as np
import matplotlib.animation as animation
import pandas
import os
#end of import

class BoxAnalysis:
    """
    Description
    -------
    **pyAnalysis** class provides the functionality for generating real time __graph form continuous input.
    """
 
    __fig = plt.figure()
    __ax1 = __fig.add_subplot(2,2,1)
    __ax2 = __fig.add_subplot(2,2,2)
    __dateTime = 0
    __initTime = 0
    __timeISO = 0
    __column = ['Time','Data','Average','SD']
    __dataALog = 0
    __dataBLog = 0
    __ploatdataA = []
    __ploatdataB = []
    __ploatDelay = 0
    __labels = [0,0,0,0,0,0,0,0,0,0]
    __counter = 0
    __tmpgetA, __tmpgetB = [],[]
    __hover_ax = 0
    __hover_xy = [0,0]

    def __init__(self, __ploatDelay):
        self.__initTime = time.time()
        self.__ploatDelay = __ploatDelay
        self.__dataALog = pandas.DataFrame(columns = self.__column)
        self.__dataBLog = pandas.DataFrame(columns = self.__column)
        self.__dataALog = self.__openDatabase('dataBaseA.csv')
        self.__dataBLog = self.__openDatabase('dataBaseB.csv')
        
    
    def getNewData(self, number, error):
        """
        Description
        -------
        **getNewData()** genreats a new random float. The genreated number(float) is in the range of *+/- (number*error)/100*.
        The gunction round-up upto *2 decimal digit* and gives a float output.
        """
    
        if(number == 0):
            return random.randint(1, 100)
        error = random.uniform(-error, 1.2*error)
        return round((number+((number*error)/100)), 2)

#    Database function
    def __openDatabase(self, dataBase):
        """
        Description
        -------
        **__openDatabase()** try to open .csv database file. and return the pandas dataframe variable of the .csv file. If the function fails to open the database file __openDatabase() try to create a new file.
        """
        if(os.path.isfile(os.path.dirname(__file__)+"/"+dataBase)):
            dataLog = pandas.read_csv(os.path.dirname(__file__)+"/"+dataBase)
            return dataLog
        else:
            with open(dataBase, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar=' ', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(self.__column)
                writer.writerow([''])
            
            tmp = pandas.DataFrame(columns = self.__column)
            return tmp.append({'Time':0,'Data':0,'Average':0,'SD':0}, ignore_index=True)
        
    def __saveDatabase(self, __dateTime, inputData, dataLog, n, dataBase):
        """
        Description
        -------
        **__saveDatabase()** append one row in .csv database and log variable and return the log variable.
        """
        dataLog = dataLog.append({'Time':__dateTime,'Data':inputData,'Average':self.__average(inputData, dataLog, n),'SD':self.__sd(inputData, dataLog, n)}, ignore_index=True)
        with open(dataBase, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar=' ', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(dataLog.iloc[-1])
        return dataLog
    
    def __readCSV(self, dataBase, elementInSet, totalSet):
        """
        Description
        -------
        **__readCSV()** read the CSV database file and return only required number of data which is important for plotting box __graph.
        """
        ploat = []
        data = pandas.read_csv(os.path.dirname(__file__)+"/"+dataBase)
        i_lim = int(totalSet)
        n = 1
        if(data['Data'].count() < int(elementInSet)):
            return [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        
        elif(data['Data'].count() < int(elementInSet)*int(totalSet)):
            i_lim = (data['Data'].count() / int(elementInSet))
        for i in range(1, int(i_lim)+1):
            tmp = []
            for j in range(1, elementInSet+1):
                tmp.append(data.iloc[-n]['Data'])
                n+=1;
            ploat.append(tmp)
            if(len(self.__labels) > 10):
                self.__labels.pop(0)
            self.__labels.append("-"+str(int(elementInSet)*(i_lim-i+1))+" sec.")
        return ploat


#     Math function
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

#Misc
    def __timeSync(self):
        tmpTime = time.time()
        timeSince = tmpTime - self.__initTime
        time.sleep(1 - (timeSince - int(timeSince)))
        self.__dateTime = time.time()
        self.__timeISO = str(datetime.datetime.fromtimestamp(self.__dateTime).strftime('%d-%m-%Y %H:%M:%S'))

#    Graph Function
        
    def __rotateLabel(self, ax):     
        for label in ax.get_xmajorticklabels() + ax.get_xmajorticklabels():
            label.set_rotation(90)
            label.set_horizontalalignment("right")

    def __initGraph(self):
        self.__ploatdataA = self.__readCSV("dataBaseA.csv", self.__ploatDelay, 10)
        self.__ploatdataB = self.__readCSV("dataBaseB.csv", self.__ploatDelay, 10)
        
        self.__ploatdataA.append(self.__tmpgetA)
        self.__ploatdataB.append(self.__tmpgetB)
        self.__fig.canvas.mpl_connect("motion_notify_event", self.__hover)
        return

    def __hover(self, event):
        self.__hover_ax = 0;
        for curve in self.__ax1.get_lines():
            if curve.contains(event)[0]:
                self.__hover_ax = 1;
                xy = curve.get_xydata()
                self.__hover_xy = xy[0]
        for curve in self.__ax2.get_lines():
            if curve.contains(event)[0]:
                self.__hover_ax = 2;
                xy = curve.get_xydata()
                self.__hover_xy = xy[0]

    def __graph(self, frame):
        self.__timeSync()
        dataA = self.getNewData(int(self.__dataALog.iloc[-1]['Data']), 10)
        dataB = self.getNewData(int(self.__dataBLog.iloc[-1]['Data']), 20)
        self.__dataALog = self.__saveDatabase(self.__timeISO, dataA, self.__dataALog, 10, 'dataBaseA.csv')
        self.__dataBLog = self.__saveDatabase(self.__timeISO, dataB, self.__dataBLog, 10, 'dataBaseB.csv')
        
        if (dataA  < 50):
            print("Lower Limit [Data A]")
        elif(dataA > 100):
            print("Upper Limit [Data A]")

        if (dataB  < 50):
            print("Lower Limit [Data B]")
        elif(dataB > 100):
            print("Upper Limit [Data B]")   
         

        self.__tmpgetA.append(dataA)
        self.__tmpgetB.append(dataB)
        if(self.__counter == self.__ploatDelay-1): 
            self.__ploatdataA.pop(-1)
            self.__ploatdataB.pop(-1)
            self.__ploatdataA.append(self.__tmpgetA[:])
            if(len(self.__ploatdataA) >= 10):
                self.__ploatdataA.pop(0)
            self.__ploatdataB.append(self.__tmpgetB[:])
            if(len(self.__ploatdataB) >= 10):
                self.__ploatdataB.pop(0)
            if(len(self.__labels) >= 10):
                self.__labels.pop(0)
            self.__labels.append(self.__timeISO)

            self.__tmpgetA.clear()
            self.__tmpgetB.clear()
            self.__ploatdataA.append(self.__tmpgetA)
            self.__ploatdataB.append(self.__tmpgetB)
        
        self.__counter = (self.__counter+1)%(self.__ploatDelay)

        self.__ax1.clear()
        self.__ax2.clear()
        self.__ax1.set_title('Data A')
        self.__ax2.set_title('Data B')
        
        # adding horizontal grid lines
        self.__ax1.yaxis.grid(True)
        self.__ax2.yaxis.grid(True)
        
        try:
            if self.__hover_ax == 1 and self.__ploatdataA[int(self.__hover_xy[0])]:
                annot = self.__ax1.annotate("", xy =(0, self.__hover_xy[1]-self.__hover_xy[1]*0.5), bbox=dict(boxstyle="round", fc="w"))
                annot.set_text("Mean : "+str(np.mean(self.__ploatdataA[int(self.__hover_xy[0])]))+ "\nSD : "+str(np.std(self.__ploatdataA[int(self.__hover_xy[0])]))+ "\nMax : "+str(np.max(self.__ploatdataA[int(self.__hover_xy[0])]))+ "\nMin : "+str(np.min(self.__ploatdataA[int(self.__hover_xy[0])])))
                annot.get_bbox_patch().set_facecolor("coral")
                annot.get_bbox_patch().set_alpha(0.8)
                annot.set_visible(True)
            elif self.__hover_ax == 2 and self.__ploatdataA[int(self.__hover_xy[0])]:
                annot = self.__ax2.annotate("", xy =(0, self.__hover_xy[1]-self.__hover_xy[1]*0.5), bbox=dict(boxstyle="round", fc="w"))
                annot.set_text("Mean : "+str(np.mean(self.__ploatdataA[int(self.__hover_xy[0])]))+ "\nSD : "+str(np.std(self.__ploatdataA[int(self.__hover_xy[0])]))+ "\nMax : "+str(np.max(self.__ploatdataA[int(self.__hover_xy[0])]))+ "\nMin : "+str(np.min(self.__ploatdataA[int(self.__hover_xy[0])])))
                annot.get_bbox_patch().set_facecolor("coral")
                annot.get_bbox_patch().set_alpha(0.8)
                annot.set_visible(True)
                
            
        except:
            print("Error...");
            
        self.__ax1.boxplot(self.__ploatdataA, 0, 'rs',patch_artist=True)
        self.__ax2.boxplot(self.__ploatdataB, 0, 'rs',patch_artist=True)

        plt.setp(self.__ax1, xticks=[0,1,2,3,4,5,6,7,8,9,10,11], xticklabels=self.__labels+[self.__timeISO])
        plt.setp(self.__ax2, xticks=[0,1,2,3,4,5,6,7,8,9,10,11], xticklabels=self.__labels+[self.__timeISO])

        self.__rotateLabel(self.__ax1)
        self.__rotateLabel(self.__ax2)     
        
        return
    
    def genrateBoxAnalysis(self):
        """
        Description
        -------
        **genrateBoxAnalysis()** generate box graph. using FuncAnimation().
        Need to import matplotlib.animation as animation.

        Parameters
        ----------
        __ploatDelay *int*
            Time delay form ploting graph.
        
        Return
        -------
        *void*
        
        Examples
        --------
        >>> box_plot.genrateGraph()
        """
        ani = animation.FuncAnimation(self.__fig, self.__graph, init_func=self.__initGraph, interval=500, blit=False)
        plt.show()
