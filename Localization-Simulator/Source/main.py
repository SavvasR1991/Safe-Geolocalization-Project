import numpy as np
import sys

from simulator import *
from statistics_Collector import *


def main():
    inputArg = {}
    xyz = [];
    xyzTDOA = []; xyzRSSI = []; xyzTOA=[]
    calculatedValues = {}
    calculatedTraces = {}
    RSSIValues = []; TDOAValues = [];TOAValues = [];distances=[]
    rssiAlg =[];tdoaAlg = [];toaAlg = []
    nodesTmp = [];  X = []; alpha = 'A';nodes = {}; algorithms = {};algorithmstmp=[];totalNodes = 0;curArgm = "";curAlg=""
    labelsTrace = ["Trace "]
    labelsStatistics = []
    metrics_SI = {"DISTANCES": "meters","RSSI": "dBm","TIME":"sec"}
    
    if len(sys.argv) < 40:
        print("Wrong input provided in main.py... Abort........")
        exit(-1)
    for argm in sys.argv:
        if "--" in argm:
            curArgm  = argm
        else:
            if curArgm == "--X":
                X.append(float(argm))
            elif curArgm == "--nd":
                nodesTmp.append(float(argm))
            elif curArgm == "--Tal":
                if argm in "RSSI" or argm in "TDOA" or argm in "TOA":
                    curAlg  = argm
                else:
                    if curAlg in "RSSI":
                        rssiAlg.append(argm)
                    elif curAlg in "TDOA":
                        tdoaAlg.append(argm)
                    elif curAlg in "TOA":
                        toaAlg.append(argm)
            elif curArgm == "--tp":
                transittionPower = float(argm)
            elif curArgm == "--noi":
                noise = float(argm)
            elif curArgm == "--m":
                 m= int(argm)
            elif curArgm == "--st":
                n= int(argm)
            elif curArgm == "--d":
                d= float(argm)
            elif curArgm == "--t":
                t= float(argm)
            elif curArgm == "--exp":
                totalExperiments = int(argm)
            elif curArgm == "--pl":
                plot= argm
            elif curArgm == "--top":
                pickForCalc= argm
            else:
                continue
    algorithms.update({"RSSI":rssiAlg})
    algorithms.update({"TDOA":tdoaAlg})
    algorithms.update({"TOA":toaAlg})
    for key,values in algorithms.items():
        if values:
            for val in values:
                labelsStatistics.append(str(key)+"_"+str(val)+"_Performance")
                labelsTrace.append(str(key)+" "+str(val)+"  ")

    for i in range(0, int(nodesTmp[0])): 
        nodes.update( {str(alpha) : np.array([nodesTmp[i*3+1],nodesTmp[i*3+2],nodesTmp[i*3+3]])} )
        alpha = chr(ord(alpha) + 1)

    folder = Simulation.initialize()

    print("-----------------------Creating experiments-----------------------")
    for repeat in range(0,totalExperiments):

        Simulation.setup()    

        Simulation.brownian_motion_simulation(xyz,X,m,n,d,t)
        mathTools.printProgressBar(repeat*7  , totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.simulationDataCreation(nodes,transittionPower,noise,xyz,distances,calculatedValues,algorithms)
        mathTools.printProgressBar(repeat*7+1, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
        Simulation.simulation(nodes,xyz,calculatedTraces,calculatedValues,transittionPower,noise,pickForCalc,algorithms)
        mathTools.printProgressBar(repeat*7+2, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.storeDataFiles(nodes,transittionPower,noise,distances,calculatedValues,xyz,calculatedTraces,metrics_SI)
        mathTools.printProgressBar(repeat*7+3, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.plotGraphics(nodes,calculatedTraces,plot)
        mathTools.printProgressBar(repeat*7+4, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.plotStatisticsGraphics(nodes,calculatedTraces,calculatedValues)
        mathTools.printProgressBar(repeat*7+5, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.cleanup(xyz,xyzTDOA,xyzRSSI,xyzTOA,RSSIValues,TDOAValues,TOAValues,distances)
        mathTools.printProgressBar(repeat*7+6, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

    Collector.statisticsCollector(folder,algorithms)
    mathTools.printProgressBar(totalExperiments*7, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)
    print("-----------------------Experiments created-----------------------")

if __name__ == "__main__":
    main()
