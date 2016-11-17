# -*- coding: utf-8 -*-
"""
Created on  

@author: fame
"""

import numpy as np
import itertools as it
import matplotlib.pyplot as plt



def predict(X,W,b):
    """
    implement the function h(x, W, b) here
    X: N-by-D array of training data
    W: D dimensional array of weights
    b: scalar bias

    Should return a N dimensional array
    """
    return(np.array([np.dot(W,i)+b for i in X]))


def sigmoid(a):
    """
    implement the sigmoid here
    a: N dimensional numpy array

    Should return a N dimensional array
    """
    return(1/(1+np.exp(a)))



def l2loss(X,y,W,b):
    """
    implement the L2 loss function
    X: N-by-D array of training data
    y: N dimensional numpy array of labels
    W: D dimensional array of weights
    b: scalar bias

    Should return three variables: (i) the l2 loss: scalar, (ii) the gradient with respect to W, (iii) the gradient with respect to b
    """
    sig = sigmoid(predict(X,W,b))
    lossFunction = np.sum((y-sig)**2)
    dLdb = np.sum(2*(y-sig)*sig*(1-sig))

    dLdW = np.zeros(len(W))
    coeffArray = 2*(y-sig)*sig*(1-sig)
    for j,i in it.product(range(len(W)),range(len(y))):
        dLdW[j] += coeffArray[i]*X[i][j]

    return(lossFunction,dLdb,dLdW)




def train(X,y,W,b, num_iters=1000, eta=0.001):
    """
    implement the gradient descent here
    X: N-by-D array of training data
    y: N dimensional numpy array of labels
    W: D dimensional array of weights
    b: scalar bias
    num_iters: (optional) number of steps to take when optimizing
    eta: (optional)  the stepsize for the gradient descent

    Should return the final values of W and b
     """
    lossFunctionArray = []
    for i in range(num_iters):
        lossFunction, changeB, changeW = l2loss(X, y, W, b)
        lossFunctionArray.append(lossFunction)
        b -= eta*changeB
        W -= eta*changeW
        print i
    plt.plot(np.arange(len(lossFunctionArray)),lossFunctionArray)
    plt.show()
    return(W, b)

'''
In the main program, we run

W, b, lossFunctionArray = train(W_train, y_train, W0, b0, num_iters, eta)
plotArray(lossFunctionArray)
'''
