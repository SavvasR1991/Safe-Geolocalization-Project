import os
import sys
import time

from math_Tools import *
from data_Creator import *
from scipy.constants import c as speed_of_light

class Algorithms:
    
    def RSSI_Algorithm_Multilateration(nodes,RSSIdbm,xyzRSSI,transittionPower,noise,pickForCalc,time_s):
        r = []
        for keys,rssidbm in RSSIdbm.items():
            r.append(10**((transittionPower-rssidbm)/(10*noise)))
        start_time = time.time()
        xyzRSSI.append(mathTools.multilaterationCalculator(nodes,r,pickForCalc))
        time_s.append(time.time() - start_time)

    def RSSI_Algorithm_Direct_Location_Method(nodes,RSSIdbm,xyzRSSI,transittionPower,noise,pickForCalc,time_s):
        r = []
        for keys,rssidbm in RSSIdbm.items():
            r.append(10**((transittionPower-rssidbm)/(10*noise)))
        start_time = time.time()
        xyzRSSI.append(mathTools.Direct_Location_Method(nodes,r,pickForCalc))
        time_s.append(time.time() - start_time)

    def TOA_Algorithm_Multilateration(nodes, TOA,xyzTOA,pickForCalc,time_s):
        r = []
        for keys,toa in TOA.items():
            r.append(toa*speed_of_light)
        start_time = time.time()
        xyzTOA.append(mathTools.multilaterationCalculator(nodes,r,pickForCalc))
        time_s.append(time.time() - start_time)

    def TOA_Algorithm_Direct_Location_Method(nodes, TOA,xyzTOA,pickForCalc,time_s):
        r = []
        for keys,toa in TOA.items():
            r.append(toa*speed_of_light)
        start_time = time.time()
        xyzTOA.append(mathTools.Direct_Location_Method(nodes,r,pickForCalc))
        time_s.append(time.time() - start_time)

    def TDOA_Algorithm_CHAN(nodes, toa,xyzTDOA,time_s):
        start_time = time.time()
        x1=nodes["A"][0]; x2=nodes["B"][0]; x3=nodes["C"][0]; x4=nodes["D"][0]; x5=nodes["E"][0]
        y1=nodes["A"][1]; y2=nodes["B"][1]; y3=nodes["C"][1]; y4=nodes["D"][1]; y5=nodes["E"][1]
        z1=nodes["A"][2]; z2=nodes["B"][2]; z3=nodes["C"][2]; z4=nodes["D"][2]; z5=nodes["E"][2]
        R1 = toa["A"]*speed_of_light; R2 = toa["B"]*speed_of_light
        R3 = toa["C"]*speed_of_light; R4 = toa["D"]*speed_of_light; R5 = toa["E"]*speed_of_light
        BS_X_MAX=x1; BS_Y_MAX=y1; BS_X_MIN=x1; BS_Y_MIN=y1; BS = [nodes["A"],nodes["B"],nodes["C"],nodes["D"]]
        for  i in range(0,3):
            if (BS_X_MAX<BS[i + 1][0]):
                BS_X_MAX=BS[i+1][0]
            if (BS_Y_MAX<BS[i + 1][1]):
                BS_Y_MAX = BS[i + 1][1]
            if (BS_X_MIN>BS[i+1][0]):
                BS_X_MIN = BS[i+1][0]
            if (BS_Y_MIN>BS[i + 1][1]):
                BS_Y_MIN=BS[i+1][1]

        Ga = [[0,0,0],[0,0,0],[0,0,0]];Q = [[1,0,0],[0,1,0],[0,0,1]]; Za0 = [0,0,0];Za1 = [0,0,0];sh = [0,0,0];h = []
        B = [[0,0,0],[0,0,0],[0,0,0]]; FI = [[0,0,0],[0,0,0],[0,0,0]]; covZa = [[0,0,0],[0,0,0],[0,0,0]];Za2 = [0,1]
        Ba2 = [[0,0,0],[0,0,0],[0,0,0]];sFI = [[0,0,0],[0,0,0],[0,0,0]]
        temp0 = [[0,0,0],[0,0,0],[0,0,0]]; temp1 = [[0,0,0],[0,0,0],[0,0,0]]   
        temp2 = [[0,0,0],[0,0,0],[0,0,0]]; temp3 = [0,0,0,0,0,0,0,0,0]   
        temp4 = [0,0,0,0,0,0,0,0,0];       temp5 = [[0,0,0],[0,0,0],[0,0,0]]   
        temp6 = [[0,0,0],[0,0,0],[0,0,0]]; temp7 = [[0,0,0],[0,0,0],[0,0,0]]   
        R21 = abs(R2 - R1);  R31 = abs(R3 - R1); R41 = abs(R4 - R1)
        K1 = (x1**2) + (y1**2); K2 = (x2**2) + (y2**2);K3 = (x3**2) + (y3**2); K4 = (x4**2) + (y4**2)
        h.append(0.5*(R21**2)-K2+K1);h.append(0.5*(R31**2)-K3+K1); h.append(0.5*(R41**2)-K4+K1)
        x21= x2 - x1; x31= x3 - x1; x41= x4 - x1;y21= y2 - y1; y31= y3 - y1; y41= y4 - y1
        Ga[0][0]= -x21; Ga[0][1]= -y21; Ga[0][2]= -R21
        Ga[1][0]= -x31; Ga[1][1]= -y31; Ga[1][2]= -R31
        Ga[2][0]= -x41; Ga[2][1]= -y41; Ga[2][2]= -R41
        temp0 = Ga.copy()  
        mathTools.mulMatri(temp0,Q,temp1)
        mathTools.mulMatri(temp1, Ga, temp2)
        mathTools.Matrix2Vector(temp2,temp3)
        mathTools.inv(temp3, temp4, 3)
        mathTools.Vector2Matrix(temp4, temp5)
        mathTools.mulMatri(temp5,temp0,temp6)
        mathTools.mulMatri(temp6, Q, temp7)
        mathTools. MatrixPlusVextor(temp7,h,Za0)	
        B[0][0]= math.sqrt( (x1-Za0[0])**2 + (y1-Za0[1])**2 )
        B[1][1]= math.sqrt( (x2-Za0[0])**2 + (y2-Za0[1])**2 ) 
        B[2][2]= math.sqrt( (x3-Za0[0])**2 + (y3-Za0[1])**2 ) 
        temp0 = [[0,0,0],[0,0,0],[0,0,0]]    
        mathTools.mulMatri(B,Q,temp0)
        mathTools.mulMatri(temp0,B,FI)
     
        temp0 = [[0,0,0],[0,0,0],[0,0,0]]; temp1 = [0,0,0,0,0,0,0,0,0]  
        temp2 = [0,0,0,0,0,0,0,0,0]; temp3 = [[0,0,0],[0,0,0],[0,0,0]]   
        temp4 = [[0,0,0],[0,0,0],[0,0,0]]; temp5 = [[0,0,0],[0,0,0],[0,0,0]]   
        temp6 = [0,0,0,0,0,0,0,0,0]; temp7 = [0,0,0,0,0,0,0,0,0]
        temp8 = [[0,0,0],[0,0,0],[0,0,0]]; temp9 = [[0,0,0],[0,0,0],[0,0,0]]   
        temp10 = [[0,0,0],[0,0,0],[0,0,0]]   
        temp0 = Ga.copy()  
        mathTools.Matrix2Vector(FI,temp1)
        mathTools.inv(temp1, temp2, 3)
        mathTools.Vector2Matrix(temp2, temp3)
        mathTools.mulMatri(temp0,temp3,temp4)
        mathTools.mulMatri(temp4,Ga,temp5)
        mathTools.Matrix2Vector(temp5,temp6)
        mathTools.inv(temp6, temp7, 3)
        mathTools.Vector2Matrix(temp7, temp8)
        mathTools.mulMatri(temp8,temp0,temp9)
        mathTools.mulMatri(temp9,temp3,temp10)
        mathTools.MatrixPlusVextor(temp10,h,Za1)
        if Za1[2]<0:
	        Za1[2]=-Za1[2]
        for i in range(0,3):
	        for j in range(0,3):
		        covZa[i][j]=temp8[i][j]
        Ba2[0][0]= Za1[0]-x1;Ba2[1][1]= Za1[1]-y1; Ba2[2][2]= Za1[2]
        temp0=[[0,0,0],[0,0,0],[0,0,0]]; temp1=[[0,0,0],[0,0,0],[0,0,0]]
        mathTools.mulMatri(Ba2,covZa,temp0)
        mathTools.mulMatri(temp0,Ba2,temp1)
        for i in range(0,3):
            for j in range(0,3):
                sFI[i][j]=4*temp1[i][j];
        sh[0]=(Za1[0]-x1)**2
        sh[1]=(Za1[1]-y1)**2
        sh[2]=Za1[2]**2

        temp0 = [[1,0,1],[0,1,1]]; temp1 = [0,0,0,0,0,0,0,0,0]  
        temp2 = [0,0,0,0,0,0,0,0,0]; temp3 = [[0,0,0],[0,0,0],[0,0,0]]   
        temp4 = [[0,0,0],[0,0,0]];temp5 = [[0,0],[0,0]]   
        temp6 = [0,0,0,0]; temp7 = [0,0,0,0]
        temp8 = [[0,0],[0,0]];temp9 = [[0,0,0],[0,0,0]]
        mathTools.Matrix2Vector(sFI,temp1)
        mathTools.inv(temp1, temp2, 3)
        mathTools.Vector2Matrix(temp2, temp3)
        mathTools.mulMatri_23X33(temp0,temp3,temp4)
        temp5[0][0]=temp4[0][0]+temp4[0][2]
        temp5[0][1]=temp4[0][1]+temp4[0][2]
        temp5[1][0]=temp4[1][0]+temp4[1][2]
        temp5[1][1]=temp4[1][1]+temp4[1][2]
        mathTools.Matrix2Vector_22(temp5,temp6)
        mathTools.inv(temp6, temp7, 2)
        mathTools.Vector2Matrix_22(temp7, temp8)
        for i in range(0,2):
            for j in range(0,3):
                for k in range(0,2):
                    temp9[i][j] = temp9[i][j] + temp8[i][k] * temp4[k][j]
        Za2[0]=abs(temp9[0][0]*sh[0]+temp9[0][1]*sh[1]+temp9[0][2]*sh[2])
        Za2[1]=abs(temp9[1][0]*sh[0]+temp9[1][1]*sh[1]+temp9[1][2]*sh[2])
        POS = [[0,0],[0,0],[0,0],[0,0]]
        POS[0][0] = math.sqrt(Za2[0]) + x1
        POS[0][1] = math.sqrt(Za2[1]) + y1
        POS[1][0] = -math.sqrt(Za2[0]) + x1
        POS[1][1] = -math.sqrt(Za2[1]) + y1
        POS[2][0] = math.sqrt(Za2[0]) - x1
        POS[2][1] = math.sqrt(Za2[1]) - y1
        POS[3][0] = -math.sqrt(Za2[0]) - x1
        POS[3][1] = -math.sqrt(Za2[1]) - y1
        POS_Y =0;POS_X=0;POS_Z=0
        for i in range(0,4):
            if ((POS[i][0]<BS_X_MAX) and (POS[i][0]>BS_X_MIN)):
                POS_X = POS[i][0]
        for i in range(0,4):
            if ((POS[i][1]<BS_Y_MAX) and (POS[i][1]>BS_Y_MIN)):
                POS_Y = POS[i][1]
        xyzTDOA.append([POS_X,POS_Y,POS_Z])
        time_s.append(time.time() - start_time)
       
    def TDOA_Algorithm_FourNodes(nodes, toa,xyzTDOA,time_s):
        start_time = time.time()
        e = 5
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
            if  abs(abs(x)-abs(temp[0]))>e:
                x=temp[0]
            if  abs(abs(y)-abs(temp[1]))>e:
                y=temp[1]
            if  abs(abs(z)-abs(temp[2]))>e:
                z=temp[2]
        xyzTDOA.append([-x,-y,-z])
        time_s.append(time.time() - start_time)

    def Run_Selected_Algorithms(nodes,calculatedTraces,calculatedValues,xyz,transittionPower,noise,pickForCalc,algorithms,dirTotalTime):
        execution = []  
        calculatedTraces.update({"Traces" : xyz})
        for keys,values in algorithms.items():
            for val in values:
                execution.append(getattr(Algorithms,str(keys)+"_Algorithm_"+str(val)))
        x, y, z = zip(*xyz)
        tmpRSSI = [[] for i in range(len(algorithms["RSSI"]))]
        tmpTDOA = [[] for i in range(len(algorithms["TDOA"]))]
        tmpTOA = [[] for i in range(len(algorithms["TOA"]))]
        tmpRSSITime = [[] for i in range(len(algorithms["RSSI"]))]
        tmpTDOATime = [[] for i in range(len(algorithms["TDOA"]))]
        tmpTOATime = [[] for i in range(len(algorithms["TOA"]))]
        for i in range(0, len(x)):
            for func in execution:
                count = 0
                if "RSSI" in str(func):
                    timeRssi=[]
                    for rssi in algorithms["RSSI"]:
                        func(nodes,calculatedValues["RSSI"][i],tmpRSSI[count],transittionPower,noise,pickForCalc,tmpRSSITime[count])
                        count = count + 1
                elif "TDOA" in str(func):
                    timeTDOA=[]
                    for tdoaVar in algorithms["TDOA"]:
                        func(nodes,calculatedValues["TOA"][i],tmpTDOA[count],tmpTDOATime[count])
                        count = count + 1
                elif "TOA" in str(func):
                    timeTOA=[]
                    for toaVar in algorithms["TOA"]:
                        func(nodes,calculatedValues["TOA"][i],tmpTOA[count],pickForCalc,tmpTOATime[count])
                        count = count + 1
                else:
                    exit(-1)
        for keys,values in algorithms.items():
            for val in values: 
                count = 0
                if "RSSI" in keys: 
                    calculatedTraces.update({str(keys)+"_"+str(val) : tmpRSSI[count]})
                    dirTotalTime.update({str(keys)+"_"+str(val) : tmpRSSITime[count]})
                    count = count + 1
                elif "TDOA" in keys: 
                    calculatedTraces.update({str(keys)+"_"+str(val) : tmpTDOA[count]})
                    dirTotalTime.update({str(keys)+"_"+str(val) : tmpTDOATime[count]})
                    count = count + 1
                else:
                    calculatedTraces.update({str(keys)+"_"+str(val) : tmpTOA[count]})
                    dirTotalTime.update({str(keys)+"_"+str(val) : tmpTOATime[count]})
                    count = count + 1

