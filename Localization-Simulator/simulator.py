import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import numpy as np
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import tkinter as tk

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

#----------------------------------------------------- USER INPUT ------------------------------------------------------#
def get_data(A,B,C,D,E,transittionPower,noise,n):
    global start
    def fetch(entries,A,B,C,D,E,transittionPower,noise,n):
        for entry in entries:
            field = entry[0]
            text  = entry[1].get()
        root.destroy()
    def makeform(root, fields):
        entries = []
        for field in fields:
            row = tk.Frame(root)
            lab = tk.Label(row, width=15, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent))
        return entries
    def quit():
        root.destroy()
        exit()
    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Control-Q>', (lambda event, e=ents: fetch(e)))   

    b1 = tk.Button(root, text='Enter',command=(lambda e=ents: fetch(e,A,B,C,D,E,transittionPower,noise,n)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop() 
#-----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------- SIMULATION ------------------------------------------------------#
class Simulation:
    def initialize():
        global numbering
        try:
            os.mkdir("Statistics")
        except OSError:
            if not os.path.isdir("Statistics"):
                print ("Creation of the directory failed Statistics. Exit...")
                exit()
        path, dirs, files = next(os.walk(os.getcwd()+"/Statistics"))
        numbering = len(dirs)
        while os.path.isdir("Statistics/Experiment_"+str(numbering+1)):
            numbering = numbering + 1
        return "/Statistics/Experiment_"+str(numbering+1)

    def setup():
        now = datetime.now()
        global pathlog; global pathfig; global pathdata; global numbering
        expPath = "Experiment_"+str(numbering+1)
        pathToCheck =["Statistics/"+expPath,"Statistics/"+expPath+"/SUMMARY","Statistics/"+expPath+"/Statistics "+\
            str(now),"Statistics/"+expPath+"/Statistics "+str(now)+"/Logs","Statistics/"+expPath+"/Statistics "+\
            str(now)+"/Figures","Statistics/"+expPath+"/Statistics "+str(now)+"/Data"]
        for i in pathToCheck:   
            try:
                os.mkdir(i)
            except OSError:
                if not os.path.isdir(i):
                    print ("Creation of the directory %s failed. Exit..." % i)
                    exit()
        pathlog  = "Statistics/"+expPath+"/Statistics "+str(now)+"/Logs"
        pathfig  = "Statistics/"+expPath+"/Statistics "+str(now)+"/Figures"
        pathdata = "Statistics/"+expPath+"/Statistics "+str(now)+"/Data" 

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

    def simulationDataCreation(nodes,transittionPower,noise,xyz,distances,RSSIValues,TDOAValues,TOAValues):
        x, y, z = zip(*xyz)
        for i in range(0, len(x)):
            distances.append(Data.Distances_Data_Input(nodes,[x[i], y[i], z[i]]))
            RSSIValues.append(Data.RSSI_Data_Input(transittionPower,noise,nodes,[x[i],y[i],z[i]]))
            TDOAValues.append(Data.TODA_Data_Input(nodes,[x[i], y[i], z[i]]))
            TOAValues.append(Data.TOA_Data_Input(nodes,[x[i], y[i], z[i]]))
            
    def simulation(nodes,xyz,Values,transittionPower,noise):
        x, y, z = zip(*xyz[0])
        for i in range(0, len(x)):
            Algorithms.RSSI_Algorithm(nodes, Values[0][i],xyz[1],transittionPower,noise)
            Algorithms.TDOA_Algorithm(nodes,Values[2][i],xyz[2])
            Algorithms.TOA_Algorithm(nodes,Values[2][i],xyz[3])
        
    def storeDataFiles(nodes,transittionPower,noise,Values,traces,labels,metricSI):
        A=nodes[0];B=nodes[1];C=nodes[2];D=nodes[3]
        x, y, z = zip(*traces[0])
        dist = Data.tetrahedronContour(nodes)
        header = " A = " + str(A) + "\n B = " + str(B) + "\n C = " + str(C) + "\n D = " + str(C) + "\n\n"+\
                "-------------------------------------------------\n"+"        |    A    |    B    |    C    |    D    |\n"+\
                "|   A   |    -    |"+'{:>9}'.format(str(dist["AB"]))[:9]+"|"+'{:>9}'.format(str(dist["AC"]))[:9]+\
                "|"+'{:>9}'.format(str(dist["AD"]))[:9]+"|\n"+"|   B   |" + '{:>9}'.format(str(dist["AB"]))[:9] +\
                "|    -    |" + '{:>9}'.format(str(dist["BC"]))[:9]+"|"+'{:>9}'.format(str(dist["BD"]))[:9] + "|\n" +\
                "|   C   |" + '{:>9}'.format(str(dist["AC"]))[:9] + "|" + '{:>9}'.format(str(dist["BC"]))[:9] +\
                "|    -    |" + '{:>9}'.format(str(dist["CD"]))[:9] + "|\n"+"|   D   |" + '{:>9}'.format(str(dist["AD"]))[:9]+\
                "|" + '{:>9}'.format(str(dist["BD"]))[:9] + "|" + '{:>9}'.format(str(dist["CD"]))[:9] + "|    -    |\n\n"
        i_l = 0   
        for filelabel in labels:
            logs = "/"+filelabel +"Output.txt" 
            file = open(pathlog+logs, "w")    
            fileRaw = open(pathdata+"/"+filelabel+"_Raw_Data.txt", "w")
            if "RSSI" in logs:
                headerRssi = " A = " + str(A) + "\n B = " + str(B) + "\n C = " + str(C) + "\n D = " + str(C) + "\n\n"+\
                             "Transmition Power of A, B, C and D :" + str(transittionPower) + " dBm\n"+"White Noise coefficient            :" + str(noise) + "\n"+\
                             "Equation for RSSI calculation      :RSSI = A − 10 · n · log10 d\n\nNode E Trace Log: \n\n"
                file.write(headerRssi+"\n\n")
            file.write(header+"Node E "+labels[i_l]+" log:\n\n")
            for i in range(0, len(x)): 
                if "TDOA" in logs:
                    inputFile = "[ " + str(x[i]).ljust(10)[:15] + ", " + str(y[i]).ljust(10)[:15] + ", " +\
                            str(z[i]).ljust(10)[:15] + "] :\t\t Distances-> AB = " + \
                            str(Values[i_l][i]["R12"]).ljust(10)[:15] + metricSI[i_l]+", AC = " +\
                            str(Values[i_l][i]["R13"]).ljust(10)[:15] + metricSI[i_l]+", AD = " +\
                            str(Values[i_l][i]["R14"]).ljust(10)[:15] + metricSI[i_l]+", BC = " +\
                            str(Values[i_l][i]["R23"]).ljust(10)[:15] + metricSI[i_l]+", BD = " +\
                            str(Values[i_l][i]["R24"]).ljust(10)[:15] + metricSI[i_l]+", CD = " +\
                            str(Values[i_l][i]["R34"]).ljust(10)[:15] + metricSI[i_l]+"\n"
                            
                    inputFileRaw = str(Values[i_l][i]["R12"])+" "+str(Values[i_l][i]["R13"])+" "+\
                                   str(Values[i_l][i]["R13"])+" "+str(Values[i_l][i]["R14"])+" "+\
                                   str(Values[i_l][i]["R23"])+" "+str(Values[i_l][i]["R24"])+" "+\
                                   str(Values[i_l][i]["R34"])+"\n"
                    fileRaw.write(inputFileRaw)
                else: 
                    inputFile = "[ " + str(x[i]).ljust(10)[:15] + ", " + str(y[i]).ljust(10)[:15] + ", " +\
                            str(z[i]).ljust(10)[:15] + "] :\t\t Distances-> AE = " + \
                            str(Values[i_l][i][0]).ljust(10)[:15] + metricSI[i_l]+", BE = " +\
                            str(Values[i_l][i][1]).ljust(10)[:15] + metricSI[i_l]+", CE = " +\
                            str(Values[i_l][i][2]).ljust(10)[:15] + metricSI[i_l]+", DE = " +\
                            str(Values[i_l][i][3]).ljust(10)[:15] + metricSI[i_l]+"\n"
                    fileRaw.write(str(Values[i_l][i][0])+" "+str(Values[i_l][i][1])+" "+str(Values[i_l][i][2])+" "+str(Values[i_l
][i][3])+"\n")     
                file.write(inputFile)
            if "Trace" not in filelabel:
                filePerf = open(pathlog+"/"+str(labels[i_l])+"PerformanceOutput.txt", "w")
                headerPer = " A = " + str(A) + "\n B = " + str(B) + "\n C = " + str(C) + "\n D = " + str(C) + "\n\n"
                filePerf.write(headerPer+"Node E movement trace log:\n\n")
                x_, y_, z_ = zip(*traces[i_l])
                for i in range(0, len(x_)):
                    inputFile = "[ " + str(x[i]).ljust(10)[:15] + ", " + str(y[i]).ljust(10)[:15] + ", " + str(z[i]).ljust(10)[:15] +\
                                "] :\t\t "+str(labels[i_l])+" Value-> "+ str(x_[i]).ljust(10)[:15] + ", " + str(y_[i]).ljust(10)[:15] + ", " + str(z_[i]).ljust(10)[:15]+"\n"
                    filePerf.write(inputFile)
            i_l = i_l +1
                
    def plotGraphics(A,B,C,D,traces,label):
        global pathlog;
        #mpl.use('Agg')
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        color = 6;counter = 0;linewdth = 5
        for t in traces:
            x, y, z = zip(*t)
            ax.plot(x, y, z, "C"+str(color), label=label[counter], linewidth=linewdth)
            ax.scatter(x[0], y[0], z[0], "C"+str(color), label="Start " + label[counter])
            color = color + 1
            ax.scatter(x[-1], y[-1], z[-1], "C"+str(color), label="End   " + label[counter])
            color = color + 1;  counter = counter +1;  linewdth = linewdth - linewdth*0.40 
        v = np.array([A, B, C, C, D])
        ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
        verts = [[v[0], v[1], v[4]], [v[0], v[3], v[4]], [v[2], v[1], v[4]], [v[2], v[3], v[4]], [v[0], v[1], v[2], v[3]]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
        ax.scatter(x[-1], y[-1], z[-1], c='b', marker='o')
        ax.legend()
        plt.savefig(pathfig+"/TraceLog.png")
        plt.show()
        plt.clf() 

    def plotStatisticsGraphics(A,B,C,D,xyz,traces,labels):
        global pathfig;
        for num in range(0,len(labels)):
            if "Performance" in labels[num]:
                x, y, z = zip(*xyz)
                x_, y_, z_ = zip(*traces[num])
                diffx=[]; diffy=[]; diffz=[]
                for i in range(0,len(x)):
                    diffx.append(abs((x[i]-x_[i])))
                plt.plot((diffx),label="x axis")
                for i in range(0,len(y)):
                    diffy.append(abs((y[i]-y_[i])))
                plt.plot((diffy),label="y axis")
                for i in range(0,len(z)):
                    diffz.append(abs((z[i]-z_[i])))
                plt.plot((diffz),label="z axis")
                plt.ylabel(str(labels[num])+'RSSI x,y,z Difference from actual values')
            else:
                if "TDOA_Values" in labels[num]:
                    R12=[];R13=[];R14=[]
                    R23=[];R24=[];R34=[] 
                    for a in range(0,len(traces[num])):
                        R12.append(traces[num][a]["R12"])
                        R13.append(traces[num][a]["R13"])
                        R14.append(traces[num][a]["R14"])
                        R23.append(traces[num][a]["R23"])
                        R24.append(traces[num][a]["R24"])
                        R34.append(traces[num][a]["R34"])
                    plt.plot(R12,label="AB tdoa");plt.plot(R13,label="AC tdoa")
                    plt.plot(R14,label="AD tdoa");plt.plot(R23,label="BC tdoa")
                    plt.plot(R24,label="BD tdoa");plt.plot(R34,label="CD tdoa")
                else:
                    A, B, C, D = zip(*traces[num])
                    plt.plot(A,label="A Node");plt.plot(B,label="B Node")
                    plt.plot(C,label="C Node");plt.plot(D,label="D Node")
                    plt.ylabel(str(labels[num]))
                    
            plt.xlabel('Steps')
            plt.legend()
            plt.savefig(pathfig+"/"+labels[num]+".png")
            plt.close()

    def cleanup(xyz,xyzTDOA,xyzRSSI,xyzTOA,RSSIValues,TDOAValues,TOAValues,distances):   
        xyz.clear();xyzTDOA.clear();xyzRSSI.clear();xyzTOA.clear()
        RSSIValues.clear();TDOAValues.clear();TOAValues.clear();distances.clear()
#-----------------------------------------------------------------------------------------------------------------------#

