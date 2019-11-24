import os
import re
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

HOME = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', ''))

class Collector:
        
    def statisticsCollector(folder,algorithms):
        
        def before(value, a):
            pos_a = value.find(a)
            if pos_a == -1: return ""
            return value[0:pos_a]

        def plotStatistics(folder,Values,meanX,varianceS):
            summary = str(HOME)+folder+"/SUMMARY/"
            pathdir = str(HOME)+folder
            label = ["X","Y","Z"]
            for keys,values in Values.items():
                try:
                    os.mkdir(pathdir+"/SUMMARY/"+str(keys)+"/")
                except OSError:
                    exit(-1)
                xVar = []; xMean = []
                yVar = []; yMean = []
                zVar = []; zMean = []

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
                    ax.plot(Mean[axis], color='C2',label=str(label[axis])+" Mean Value", linewidth=2)
                    ax.set_ylabel('Statistics with S^2 = ' + str(varianceS[keys][axis]))
                    ax.legend()
                    plt.savefig(pathdir+"/SUMMARY/"+str(keys)+"/"+str(label[axis])+"_Error.png")
                    plt.close() 


        pathdir = str(HOME)+folder
        path, dirs, files = next(os.walk(pathdir))
        meanX = {}
        varianceS = {}  
        
        fileSummary = open(pathdir+"/SUMMARY/Info.txt", "w+")
        for d in dirs:
            if "Statistics" in str(d):
                path2, dirs2, files2 = next(os.walk(pathdir+"/"+str(d)+"/Logs"))
                Values = {}
                for f in files2:
                    inputVal = []
                    if "Performance" in f and "Traces" not in f:
                        fileP = open(pathdir+"/"+str(d)+"/Logs/"+f, "r")
                        for x in fileP:
                            if "TOA" in str(x) or "TDOA" in str(x) or "RSSI" in str(x):
                                out = re.findall(r'\d+\.\d+|\d+',x) 
                                inputVal.append([abs(float(out[0])-float(out[3])),abs(float(out[1])-float(out[4])),abs(float(out[2])-float(out[5]))])
                        Values.update({str(before(f,"_Performance")) : inputVal})
             
        for keys,var in Values.items():  
            _x = 0;_x_ = 0
            _y = 0;_y_ = 0
            _z = 0;_z_ = 0
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
            fileInput = fileInput + str(keys) + "Performance:\n    Average Error :\n      E[X] = "+str(meanX[keys][0])+", E[Y] = "+str(meanX[keys][1])+", E[Z] = "+str(meanX[keys][2])+"\n\n"
        for keys,values in varianceS.items():
            fileInput = fileInput + str(keys) + "Performance:\n    Variance Error:\n      V[X] = "+str(varianceS[keys][0])+", V[Y] = "+str(varianceS[keys][1])+", V[Z] = "+str(varianceS[keys][2])+"\n"

        fileSummary.write(fileInput)
        plotStatistics(folder,Values,meanX,varianceS)
