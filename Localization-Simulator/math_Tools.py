import os
import math
import numpy as np

class mathTools():
    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

    def nodeDistancesCalculation(p1,p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2])**2)
        
    def nodeDistancesCalculationDiff(p1,p2,E):
        return abs(math.sqrt((p2[0] - E[0]) ** 2 + (p2[1] - E[1]) ** 2 + (p2[2] - E[2])**2) - math.sqrt((p1[0] - E[0]) ** 2 + (p1[1] - E[1]) ** 2 + (p1[2] - E[2])**2))
    
    def multilaterationCalculator(nodes,r1,r2,r3):
        P1 = np.array(nodes[0]); P2 = np.array(nodes[1]); P3 = np.array(nodes[2])
        x1 = P1[0]; x2 = P2[0]; x3 = P3[0]
        y1 = P1[1]; y2 = P2[1]; y3 = P3[1]
        z1 = P1[2]; z2 = P2[2]; z3 = P3[2]
        k1 = r1 * r1 - r2 * r2 - x1 * x1 + x2 * x2 - y1 * y1 + y2 * y2 - z1 * z1 + z2 * z2
        a1 = 2 * (x2 - x1); b1 = 2 * (y2 - y1); c1 = 2 * (z2 - z1)	
        k3 = r3 * r3 - r2 * r2 - x3 * x3 + x2 * x2 - y3 * y3 + y2 * y2 - z3 * z3 + z2 * z2
        a3 = 2 * (x2 - x3); b3 = 2 * (y2 - y3); c3 = 2 * (z2 - z3)
        if a1 == 0:
            e = -c1 / b1; f = k1 / b1
        elif a3 == 0:
            e = -c3 / b3; f = k3 / b3
        else:
            a31 = a3 / a1
            e = - ((a31 * c1 - c3) / (a31 * b1 - b3))
            f = (a31 * k1 - k3) / (a31 * b1 - b3)
        if b1 == 0:
            g = -c1 / a1; h = k1 / a1
        elif b3 == 0:
            g = -c3 / a3; h = k3 / a3
        else :
            b31 = b3 / b1;
            g = - ((b31 * c1 - c3) / (b31 * a1 - a3))
            h = (b31 * k1 - k3) / (b31 * a1 - a3)

        A = g * g + e * e + 1
        B = -x1 * g - y1 * e - 2 * z1 - x1 * g - y1 * e + 2 * g * h + 2 * e * f
        C = x1 * x1 + y1 * y1 + z1 * z1 - 2 * x1 * h - 2 * y1 * f + h * h + f * f - r1 * r1
        rootD = math.sqrt(B * B - 4 * A * C)
        z = (-B + rootD) / (2 * A); x = g * z + h; y = e * z + f
        return [x,y,z]
  
