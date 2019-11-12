import numpy
from numpy import sqrt, dot, cross
from numpy.linalg import norm

# Find the intersection of three spheres
# P1,P2,P3 are the centers, r1,r2,r3 are the radii
# Implementaton based on Wikipedia Trilateration article.

pointImportSeparator = 0
shapeCounter = 1
text_file = open("Output.txt", "w")

with open('test1.txt','r') as f:
    temp = []
    for line in f:
        x = line.split()
        if x:
            if pointImportSeparator == 0:
                P1 = numpy.array([float(x[0]), float(x[1]) ,float(x[2])])
                xa = float(x[0])
                ya = float(x[1])
                za = float(x[2])
            elif pointImportSeparator == 1:
                P2 = numpy.array([float(x[0]), float(x[1]) ,float(x[2])])
                xb = float(x[0])
                yb = float(x[1])
                zb = float(x[2])
            elif pointImportSeparator == 2:
                P3 = numpy.array([float(x[0]), float(x[1]) ,float(x[2])])
                xc = float(x[0])
                yc = float(x[1])
                zc = float(x[2])
            elif pointImportSeparator == 3:
                P4 = numpy.array([float(x[0]), float(x[1]) ,float(x[2])])
                xd = float(x[0])
                yd = float(x[1])
                zd = float(x[2])


                r1=sqrt((xa - xd)**2 + (ya - yd)**2 + (za - zd)**2)
                r2=sqrt((xb - xd)**2 + (yb - yd)**2 + (zb - zd)**2)
                r3=sqrt((xc - xd)**2 + (yc - yd)**2 + (zc - zd)**2)

                temp1 = P2-P1
                e_x = temp1/norm(temp1)
                temp2 = P3-P1
                i = dot(e_x,temp2)
                temp3 = temp2 - i*e_x
                e_y = temp3/norm(temp3)
                e_z = cross(e_x,e_y)
                d = norm(P2-P1)
                j = dot(e_y,temp2)
                x = (r1*r1 - r2*r2 + d*d) / (2*d)
                y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)
                temp4 = r1*r1 - x*x - y*y
                if temp4<0:
                    raise Exception("The three spheres do not intersect!");
                z = sqrt(temp4)
                p_12_a = P1 + x*e_x + y*e_y + z*e_z

                output = "The Base of the Triangular Pyramid of Shape "+str(shapeCounter)+\
                         " is :\nA = [" +str(xa) +","+ str(ya)+" ,"+ str(za)+"]\nB = [ "+str(xb)+" , "+str(yb)+" , "+str(zb)+\
                         "]\nC = [ "+str(xc)+" , "+str(yc)+" , "+str(zc)+"]\nThe unknown Node has    D  = [ "+str(xd)+" , "+str(yd)+" , "+str(zd)+\
                         "]\nThe length of A,D is  |AD| = [ "+str(r1)+"]\nThe length of B,D is  |BD| = [ "+str(r2)+"]\nThe length of C,D is  |CD| = [ "+str(r3)+\
                         "]\nThe algorithm calcuted: D =  [ "+str(p_12_a[0]) +","+ str(p_12_a[1])+" ,"+ str(p_12_a[2])+" ]\n\n"
                print(p_12_a)
                print(shapeCounter)
                text_file.write(output)

                shapeCounter = shapeCounter +1
            if pointImportSeparator == 3:
                pointImportSeparator = 0
            else:
                pointImportSeparator = pointImportSeparator + 1

text_file.close()
