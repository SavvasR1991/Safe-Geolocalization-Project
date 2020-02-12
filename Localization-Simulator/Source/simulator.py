import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import numpy as np
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import tkinter as tk
import subprocess


from math_Tools import *
from data_Creator import *
from algorithm_Localization import *

from numpy.linalg import norm
from numpy import sqrt, dot, cross
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from urllib3.connectionpool import xrange
from scipy.constants import c as speed_of_light
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

pathlog = "";pathfig = "";pathdata = ""
fields = 'A Coordinates', 'B Coordinates', 'C Coordinates', 'D Coordinates', 'E Start Point','Transmition Power','Noise Ratio','Steps','Show plots',"Num of Exp."
numbering = 0
HOME = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', ''))

#----------------------------------------------------- SIMULATION ------------------------------------------------------#
class Simulation:
    def initialize():
        global numbering
        try:
            os.mkdir(str(HOME)+"/Statistics")
        except OSError:
            if not os.path.isdir(str(HOME)+"/Statistics"):
                print ("Creation of the directory failed Statistics. Exit...")
                exit(-1)
        path, dirs, files = next(os.walk(str(HOME)+"/Statistics"))
        numbering = len(dirs)
        while os.path.isdir(str(HOME)+"/Statistics/Experiment_"+str(numbering+1)):
            numbering = numbering + 1
        return "/Statistics/Experiment_"+str(numbering+1)

    def setup():
        now = datetime.now()
        global pathlog; global pathfig; global pathdata; global numbering
        expPath = "Experiment_"+str(numbering+1)
        pathToCheck =[str(HOME)+"/Statistics/"+expPath,str(HOME)+"/Statistics/"+expPath+"/SUMMARY",str(HOME)+"/Statistics/"+expPath+"/Statistics "+\
            str(now),str(HOME)+"/Statistics/"+expPath+"/Statistics "+str(now)+"/Logs",str(HOME)+"/Statistics/"+expPath+"/Statistics "+\
            str(now)+"/Figures",str(HOME)+"/Statistics/"+expPath+"/Statistics "+str(now)+"/Data"]
        for i in pathToCheck:   
            try:
                os.mkdir(i)
            except OSError:
                if not os.path.isdir(i):
                    print ("Creation of the directory %s failed. Exit..." % i)
                    exit(-1)
        pathlog  = str(HOME)+"/Statistics/"+expPath+"/Statistics "+str(now)+"/Logs"
        pathfig  = str(HOME)+"/Statistics/"+expPath+"/Statistics "+str(now)+"/Figures"
        pathdata = str(HOME)+"/Statistics/"+expPath+"/Statistics "+str(now)+"/Data" 

    def brownian_motion_simulation(xyz,cur,m,n,d,t):
        dt = t / float(n - 1)
        for j in range(1, n):
            s = np.sqrt(2.0 * m * d * dt) * np.random.randn(1)
            dx = np.random.randn(m)
            norm_dx = np.sqrt(np.sum(dx ** 2))
            for i in range(0, m):
                dx[i] = s * dx[i] / norm_dx
            cur[0] += dx[0]; cur[1] += dx[1]
            if cur[2] + dx[2] > 0:
                cur[2] += dx[2]
            else:
                cur[2] += abs(dx[2])
            p = np.array(cur[:])
            xyz.append(cur[:])

    def simulationDataCreation(nodes,transittionPower,noise,xyz,distances,calculatedValues,algorithms,dirTotalTime):
        x, y, z = zip(*xyz)
        RSSIValues =[]; TDOAValues =[]; TOAValues = []
        for i in range(0, len(x)):
            distances.append(Data.Distances_Data_Input(nodes,[x[i], y[i], z[i]]))
            if "RSSI" in algorithms:
                RSSIValues.append(Data.RSSI_Data_Input(transittionPower,noise,nodes,[x[i],y[i],z[i]]))
            if "TDOA" in algorithms:
                TDOAValues.append(Data.TODA_Data_Input(nodes,[x[i], y[i], z[i]]))
            if "TOA" in algorithms:
                TOAValues.append(Data.TOA_Data_Input(nodes,[x[i], y[i], z[i]]))
            if "TDOA" not in algorithms and "RSSI" not in algorithms and "TOA" not in algorithms:
                exit(-1)
        if RSSIValues: 
            calculatedValues.update({"RSSI": RSSIValues})
        if TDOAValues:
            calculatedValues.update({"TDOA": TDOAValues})
        if TOAValues:
            calculatedValues.update({"TOA": TOAValues})
        rc = subprocess.call("./BS_Communication/run "+str(len(nodes)-1)+" "+str(len(xyz)),shell=True)
        with open(os.getcwd()+"/BS_Communication/Total_Time.txt") as fp:
            line = fp.readline()
            dirTotalTime.update({"Communication_Time" : line})
            
    def simulation(nodes,xyz,calculatedTraces,calculatedValues,transittionPower,noise,pickForCalc,algorithms,dirTotalTime):
        Algorithms.Run_Selected_Algorithms(nodes,calculatedTraces, calculatedValues,xyz,transittionPower,noise,pickForCalc,algorithms,dirTotalTime)

    def storeDataFiles(nodes,transittionPower,noise,distances,Values,traces,calculatedTraces,metric_SI,dirTotalTime):
        x, y, z = zip(*traces)
        dist = Data.tetrahedronContour(nodes)
        header = ""; headerRssi=""; txt = "-----------"; txt2 = "";metricSI ="";fileRaw=[]
        for tmp in range(0,len(nodes)):
            txt = txt + "----------" 
        txt = txt + "\n          |"
        for keys,values in nodes.items():
            header  = header + " " + str(keys)+ " = " + str(values)+ "\n"
            txt = txt + "    "+str(keys)+"    |"
            txt2 = txt2 +  "|    "+str(keys)+"    |"
            for keys2,values2 in nodes.items():
                if keys == keys2:
                    txt2 = txt2 + "    -    |"
                else:
                    inputNode = []
                    inputNode.append(str(keys))
                    inputNode.append(str(keys2))
                    inputNode = sorted(inputNode)
                    txt2 = txt2 +'{:>9}'.format(str(dist[str(inputNode[0])+str(inputNode[1])]))[:9]+"|"
            txt2 = txt2 + "\n"
        header = header + "\n\n" + txt + "\n" + txt2 + "\n\n"
        headerRssi = header+ "\n\n"+\
                 "Transmition Power of nodes         :" + str(transittionPower) + " dBm\n"+"White Noise coefficient            :" + str(noise) + "\n"+\
                 "Equation for calculation           : Received signal strength A − 10 · n · log10 d\n\n"
        for keys, values in calculatedTraces.items():
            if keys in "Traces":
                inputFileRaw = 0
                fileRaw = open(pathdata+"/"+str(keys)+"_Raw_Data.txt", "w")
            logs = "/"+str(keys) +"_Performance"
            filePerf = open(pathlog+logs+"_Output.txt", "w")    

            if "RSSI" in logs:
                final_header = headerRssi+"\n\n"
            else:
                final_header = header
            filePerf.write(final_header)
            for i in range(0, len(x)): 
                inputFile = ""
                if "RSSI" in keys:
                    metricSI= metric_SI["RSSI"]
                elif "TDOA" in keys or "TOA" in keys:
                    metricSI= metric_SI["TIME"]
                else:
                    metricSI= metric_SI["DISTANCES"]
                if keys in "Traces":
                    inputFile = "[ " + str(x[i]).ljust(10)[:15] + ", " + str(y[i]).ljust(10)[:15] + ", " + str(z[i]).ljust(10)[:15] + "] \n"
                    inputFileRaw =  str(x[i]) + " " + str(y[i]) + " " + str(z[i]) + " \n"
                else:
                    inputFile = "[ " + str(x[i]).ljust(10)[:15] + ", " + str(y[i]).ljust(10)[:15] + ", " + str(z[i]).ljust(10)[:15] + "] :\t\t "+str(keys)+"-> "
                    inputFile = inputFile  + str(values[i][0]).ljust(10)[:22]+" "+ str(values[i][1]).ljust(10)[:22]+" "+ str(values[i][2]).ljust(10)[:22]+"\n" 
                filePerf.write(inputFile)
                if keys in "Traces":
                    fileRaw.write(inputFileRaw)
        for keys2,values2 in Values.items():
            fileRaw = open(pathdata+"/"+str(keys2)+"_Raw_Data.txt", "w")
            file = open(pathlog+"/"+str(keys2) +"_Output.txt", "w")    
            inputFileRaw = ""
            inputFile = ""
            i = 0
            if "RSSI" in keys2:
                metricSI = metric_SI["RSSI"]
                final_header = headerRssi+"\n\n"
            elif "TDOA" in keys2 or "TOA" in keys2:
                metricSI = metric_SI["TIME"]
                final_header = header
            else:
                metricSI = metric_SI["DISTANCES"]
                final_header = header
            file.write(final_header)

            for val in values2:
                inputFile = inputFile +"[ " + str(x[i]).ljust(10)[:15] + ", " + str(y[i]).ljust(10)[:15] + ", " + str(z[i]).ljust(10)[:15] + "] :\t\t "+str(keys2)+"-> "
                for keys3,values3 in val.items():
                    inputFileRaw = inputFileRaw + str(values3)+" "
                    inputFile = inputFile + str(keys3)+ " = " + str(values3).ljust(10)[:22] +", " 
                inputFileRaw = inputFileRaw + "\n"
                inputFile = inputFile + metricSI+" \n"
                i = i + 1
            fileRaw.write(inputFileRaw)
            file.write(inputFile)
        file.close()
        fileRaw.close()
        filePerf.close()
        

        for keys2,values2 in dirTotalTime.items():
            fileRawTime = open(pathdata+"/"+str(keys2)+"_Raw_Data_Time.txt", "w")
            if "Communication" not in str(keys2):
                for var in values2:
                    fileRawTime.write(str(var)+"\n")
            else:
                fileRawTime.write(str(values2)+"\n")
        fileRawTime.close()        
        
    def plotGraphics(nodes,calculatedTraces,plot):
        global pathlog;
        if "No" in plot:
            mpl.use('Agg')
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        color = 6;counter = 0;linewdth = 5
        for key,t in calculatedTraces.items():
            x, y, z = zip(*t)
            if "TDOA" in key:
                ax.plot(x, y, z, "C"+str(color), label=str(key), linewidth=linewdth)
            else:
                ax.plot(x, y, z, "C"+str(color), label=str(key), linewidth=linewdth)
            ax.scatter(x[0], y[0], z[0], "C"+str(color), label="Start " + str(key))
            color = color + 1
            ax.scatter(x[-1], y[-1], z[-1], "C"+str(color), label="End   " + str(key))
            color = color + 1;  counter = counter +1;  linewdth = linewdth - linewdth*0.40 
        for key,value in nodes.items():
            ax.text(value[0],value[1],value[2], str(key)) 
        if len(nodes) == 5:
            v = np.array([nodes["A"], nodes["B"], nodes["C"], nodes["E"], nodes["D"]])	
        elif len(nodes) == 4:
            v = np.array([nodes["A"], nodes["B"], nodes["C"], nodes["C"], nodes["D"]])	
        else:
            exit(-1)
        ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])	
        verts = [[v[0], v[1], v[4]], [v[0], v[3], v[4]], [v[2], v[1], v[4]], [v[2], v[3], v[4]], [v[0], v[1], v[2], v[3]]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
        ax.scatter(x[-1], y[-1], z[-1], c='b', marker='o')
        ax.legend()
        plt.savefig(pathfig+"/TraceLog.png")
        plt.show(); plt.clf() 

    def plotStatisticsGraphics(nodes,calculatedTraces,calculatedValues,dirTotalTime):
        global pathfig;
        x, y, z = zip(*calculatedTraces["Traces"])
        for keys,values in calculatedTraces.items():
            if "Traces" not in keys:
                x_, y_, z_ = zip(*values)
                diffx=[]; diffy=[]; diffz=[]
                for i in range(0,len(x)):
                    diffx.append(abs((x[i]-x_[i])))
                    diffy.append(abs((y[i]-y_[i])))
                    diffz.append(abs((z[i]-z_[i])))
                plt.plot((diffx),label="x axis")
                plt.plot((diffy),label="y axis")
                plt.plot((diffz),label="z axis")
                plt.ylabel(str(keys)+' x,y,z Difference from actual values')
                plt.xlabel('Steps')
                plt.legend()
                plt.savefig(pathfig+"/"+str(keys)+"_Performance.png")
                plt.close()
        for keys,values in calculatedValues.items():
            tmp = [[] for i in range(len(values[0].keys()))]
            for vals in values:
                count = 0
                for keys2,values2 in vals.items():
                    tmp[count].append(values2)
                    count = count + 1
            count = 0
            for key,values in vals.items():
                plt.plot(tmp[count],label=str(key) ) 
                plt.ylabel(str(keys)+ " Values")
                count = count + 1
            plt.xlabel('Steps')
            plt.legend()
            plt.savefig(pathfig+"/"+str(keys)+"_Values.png")
            plt.close()
            
        for keys,values in dirTotalTime.items():
            plt.plot((values),label="Total time in secs")
            plt.ylabel(str(keys)+' Execution Time')
            plt.xlabel('Steps')
            plt.legend()
            plt.savefig(pathfig+"/"+str(keys)+"_TotalTime.png")
            plt.close()

    def cleanup(xyz,xyzTDOA,xyzRSSI,xyzTOA,RSSIValues,TDOAValues,TOAValues,distances):   
        xyz.clear();xyzTDOA.clear();xyzRSSI.clear();xyzTOA.clear()
        RSSIValues.clear();TDOAValues.clear();TOAValues.clear();distances.clear()
#-----------------------------------------------------------------------------------------------------------------------#

