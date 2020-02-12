import math
from math_Tools import *
from scipy.constants import c as speed_of_light

class Data:
    def tetrahedronContour(baseNodes):
        distancesTetrahedron = {}
        temp = baseNodes.copy()
        for keys,values in baseNodes.items():
            for key2,values2 in temp.items():
                if keys != key2:
                    distancesTetrahedron.update( {str(keys)+str(key2) : mathTools.nodeDistancesCalculation(values,values2)} )
        return distancesTetrahedron

    def Distances_Data_Input(baseNodes,X):
        dist = {}
        for keys,values in baseNodes.items():
            distance = mathTools.nodeDistancesCalculation(values,X)
            dist.update({str(keys) : distance})
        return dist

    def RSSI_Data_Input(transittionPower,noise,baseNodes,X):
        RSSIdbm = {}
        for keys,values in baseNodes.items():
            distance = mathTools.nodeDistancesCalculation(values,X)
            RSSIdbm.update({str(keys) : - (10 * noise * math.log(distance, 10) - transittionPower)})
        return RSSIdbm

    def TODA_Data_Input(baseNodes,X):
        TDOA = {}
        temp = baseNodes.copy()
        for keys,values in baseNodes.items():
            del temp[keys]
            for key2,values2 in temp.items():
                TDOA.update( {"R"+str(keys)+str(key2) : mathTools.nodeDistancesCalculationDiff(values,values2,X)/speed_of_light} )
        return TDOA

    def TOA_Data_Input(baseNodes,X):
        TOA = {}
        for keys,values in baseNodes.items():
            TOA.update({str(keys) : (mathTools.nodeDistancesCalculation(values,X))/speed_of_light} )
        return TOA
