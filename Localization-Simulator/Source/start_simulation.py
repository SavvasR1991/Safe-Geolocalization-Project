import numpy as np
import json
import os

from main import *

HOME = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', ''))

with open(str(HOME)+'/Input/inputData.json') as json_file:
    data = json.load(json_file)
    expCount = 1
    arguments = ""
    for p in data:
        if expCount == 1:
            print("-------------------------- Executing "+str(expCount)+"st Experiment ---------------------------------------")
        else:        
            print("-------------------------- Executing "+str(expCount)+"nd Experiment ---------------------------------------")
        abort = "No"
        if len(p) != 12:
            print("Wrong input format in /Input/inputData.json file... Abort..")
            abort = "Yes"
        else:
            E = p["X"]
            if len(E) !=3 or ((type(E[0]) and type(E[1]) and type(E[2]) !=int) and (type(E[0]) and type(E[1]) and type(E[2]) !=float)):
                print("Wrong input in /Input/inputData.json file for Node unknown")
                print("--->1. [x,y,z] are coordinates. Must be three numbers\n")
                abort = "Skip"
            else:
                arguments = arguments + " --X " + str(E[0])+" "+str(E[1])+" "+str(E[2])+" " 

            if len(p["nodes"]) == 1:
                arguments = arguments + " --nd " + str(len(p["nodes"][0])) + " "
                for key,values in p["nodes"][0].items():
                    if len(values) !=3 or ((type(values[0]) and type(values[1]) and type(values[2]) !=int) and (type(values[0]) and type(values[1]) and type(values[2]) !=float)):
                        print("Wrong input in /Input/inputData.json file for Node " + str(key))
                        print("--->2. [x,y,z] are coordinates. Must be three numbers \n")
                        abort = "Skip"
                    else:
                        if "D" in key:
                            if int(values[2]) < 10 :
                               print("--->2. Node D [z] axis must be greater than 10 \n")
                               abort = "Skip"
                        arguments = arguments + str(values[0])+" "+str(values[1])+" "+str(values[2])+" "
            else:
                print("Wrong input in /Input/inputData.json file for nodes")
                print("--->Node structure is wrong... \n")
                abort = "Yes"
            
            if len(p["algorithms"]) == 1:
                arguments = arguments +" --Tal "
                for key,values in p["algorithms"][0].items():
                    if (key != "TDOA" and key != "TOA" and key != "RSSI"):
                        print("3. Wrong input in /Input/inputData.json file for algorithms "+str(key))
                        abort = "Skip"
                    else:
                        arguments = arguments + str(key)+" "
                        for val in values:
                            if (val != "CHAN" and val != "Multilateration" and val != "FourNodes"):
                                print("3. Wrong input in /Input/inputData.json file for algorithms "+str(val))
                                abort = "Skip"
                            else:
                                arguments = arguments +str(val)+" "
                    
            else:
                print("Wrong input in /Input/inputData.json file for algorithms")
                print("--->Algorithms structure is wrong... \n")
                abort = "Yes"
  
            transittionPower = p["transittionPower_dBm"]
            if type(transittionPower) != int and type(transittionPower) != float:
                print("Wrong input in /Input/inputData.json file for Transmition Power")
                print("--->4. Transmition Power is in dBm. Must be a number \n")
                abort = "Skip"
            else:
                arguments = arguments + " --tp " + str(transittionPower)+" "

            noise = p["noise"]
            if float(noise)<0 or float(noise)>5 :
                print("Wrong input in /Input/inputData.json file for noise")
                print("--->5. noise coefficient is between [0(No Noise) - 5(Extreme noise)] \n")
                abort = "Skip"
            else:
                arguments = arguments + " --noi "+ str(noise)+" "

            m=p["Dimensions"]
            if int(m) != 3:
                print("Wrong input in /Input/inputData.json file for Dimensions")
                print("--->6. Simulation available only for 3 Dimensions\n")
                abort = "Skip"
            else:
                arguments = arguments + " --m "+ str(m)+" "

            n=p["steps"]
            if int(n) < 0:
                print("Wrong input in /Input/inputData.json file for steps")
                print("--->7. Steps must be greater than zero\n")
                abort = "Skip"
            else:
                arguments = arguments + " --st "+ str(n)+" "

            d=p["density"]
            if float(d) < 0:
                print("Wrong input in /Input/inputData.json file for density")
                print("--->8. Density must be greater than zero\n")
                abort = "Skip"
            else:
                arguments = arguments + " --d "+ str(d)+" "

            t=p["time_Coeff"]
            if float(t) > 1.0 or float(t) < 0:
                print("Wrong input in /Input/inputData.json file for time coefficient")
                print("--->9. Time coefficient [0,1]\n")
                abort = "Skip"
            else:
                arguments = arguments+ " --t " + str(t)+" "

            totalExperiments = p["totalExperiments"]
            if int(totalExperiments) < 1:
                print("Wrong input in /Input/inputData.json file for total Experiments")
                print("--->10. Total Experiments at least one\n")
                abort = "Skip"
            else:
                arguments = arguments+ " --exp " + str(totalExperiments)+" "

            plot = p["showPlots"]
            if plot not in "No" and plot not in "Yes":
                print("Wrong input in /Input/inputData.json file for show Plots")
                print("--->11. Show Plots must be 'Yes' or 'No'\n")
                abort = "Skip"
            else:
                arguments = arguments + " --pl "+ str(plot)+" "

            pickForCalc = p["PickForCalculation"]
            if pickForCalc not in "No" and pickForCalc not in "Yes":
                print("Wrong input in /Input/inputData.json file for show Plots")
                print("--->12. Select 'Yes' or 'No' to involve pick to trace calculation\n")
                abort = "Skip"
            else:
                arguments = arguments + " --top "+ str(pickForCalc)+" "
            expCount = expCount +1
        if abort in "Yes":
            print("Aborting...\n----------------------------------- ABORTING -----------------------------------------------\n\n")
            exit(-1)
        elif abort in "No":
            re = os.system("python3.7 main.py " + arguments)
            if re != 0:
                print("------------------------------------- FAILS ------------------------------------------------\n\n")  
            else:                     
                print("------------------------------------ SUCCESS -----------------------------------------------\n\n")        
        else:
            print("Skip this experiment...\n------------------------------------ SKIPPING ----------------------------------------------\n\n")

