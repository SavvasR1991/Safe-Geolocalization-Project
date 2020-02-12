import os
import math
import numpy as np

class mathTools():
    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        if iteration == total: 
            print()

    def nodeDistancesCalculation(p1,p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2])**2)
        
    def nodeDistancesCalculationDiff(p1,p2,E):
        return abs(math.sqrt((p2[0] - E[0]) ** 2 + (p2[1] - E[1]) ** 2 + (p2[2] - E[2])**2) - math.sqrt((p1[0] - E[0]) ** 2 + (p1[1] - E[1]) ** 2 + (p1[2] - E[2])**2))

    def Direct_Location_Method(nodes,r,pickForCalc):
        r1 = r[0]; r2 = r[1]; r3 = r[2]; r4 = r[3] 
        P1 = np.array(nodes["A"]);P2 = np.array(nodes["B"]);P3 = np.array(nodes["C"])
        if "Yes" in pickForCalc:        
            P4 = np.array(nodes["D"])
        else:
            P4 = np.array(nodes["E"])
            r4 = r[4] 
        x1 = P1[0];x2 = P2[0];x3 = P3[0];x4 = P4[0];
        y1 = P1[1];y2 = P2[1];y3 = P3[1];y4 = P4[1];
        z1 = P1[2];z2 = P2[2];z3 = P3[2];z4 = P4[2];

        A1 = ( r1**2 - r2**2 ) + ( x2**2 - x1**2 ) + ( y2**2 - y1**2 ) + ( z2**2 - z1**2 )
        A2 = ( r1**2 - r3**2 ) + ( x3**2 - x1**2 ) + ( y3**2 - y1**2 ) + ( z3**2 - z1**2 )
        A3 = ( r1**2 - r4**2 ) + ( x4**2 - x1**2 ) + ( y4**2 - y1**2 ) + ( z4**2 - z1**2 )
        
        I1 = ( z3 - z1 )*( x2 - x1 ) - ( z2 - z1 )*( x3 - x1 ) 
        I2 = ( z4 - z1 )*( x2 - x1 ) - ( z2 - z1 )*( x4 - x1 ) 
        I3 = ( z3 - z1 )* A1 - ( z2 - z1 ) * A2 
        I4 = ( z4 - z1 )* A1 - ( z2 - z1 ) * A3
        I5 = ( z3 - z1 )*( y2 - y1 ) - ( z2 - z1 )*( y3 - y1 )
        I6 = ( z4 - z1 )*( y2 - y1 ) - ( z2 - z1 )*( y4 - y1 )
        I7 = ( y3 - y1 )*( x2 - x1 ) - ( y2 - y1 )*( x3 - x1 )
        I8 = ( y4 - y1 )*( x2 - x1 ) - ( y2 - y1 )*( x4 - x1 )
        I9 = ( y3 - y1 )* A1 - ( y2 - y1 )* A2 
        I10 = ( y4 - y1 )* A1 - ( y2 - y1 )* A3
        I11 = ( y3 - y1 )*( z2 - z1 ) - ( y2 - y1 )*( z3 - z1 )
        I12 = ( y4 - y1 )*( z2 - z1 ) - ( y2 - y1 )*( z4 - z1 )

        x= 1/2 * ((I4*I5 - I3*I6)/(I2*I5 - I1*I6))
        y= 1/2 * ((I1*I4 - I2*I3)/(I1*I6 - I2*I5))
        z= 1/2 * ((I7*I10 - I8*I9)/(I7*I12 - I8*I11))
        return [x,y,z]
        
    def multilaterationCalculator(nodes,r,pickForCalc):
        r1 = r[0];r2 = r[1];r3 = r[2]; r4 = r[3]
        P1 = np.array(nodes["A"]); P2 = np.array(nodes["B"])
        tempr3 = r3
        if "Yes" in pickForCalc:        
            P3 = np.array(nodes["D"])
            r3 = r4
        else:
            P3 = np.array(nodes["C"])
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
        if "Yes" in pickForCalc:  
            calcDist = mathTools.nodeDistancesCalculation([x,y,z],nodes["C"])
            mirrorXYZ = [0,0,0]
            if abs(calcDist - tempr3) > 0.00000000007: 
                zz = (-B - rootD) / (2 * A)
                x = g * (zz) + h; y = e * (zz) + f
                return [x,y,zz]
            else:
                return [x,y,z]
        else:
            return [x,y,z]
  
    def mulMatri(temp0,Q,temp1):
        for i in range(0,3):
            for j in range(0,3):
                for k in range(0,3):
                    temp1[i][j] += temp0[i][k] * Q[k][j]

    def Matrix2Vector(matrixA,vectorB):
        k = 0
        for i in range(0,3):
            for j in range(0,3):
                vectorB[k]=matrixA[i][j]
                k = k + 1

    def rem(a, i, j, n):
        pTemp = []
        for tm in range(0,(n - 1)*(n - 1)):
            pTemp.append(0)
        for k in range(0,i):
            for  m in range(0,j):
                pTemp[k*(n - 1) + m] = a[k*n + m]
            for m in range(j,n-1): 
                pTemp[k*(n - 1) + m] = a[k*n + m + 1]
        for k in range(i,n-1): 
            for m in range(0,j):
                pTemp[k*(n - 1) + m] = a[(k + 1)*n + m];
            for m in range(j,n-1):
                pTemp[k*(n - 1) + m] = a[(k + 1)*n + m + 1]
        if (i + j) % 2 == 1:
            return -1
        else:
            return mathTools.det(pTemp, n - 1)

    def det(a,n):       
        if n == 1:
            return a[0]
        sum = 0.0
        for j in range(0,n):
            sum += a[0 * n + j] * mathTools.rem(a, 0, j, n);
        return sum

    def inv(a, b, n):
        deta = mathTools.det(a, n); 
        for i in range (0,n):
            for j in range (0,n):
                b[i*n + j] = mathTools.rem(a, j, i, n) / deta;

    def Vector2Matrix(vectorC,matrixD):
        k=0
        for i in range(0, 3):
            for j in range(0, 3):
                matrixD[i][j]=vectorC[k]
                k = k + 1

    def mulMatri_23X33(x,y,z):
        m=2
        n=3
        for i in range(0, m):
            for j in range(0, n):
                z[i][j] = 0;
            for k in range(0, n):
                z[i][j] = z[i][j] + x[i][k] * y[k][j]

    def Matrix2Vector_22(matrixA, vectorB):
        k=0
        for i in range(0, 2): 
            for j in range(0, 2):
                vectorB[k]=matrixA[i][j]
                k = k +1

    def Vector2Matrix_22(vectorC,matrixD):
        k=0
        for i in range(0, 2): 
            for j in range(0, 2): 
                matrixD[i][j]=vectorC[k]
                k = k +1
    
    def MatrixPlusVextor(matrixE,matrixF, vectorC):
        vectorC[0]=matrixE[0][0]*matrixF[0]+matrixE[0][1]*matrixF[1]+matrixE[0][2]*matrixF[2]
        vectorC[1]=matrixE[1][0]*matrixF[0]+matrixE[1][1]*matrixF[1]+matrixE[1][2]*matrixF[2]
        vectorC[2]=matrixE[2][0]*matrixF[0]+matrixE[2][1]*matrixF[1]+matrixE[2][2]*matrixF[2]
