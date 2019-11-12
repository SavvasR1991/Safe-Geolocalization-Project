import os
import re

class Collector:
    def statisticsCollector(folder):
        pathdir = os.getcwd()+folder
        path, dirs, files = next(os.walk(pathdir))
        rssi=[]
        tdoa=[]
        toa=[]
        fileSummary = open(pathdir+"/SUMMARY/Info.txt", "w+")
        for d in dirs:
            if "Statistics" in str(d):
                path2, dirs2, files2 = next(os.walk(pathdir+"/"+str(d)+"/Logs"))
                for f in files2:
                    if "Performance" in f:
                        fileP = open(pathdir+"/"+str(d)+"/Logs/"+f, "r")
                        for x in fileP:
                            if "RSSI" in str(x):
                                out = re.findall(r'\d+\.\d+|\d+',x)
                                rssi.append([abs(float(out[0])-float(out[3])),abs(float(out[1])-float(out[4])),abs(float(out[2])-float(out[5]))])
                            if "TDOA" in str(x):
                                out = re.findall(r'\d+\.\d+|\d+',x)
                                tdoa.append([abs(float(out[0])-float(out[3])),abs(float(out[1])-float(out[4])),abs(float(out[2])-float(out[5]))])
                            if "TOA" in str(x):
                                out = re.findall(r'\d+\.\d+|\d+',x)
                                toa.append([abs(float(out[0])-float(out[3])),abs(float(out[1])-float(out[4])),abs(float(out[2])-float(out[5]))])
        Values = [rssi,tdoa,toa] 
        meanX =[[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]  
        varianceS = [[0,0,0],[0,0,0],[0,0,0]] 
        count = 0 
        for var in Values:  
            for i in var:
                meanX[count][0] = meanX[count][0] + i[0]
                meanX[count][1] = meanX[count][1] + i[1]
                meanX[count][2] = meanX[count][2] + i[2]

            meanX[count][0]=meanX[count][0]/len(var)
            meanX[count][1]=meanX[count][1]/len(var)
            meanX[count][2]=meanX[count][2]/len(var)

            for k in var:
                varianceS[count][0] = varianceS[count][0] + (k[0] - meanX[count][0])**2
                varianceS[count][1] = varianceS[count][1] + (k[1] - meanX[count][1])**2
                varianceS[count][2] = varianceS[count][2] + (k[2] - meanX[count][2])**2

            varianceS[count][0] = varianceS[count][0] /len(var)
            varianceS[count][1] = varianceS[count][1]/len(var)
            varianceS[count][2] = varianceS[count][2]/len(var)
            count = count + 1
        fileInput = "RSSI Performance:\n    Average Error :\n      E[X] = "+str(meanX[0][0])+", E[Y] = "+str(meanX[0][1])+", E[Z] = "+str(meanX[0][2])+"\n"+\
                    "    Variance Error:\n      V[X] = "+str(varianceS[0][0])+", V[Y] = "+str(varianceS[0][1])+", V[Z] = "+str(varianceS[0][2])+"\n\n"+\
                    "TDOA Performance:\n    Average Error :\n      E[X] = "+str(meanX[1][0])+", E[Y] = "+str(meanX[1][1])+", E[Z] = "+str(meanX[1][2])+"\n"+\
                    "    Variance Error:\n      V[X] = "+str(varianceS[1][0])+", V[Y] = "+str(varianceS[1][1])+", V[Z] = "+str(varianceS[1][2])+"\n\n"+\
                    "TOA  Performance:\n    Average Error :\n      E[X] = "+str(meanX[2][0])+", E[Y] = "+str(meanX[2][1])+", E[Z] = "+str(meanX[2][2])+"\n"+\
                    "    Variance Error:\n      V[X] = "+str(varianceS[2][0])+", V[Y] = "+str(varianceS[2][1])+", V[Z] = "+str(varianceS[2][2])+"\n"
        fileSummary.write(fileInput)
