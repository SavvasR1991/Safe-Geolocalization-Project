import math
from math_Tools import *
from scipy.constants import c as speed_of_light

class Data:
    def tetrahedronContour(nodes):
        distancesTetrahedron = {
            "AB":mathTools.nodeDistancesCalculation(nodes[0],nodes[1]),
            "AC":mathTools.nodeDistancesCalculation(nodes[0],nodes[2]),
            "AD":mathTools.nodeDistancesCalculation(nodes[0],nodes[3]),
            "BC":mathTools.nodeDistancesCalculation(nodes[1],nodes[2]),
            "BD":mathTools.nodeDistancesCalculation(nodes[1],nodes[3]),
            "CD":mathTools.nodeDistancesCalculation(nodes[2],nodes[3]),
        }
        distancesTetrahedron["CA"] =distancesTetrahedron["AC"]; distancesTetrahedron["BA"]=distancesTetrahedron["AB"]
        distancesTetrahedron["DA"] =distancesTetrahedron["AD"]; distancesTetrahedron["BC"]=distancesTetrahedron["BC"]
        distancesTetrahedron["BD"] =distancesTetrahedron["BD"]; distancesTetrahedron["DC"]=distancesTetrahedron["CD"]
        return distancesTetrahedron

    def Distances_Data_Input(baseNodes,E):
        dist = []
        for i in range(len(baseNodes)):
            distance = mathTools.nodeDistancesCalculation(baseNodes[i],E)
            dist.append(distance)
        return dist

    def RSSI_Data_Input(transittionPower,noise,baseNodes,E):
        RSSIdbm = []
        for i in range(len(baseNodes)):
            distance = mathTools.nodeDistancesCalculation(baseNodes[i],E)
            RSSIdbm.append(- (10 * noise * math.log(distance, 10) - transittionPower))
        return RSSIdbm

    def TODA_Data_Input(baseNodes,E):
        TDOA = {
            "R1":mathTools.nodeDistancesCalculation(baseNodes[0],E)/speed_of_light,
            "R2":mathTools.nodeDistancesCalculation(baseNodes[1],E)/speed_of_light,
            "R3":mathTools.nodeDistancesCalculation(baseNodes[2],E)/speed_of_light,
            "R4":mathTools.nodeDistancesCalculation(baseNodes[3],E)/speed_of_light,
            "R12":mathTools.nodeDistancesCalculationDiff(baseNodes[0],baseNodes[1],E)/speed_of_light,
            "R13":mathTools.nodeDistancesCalculationDiff(baseNodes[0],baseNodes[2],E)/speed_of_light,
            "R14":mathTools.nodeDistancesCalculationDiff(baseNodes[0],baseNodes[3],E)/speed_of_light,
            "R23":mathTools.nodeDistancesCalculationDiff(baseNodes[1],baseNodes[2],E)/speed_of_light,
            "R24":mathTools.nodeDistancesCalculationDiff(baseNodes[1],baseNodes[3],E)/speed_of_light,
            "R34":mathTools.nodeDistancesCalculationDiff(baseNodes[2],baseNodes[3],E)/speed_of_light,
        }
        TDOA["R21"]=TDOA["R12"]; TDOA["R31"]=TDOA["R13"]; TDOA["R41"]=TDOA["R14"]
        TDOA["R32"]=TDOA["R23"]; TDOA["R42"]=TDOA["R24"]; TDOA["R43"]=TDOA["R34"]
        return TDOA

    def TOA_Data_Input(baseNodes,E):
        TOA = []
        for d in baseNodes:
            TOA.append((mathTools.nodeDistancesCalculation(d,E))/speed_of_light)
        return TOA
