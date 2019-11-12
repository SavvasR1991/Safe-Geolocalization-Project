import os

from math_Tools import *
from data_Creator import *
from scipy.constants import c as speed_of_light

class Algorithms:
    def RSSI_Algorithm(nodes,RSSIdbm,xyzRSSI,transittionPower,noise):
        r1=10**((transittionPower-RSSIdbm[0])/(10*noise))
        r2=10**((transittionPower-RSSIdbm[1])/(10*noise))
        r3=10**((transittionPower-RSSIdbm[2])/(10*noise))
        xyzRSSI.append(mathTools.multilaterationCalculator(nodes,r1,r2,r3))

    def TOA_Algorithm(nodes, toa,xyzTOA):
        r1=toa[0]*speed_of_light
        r2=toa[1]*speed_of_light
        r3=toa[2]*speed_of_light
        xyzTOA.append(mathTools.multilaterationCalculator(nodes,r1,r2,r3))
       
    def TDOA_Algorithm(nodes, tdoa,xyzTDOA):
        if xyzTDOA:        
            temp = xyzTDOA[-1]
        x1=nodes[0][0]; x2=nodes[1][0]; x3=nodes[2][0]; x4=nodes[3][0];
        y1=nodes[0][1]; y2=nodes[1][1]; y3=nodes[2][1]; y4=nodes[3][1];
        z1=nodes[0][2]; z2=nodes[1][2]; z3=nodes[2][2]; z4=nodes[3][2];
        
        x31=x3-x1; x41=x4-x1; x32=x3-x2; x42=x4-x2
        y31=y3-y1; y41=y4-y1; y32=y3-y2; y42=y4-y2
        z31=z3-z1; z41=z4-z1; z32=z3-z2; z42=z4-z2
        
        R1 = tdoa[0]*speed_of_light; R2 = tdoa[1]*speed_of_light
        R3 = tdoa[2]*speed_of_light; R4 = tdoa[3]*speed_of_light
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

