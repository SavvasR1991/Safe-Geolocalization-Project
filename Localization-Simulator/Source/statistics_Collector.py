import os
import re
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

HOME = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', ''))

class Collector:     
    def statisticsCollector(folder,algorithms,dirTotalTime):
        def before(value, a):
            pos_a = value.find(a)
            if pos_a == -1: return ""
            return value[0:pos_a]
            
        def plotStatistics2(folder,Values,meanX,varianceS,Values3):
            pathdir = str(HOME)+folder
            for keys,values in Values.items():
                try:
                    os.mkdir(pathdir+"/SUMMARY/Time_Performance/"+str(keys).replace("_Raw_Data","")+"_Time/")
                except OSError:
                    exit(-1)
                xVar = []; xMean = []; xMean2 = [];counter = 0;count =[]
                for var in values:
                    xMean.append(meanX[keys])
                    counter = counter + var+Values3['Communication']
                    xMean2.append(var+Values3['Communication'])
                    xVar.append(var)   
                for var in values:
                    count.append(counter/len(values))
                fig = plt.figure()
                fig.suptitle(str(keys).replace("_Raw_Data","")+" Execution Time Summary")
                ax = fig.gca()
                ax.plot(xVar, '.', color='C1',label="", linewidth=0.05)
                ax.plot(xMean, color='C2',label=" Mean Value = "+str(meanX[keys])+"\n S^2 = " + str(varianceS[keys]), linewidth=2)
                ax.set_ylabel("Milli seconds")
                ax.set_xlabel('Steps')
                ax.legend()
                plt.savefig(pathdir+"/SUMMARY/Time_Performance/"+(str(keys)).replace("_Raw_Data","")+"_Time/"+str(keys).replace("_Raw_Data","")+"_Execution_time.png")
                plt.close() 

                fig1 = plt.figure()
                fig1.suptitle(str(keys).replace("_Raw_Data","")+" Time Summary")
                ax1 = fig1.gca()
                ax1.plot(xMean2, color='C2',label=" Total Time: Communication + Execution Time ", linewidth=2)
                ax1.plot(count, color='C3',label=" Mean Total Time "+str(counter/len(values)), linewidth=2)
                ax1.set_ylabel("Milli seconds")
                ax1.set_xlabel('Steps')
                ax1.legend()
                plt.savefig(pathdir+"/SUMMARY/Time_Performance/"+str(keys).replace("_Raw_Data","")+"_Time/"+str(keys).replace("_Raw_Data","")+"_Total_time.png")
                plt.close()
            comm = [] 
            for keys,values in Values.items():
                for v in values:
                    comm.append(Values3["Communication"])
                break
            fig = plt.figure()
            ax = fig.gca()
            fig.suptitle("Communication Time Summary")
            ax.plot(comm, color='C2',label="Mean Communication Time = "+str(Values3["Communication"]), linewidth=2)
            ax.set_ylabel('Milli seconds')
            ax.set_xlabel('Steps')
            ax.legend()
            plt.savefig(pathdir+"/SUMMARY/Time_Performance/Communication_time.png")
            plt.close() 

        def plotStatistics(folder,Values,meanX,varianceS):
            pathdir = str(HOME)+folder
            label = ["X","Y","Z"]
            for keys,values in Values.items():
                try:
                    os.mkdir(pathdir+"/SUMMARY/Performance/"+str(keys)+"/")
                except OSError:
                    exit(-1)
                xVar = []; xMean = [];yVar = []; yMean = [];zVar = []; zMean = []
                for var in values:
                    xMean.append(meanX[keys][0])
                    xVar.append(var[0])   
                    yMean.append(meanX[keys][1])
                    yVar.append(var[1])   
                    zMean.append(meanX[keys][2])
                    zVar.append(var[2]) 
                Mean = [xMean,yMean,zMean]
                Var = [xVar,yVar,zVar]
                for axis in range(0,3):
                    fig = plt.figure()
                    ax = fig.gca()
                    ax.plot(Var[axis], '.', color='C1',label=str(label[axis])+"-Error", linewidth=0.05)
                    ax.plot(Mean[axis], color='C2',label=str(label[axis])+" Mean Value = "+str(Mean[axis][0]) + "\n S^2 = " + str(varianceS[keys][axis]), linewidth=2)
                    ax.set_ylabel("Meters")
                    ax.set_xlabel('Steps')
                    ax.legend()
                    plt.savefig(pathdir+"/SUMMARY/Performance/"+str(keys)+"/"+str(label[axis])+"_Error.png")
                    plt.close() 

        pathdir = str(HOME)+folder
        path, dirs, files = next(os.walk(pathdir))
        varianceS = {};meanX ={};Values = {};Values2 = {};Values3 = {}
        try:
            os.mkdir(pathdir+"/SUMMARY/Performance/")
        except OSError:
            exit(-1)
        try:
            os.mkdir(pathdir+"/SUMMARY/Time_Performance/")
        except OSError:
            exit(-1)
        fileSummary = open(pathdir+"/SUMMARY/Info.txt", "w+")
        for d in dirs:
            if "Statistics" in str(d):
                path2, dirs2, files2 = next(os.walk(pathdir+"/"+str(d)+"/Logs"))
                for f in files2:
                    if "Performance" in f and "Traces" not in f:
                        Values.update({str(before(f,"_Performance")) : []})
                break
        for d in dirs:
            if "Statistics" in str(d):
                path2, dirs2, files2 = next(os.walk(pathdir+"/"+str(d)+"/Data"))
                for f in files2:
                    if "Time" in f and "Communication" not in f:
                        Values2.update({str(before(f,"_Time")) : []})
                    if "Communication" in f:   
                        Values3.update({str(before(f,"_Time")) : 0})
                break
                
        for d in dirs:
            if "Statistics" in str(d):
                path2, dirs2, files2 = next(os.walk(pathdir+"/"+str(d)+"/Logs"))
                path3, dirs3, files3 = next(os.walk(pathdir+"/"+str(d)+"/Data"))
                for f in files2:
                    if "Performance" in f and "Traces" not in f:
                        fileP = open(pathdir+"/"+str(d)+"/Logs/"+f, "r")
                        for x in fileP:
                            if "TOA" in str(x) or "TDOA" in str(x) or "RSSI" in str(x):
                                out = re.findall(r'\d+\.\d+|\d+',x) 
                                Values[str(before(f,"_Performance"))].append([abs(float(out[0])-float(out[3])),abs(float(out[1])-float(out[4])),abs(float(out[2])-float(out[5]))])
                                
                for f in files3:
                    if "Time" in f and "Communication" not in f:
                        fileP = open(pathdir+"/"+str(d)+"/Data/"+f, "r")
                        for x in fileP:
                            Values2[str(before(f,"_Time"))].append(1000*float(x))
                    if "Communication" in f:
                        fileP = open(pathdir+"/"+str(d)+"/Data/"+f, "r")
                        for x in fileP:
                            Values3[str(before(f,"_Time"))] = (float(x))*1000
        for keys,var in Values.items():  
            _x = 0;_x_ = 0;_y = 0;_y_ = 0;_z = 0;_z_ = 0
            for i in var:
                _x = _x + i[0]
                _y = _y + i[1]
                _z = _z + i[2]
            _x = _x/len(var)
            _y = _y/len(var)
            _z = _z/len(var)
            for k in var:
                _x_ = _x_ + (k[0] - _x)**2
                _y_ = _y_ + (k[1] - _y)**2
                _z_ = _z_ + (k[2] - _z)**2
            _x_ = _x_ /len(var)
            _y_ = _y_ /len(var)
            _z_ = _z_ /len(var)
            meanX.update({keys:[_x,_y,_z]})  
            varianceS.update({keys:[_x_,_y_,_z_]}) 
        fileInput = ""
        for keys,values in meanX.items():
            fileInput = fileInput + str(keys) + " Performance:\n    Average Error :\n      E[X] = "+str(meanX[keys][0])+", E[Y] = "+str(meanX[keys][1])+", E[Z] = "+str(meanX[keys][2])+"\n\n"
        for keys,values in varianceS.items():
            fileInput = fileInput + str(keys) + " Performance:\n    Variance Error:\n      V[X] = "+str(varianceS[keys][0])+", V[Y] = "+str(varianceS[keys][1])+", V[Z] = "+str(varianceS[keys][2])+"\n"
        fileSummary.write(fileInput)
        plotStatistics(folder,Values,meanX,varianceS)
        
        varianceS = {};meanX = {}
        for keys,var in Values2.items():  
            _x = 0;_x_ = 0;
            for i in var:
                _x = _x + i
            _x = _x/len(var)
            for k in var:
                _x_ = _x_ + (k - _x)**2
            _x_ = _x_ /len(var)
            f=_x_
            meanX.update({keys:_x})  
            varianceS.update({keys:_x_}) 
            fileSummary.write("\n"+str(keys)+" Total Execution Time:\n"+str((_x_ + f)/2))
        fileSummary.close()
        plotStatistics2(folder,Values2,meanX,varianceS,Values3)
