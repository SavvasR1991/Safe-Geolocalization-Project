import numpy as np

from simulator import *
from statistics_Collector import *


def main():
    xyz = []; xyzTDOA = []; xyzRSSI = []; xyzTOA=[]; RSSIValues = []; TDOAValues = [] ;TOAValues = [];distances=[]

    E = [20, -20, 20]
    A = np.array([10, -40, 0])
    B = np.array([-30, 30, 0])
    C = np.array([30, 30, 0])
    D = np.array([0, 0, 30])
    transittionPower = 70
    noise = 3.5
    m=3
    n=500
    d=1000.0
    t=1.0
    totalExperiments =1
    labelsTrace = ["Node E","RSSI E","TDOA E","TOA E"]
    labelsStatistics = ["RSSI_Performance","TDOA_Performance","TOA_Performance","RSSI_Values","TDOA_Values","TOA_Values"]

    folder = Simulation.initialize()

    print("-----------------------Creating experiments-----------------------")
    for repeat in range(0,totalExperiments):

        Simulation.setup()    

        Simulation.brownian_motion_simulation(xyz,E,m,n,d,t)
        mathTools.printProgressBar(repeat*7  , totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.simulationDataCreation([A,B,C,D],transittionPower,noise,xyz,distances,RSSIValues,TDOAValues,TOAValues)
        mathTools.printProgressBar(repeat*7+1, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.simulation([A,B,C,D],[xyz,xyzRSSI,xyzTDOA,xyzTOA],[RSSIValues,TDOAValues,TOAValues],transittionPower,noise)
        mathTools.printProgressBar(repeat*7+2, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.storeDataFiles([A,B,C,D],transittionPower,noise,[distances,RSSIValues,TDOAValues,TOAValues],[xyz,xyzRSSI,xyzTDOA,xyzTOA],["Trace","RSSI","TDOA","TOA"],["meters","dBm","sec","sec"])
        mathTools.printProgressBar(repeat*7+3, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.plotGraphics(A,B,C,D,[xyz,xyzRSSI,xyzTDOA,xyzTOA],labelsTrace)
        mathTools.printProgressBar(repeat*7+4, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.plotStatisticsGraphics(A,B,C,D,xyz,[xyzRSSI,xyzTDOA,xyzTOA,RSSIValues,TDOAValues,TOAValues],labelsStatistics)
        mathTools.printProgressBar(repeat*7+5, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

        Simulation.cleanup(xyz,xyzTDOA,xyzRSSI,xyzTOA,RSSIValues,TDOAValues,TOAValues,distances)
        mathTools.printProgressBar(repeat*7+6, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)

    Collector.statisticsCollector(folder)
    mathTools.printProgressBar(totalExperiments*7, totalExperiments*7, prefix = 'Progress:', suffix = 'Complete', length = 50)
    print("-----------------------Experiments created-----------------------")

if __name__ == "__main__":
    main()
