import os
import sys
from math_Tools import *
from data_Creator import *
from scipy.constants import c as speed_of_light

class Algorithms:
    
    def RSSI_Algorithm_Multilateration(nodes,RSSIdbm,xyzRSSI,transittionPower,noise,pickForCalc):
        r = []
        for keys,rssidbm in RSSIdbm.items():
            r.append(10**((transittionPower-rssidbm)/(10*noise)))
        xyzRSSI.append(mathTools.multilaterationCalculator(nodes,r,pickForCalc))

    def TOA_Algorithm_Multilateration(nodes, TOA,xyzTOA,pickForCalc):
        r = []
        for keys,toa in TOA.items():
            r.append(toa*speed_of_light)
        xyzTOA.append(mathTools.multilaterationCalculator(nodes,r,pickForCalc))


    def TDOA_Algorithm_CHAN(nodes, toa,xyzTDOA):
        if xyzTDOA:        
            temp = xyzTDOA[-1]
        x1=nodes["A"][0]; x2=nodes["B"][0]; x3=nodes["C"][0]; x4=nodes["D"][0];
        y1=nodes["A"][1]; y2=nodes["B"][1]; y3=nodes["C"][1]; y4=nodes["D"][1];
        z1=nodes["A"][2]; z2=nodes["B"][2]; z3=nodes["C"][2]; z4=nodes["D"][2];
        
        x31=x3-x1; x41=x4-x1; x32=x3-x2; x42=x4-x2
        y31=y3-y1; y41=y4-y1; y32=y3-y2; y42=y4-y2
        z31=z3-z1; z41=z4-z1; z32=z3-z2; z42=z4-z2
        
        R1 = toa["A"]*speed_of_light; R2 = toa["B"]*speed_of_light
        R3 = toa["C"]*speed_of_light; R4 = toa["D"]*speed_of_light
        R23 =(R2 - R3); R24 = (R2 - R4); R14 = (R1 - R4); R13 = (R1 - R3)
        
        K1 = (x1**2+y1**2+z1**2) ; K2 = (x2**2+y2**2+z2**2)
        K3 = (x3**2+y3**2+z3**2) ; K4 = (x4**2+y4**2+z4**2)
        K13 = K1 - K3; K14 = K1 - K4; K23 = K2 - K3; K24 = K2 - K4
        Am = np.array([[2*(x1-x2),2*(y1-y2),2*(z1-z2)],[2*(x3-x4),2*(y3-y4),2*(z3-z4)],[(x31/R13)-(x41/R14),(y31/R13)-(y41/R14),(z31/R13)-(z41/R14)],[(x32/R23)-(x42/R24),(y32/R23)-(y42/R24),(z32/R23)-(z42/R24)]])
        invAm = np.linalg.pinv(Am)
        
        b = np.array([(R1**2-R2**2-K1+K2),(R3**2-R4**2-K3+K4),0.5*(R14-R13+K14/R14- K13/R13),0.5*(R24-R23+K24/R24-K23/R23)])

        x = invAm[0][0]*b[0]+invAm[0][1]*b[1]+invAm[0][2]*b[2]+invAm[0][3]*b[3]
        y = invAm[1][0]*b[0]+invAm[1][1]*b[1]+invAm[1][2]*b[2]+invAm[1][3]*b[3]
        z = invAm[2][0]*b[0]+invAm[2][1]*b[1]+invAm[2][2]*b[2]+invAm[2][3]*b[3] 
        if xyzTDOA:        
            if  abs(abs(x)-abs(temp[0]))>100:
                x=temp[0]
            if  abs(abs(y)-abs(temp[1]))>100:
                y=temp[1]
            if  abs(abs(z)-abs(temp[2]))>100:
                z=temp[2]
        xyzTDOA.append([-x,-y,-z])

       
    def TDOA_Algorithm_FourNodes(nodes, toa,xyzTDOA):
        if xyzTDOA:        
            temp = xyzTDOA[-1]
        x1=nodes["A"][0]; x2=nodes["B"][0]; x3=nodes["C"][0]; x4=nodes["D"][0];
        y1=nodes["A"][1]; y2=nodes["B"][1]; y3=nodes["C"][1]; y4=nodes["D"][1];
        z1=nodes["A"][2]; z2=nodes["B"][2]; z3=nodes["C"][2]; z4=nodes["D"][2];
        
        x31=x3-x1; x41=x4-x1; x32=x3-x2; x42=x4-x2
        y31=y3-y1; y41=y4-y1; y32=y3-y2; y42=y4-y2
        z31=z3-z1; z41=z4-z1; z32=z3-z2; z42=z4-z2
        
        R1 = toa["A"]*speed_of_light; R2 = toa["B"]*speed_of_light
        R3 = toa["C"]*speed_of_light; R4 = toa["D"]*speed_of_light
        R23 =(R2 - R3); R24 = (R2 - R4); R14 = (R1 - R4); R13 = (R1 - R3)
        
        K1 = (x1**2+y1**2+z1**2) ; K2 = (x2**2+y2**2+z2**2)
        K3 = (x3**2+y3**2+z3**2) ; K4 = (x4**2+y4**2+z4**2)
        K13 = K1 - K3; K14 = K1 - K4; K23 = K2 - K3; K24 = K2 - K4
        Am = np.array([[2*(x1-x2),2*(y1-y2),2*(z1-z2)],[2*(x3-x4),2*(y3-y4),2*(z3-z4)],[(x31/R13)-(x41/R14),(y31/R13)-(y41/R14),(z31/R13)-(z41/R14)],[(x32/R23)-(x42/R24),(y32/R23)-(y42/R24),(z32/R23)-(z42/R24)]])
        invAm = np.linalg.pinv(Am)
        
        b = np.array([(R1**2-R2**2-K1+K2),(R3**2-R4**2-K3+K4),0.5*(R14-R13+K14/R14- K13/R13),0.5*(R24-R23+K24/R24-K23/R23)])

        x = invAm[0][0]*b[0]+invAm[0][1]*b[1]+invAm[0][2]*b[2]+invAm[0][3]*b[3]
        y = invAm[1][0]*b[0]+invAm[1][1]*b[1]+invAm[1][2]*b[2]+invAm[1][3]*b[3]
        z = invAm[2][0]*b[0]+invAm[2][1]*b[1]+invAm[2][2]*b[2]+invAm[2][3]*b[3] 
        if xyzTDOA:        
            if  abs(abs(x)-abs(temp[0]))>100:
                x=temp[0]
            if  abs(abs(y)-abs(temp[1]))>100:
                y=temp[1]
            if  abs(abs(z)-abs(temp[2]))>100:
                z=temp[2]
        xyzTDOA.append([-x,-y,-z])

    

    def Run_Selected_Algorithms(nodes,calculatedTraces,calculatedValues,xyz,transittionPower,noise,pickForCalc,algorithms):
        execution = []  
        calculatedTraces.update({"Traces" : xyz})
        for keys,values in algorithms.items():
            for val in values:
                execution.append(getattr(Algorithms,str(keys)+"_Algorithm_"+str(val)))
        x, y, z = zip(*xyz)
        tmpRSSI = [[] for i in range(len(algorithms["RSSI"]))]
        tmpTDOA = [[] for i in range(len(algorithms["TDOA"]))]
        tmpTOA = [[] for i in range(len(algorithms["TOA"]))]
        for i in range(0, len(x)):
            for func in execution:
                count = 0
                if "RSSI" in str(func):
                    for rssi in algorithms["RSSI"]:
                        func(nodes,calculatedValues["RSSI"][i],tmpRSSI[count],transittionPower,noise,pickForCalc)
                        count = count + 1
                elif "TDOA" in str(func):
                    for tdoaVar in algorithms["TDOA"]:
                        func(nodes,calculatedValues["TOA"][i],tmpTDOA[count])
                        count = count + 1
                elif "TOA" in str(func):
                    for toaVar in algorithms["TOA"]:
                        func(nodes,calculatedValues["TOA"][i],tmpTOA[count],pickForCalc)
                        count = count + 1
                else:
                    exit(-1)
        for keys,values in algorithms.items():
            for val in values: 
                count = 0
                if "RSSI" in keys: 
                    calculatedTraces.update({str(keys)+"_"+str(val) : tmpRSSI[count]})
                    count = count + 1
                elif "TDOA" in keys: 
                    calculatedTraces.update({str(keys)+"_"+str(val) : tmpTDOA[count]})
                    count = count + 1
                else:
                    calculatedTraces.update({str(keys)+"_"+str(val) : tmpTOA[count]})
                    count = count + 1

