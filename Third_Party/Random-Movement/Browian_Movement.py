# Python Version 3.7
# Import packages with pip3
#   -> matplotlib
#   -> random
#   -> mpl_toolkits
#   -> math
#   -> numpy



import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import math
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from urllib3.connectionpool import xrange
from mpl_toolkits.mplot3d import Axes3D

def nodeDistancesCalculation(p1,p2):
    dist = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2])**2)
    return dist

def pointInsideTetrahedron(v1,v2,v3,v4,p):
    def tetraCoord_Dorian(A, B, C, D):
        v1 = B - A;
        v2 = C - A;
        v3 = D - A
        mat = np.array((v1, v2, v3)).T
        M1 = np.linalg.inv(mat)
        return (M1)
    M1=tetraCoord_Dorian(v1,v2,v3,v4)
    newp = M1.dot(p-v1)
    return (np.all(newp>=0) and np.all(newp <=1) and np.sum(newp)<=1)

def brownian_motion_simulation(xyz,cur):
    m = 3
    n = 500
    d = 1000.0
    t = 1.0
    dt = t / float(n - 1)
    for j in range(1, n):
        s = np.sqrt(2.0 * m * d * dt) * np.random.randn(1)
        dx = np.random.randn(m)
        norm_dx = np.sqrt(np.sum(dx ** 2))
        print(dx)

        for i in range(0, m):
            dx[i] = s * dx[i] / norm_dx
        cur[0] += dx[0]
        cur[1] += dx[1]
        if cur[2] + dx[2] > 0:
            cur[2] += dx[2]
        else:
            cur[2] += abs(dx[2])
        p = np.array(cur[:])
        xyz.append(cur[:])

def randomWalk(xyz,cur):
    for _ in xrange(500):
        axis = random.randrange(0, 3)
        cur[axis] += random.uniform(-3, 3)
        if cur[axis] < 0:
            cur[axis] += 2
        if cur[0] > 60:
            cur[axis] -= 2
        if cur[1] > 60:
            cur[axis] -= 2
        if cur[2] > 60:
            cur[axis] -= 2
        xyz.append(cur[:])

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')

xyz = []
cur = [0,-20, 20]
A = np.array([10, -40, 0])
B = np.array([-30, 30, 0])
C = np.array([30, 30, 0])
D = np.array([0, 0, 30])

brownian_motion_simulation(xyz,cur)

x, y, z = zip(*xyz)

file = open("TraceOutput.txt","w")
header = " A = " + str(A) + "\n B = " + str(B) + "\n C = " + str(C) + "\n D = " + str(C) + "\n\n"
file.write(header)
file.write("Node E Trace Log: \n\n")
for i in range(0 , len(x)):
    inputFile = "[ " + str(x[i]).ljust(10)[:15] + ", " + str(y[i]).ljust(10)[:15]   + ", " + str(z[i]).ljust(10) [:15]  + "] :\t\t Distances-> AE = " + str(nodeDistancesCalculation(A,[x[i],y[i],z[i]])).ljust(10)[:15] + ", BE = " + str(nodeDistancesCalculation(B,[x[i],y[i],z[i]])).ljust(10)[:15] + ", CE =  "+ str(nodeDistancesCalculation(C,[x[i],y[i],z[i]])).ljust(10)[:15]+ ", DE =  " + str(nodeDistancesCalculation(D,[x[i],y[i],z[i]])).ljust(10)[:15] + "\n"
    file.write(inputFile)

ax.plot(x, y, z,'C3', label='E node movement')
ax.scatter(cur[0], cur[1], cur[2],'C7',label="End")
ax.scatter(x[0], y[0], z[0],'C3',label="Start")

v = np.array([A, B, C, C ,D ])
ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

verts = [ [v[0],v[1],v[4]], [v[0],v[3],v[4]],[v[2],v[1],v[4]], [v[2],v[3],v[4]], [v[0],v[1],v[2],v[3]]]
ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
ax.scatter(x[-1], y[-1], z[-1], c='b', marker='o')
ax.legend()
plt.show()