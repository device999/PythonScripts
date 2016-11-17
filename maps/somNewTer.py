import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import random
import math
import sys
import csv
import time

def updateSOMNeighborLine(learningRate,sigma,i,winnerIndice, pattern, neighborValue, gl):
    graph_dist = lambda gl, i1, i2: min(int(gl- max(i1, i2) + min(i1, i2)), abs(i1 - i2))
    result = learningRate*math.exp(-np.abs(graph_dist(gl, i, winnerIndice)*(dist(pattern,neighborValue)/MAXDIST))/(2*sigma))*(neighborValue - pattern)
    #

    #print result
    return pattern + result

# def updateSOMNeighborLine(learningRate,sigma,i,winnerIndice,neighborValue,pattern, gl):
#     graph_dist = lambda graphLen, i1, i2: min(int(graphLen - max(i1,i2) + min(i1,i2)), abs(i1- i2))
#
#     result = learningRate * math.exp(-np.abs(graph_dist(gl, i, winnerIndice))/(2*sigma))*(pattern - neighborValue)
#     return neighborValue + result


def dist(pattern,center):
    return np.sqrt(np.sum((pattern-center)*(pattern-center)))

if __name__ == "__main__":
    path = np.loadtxt('q3dm1-path1.csv', dtype=np.object, comments='#', delimiter=",")

#    path = np.loadtxt('q3dm1-path2.csv',dtype=np.object,comments='#',delimiter=",")
    secondPath = path[:,0:3].astype(np.float)
    amountCl = 50
    center = np.ones((amountCl,3))+np.random.random((amountCl,3))
    #centerOld = np.copy(center)

    mxDot = np.array([float(max(path[:,i])) for i in range(path.shape[1])])
    mnDot = np.array([float(min(path[:,i])) for i in range(path.shape[1])])
    MAXDIST = dist(mnDot, mxDot)

    center = np.array([[random.uniform(mnDot[i], mxDot[i]) for i in range(path.shape[1])] for n in range(amountCl)])

    distance = np.zeros(amountCl)
    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc_data = ax.scatter(secondPath[:,0], secondPath[:,1], secondPath[:,2], zorder=1, c='r', alpha=1)
    ax.plot(center[:,0], center[:,1], center[:,2], c='b')
    sc_centers = ax.scatter(center[:,0], center[:,1], center[:,2], zorder=4, s=100, marker='o',c='b', alpha=1)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    fig.show()
    K = 10000
    for k in range(K):
        learningRate = (1-float(k)/float(K))**3
        sigma = math.exp(-float(k)/float(K))
        randomPoint = secondPath[np.random.randint(0, np.shape(secondPath)[0]),:]
        #winner = 0
        #randomPoint = secondPath[k]
        for x in range(len(distance)):
            distance[x] = dist(randomPoint,center[x])
        #winner = np.amin(distance)
        winnerIndice = np.argmin(distance)

        for i in range(len(center)):
            center[i] = updateSOMNeighborLine(learningRate,sigma,i,winnerIndice,center[i],randomPoint, len(path))

        if divmod(k, 100)[1]==0:
            plt.pause(0.1)
            sc_centers._offsets3d = (center[:, 0], center[:, 1], center[:, 2])
            plt.draw()
            plt.show()


                #    plt.pause(0.0001)

    # sc_centers._offsets3d = (center[:, 0], center[:, 1], center[:, 2])
    # ax.plot(center[:, 0], center[:, 1], center[:, 2], c='b')
    # fig.show()
    # plt.show()

    # with open('C:/out/out.csv', 'w') as fl:
    #     np.savetxt(fl, center, delimiter=';')
         #print k
        #print center
        #plotting(center,secondPath,amountCl)
        
