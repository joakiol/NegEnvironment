import numpy as np

def problem1():
    #weights
    w1 = [1.2, -0.2]
    w2 = [-0.3, 1.3]

    #domain
    bidDomain=[[0, 10000], [0, 100]]

    #Values corresponding to equation V_i(x_i) = a + ((x//b)/c)*d to get V as even grid from a to a+d with c steps
    valueFunction=[[2/15, 99.5, 100, 11/15], [0.2, 0.995, 100, 0.6]]

    #All possible bids for plotting
    allBidsUtility1, allBidsUtility2 = allBids1()
    return w1, w2, bidDomain, valueFunction, allBidsUtility1, allBidsUtility2

def allBids1():
    #returns all possible values for function V_i(x_i)
    V1 = np.linspace(2/15, 13/15, 101)
    V2 = np.linspace(0.2, 0.8, 101)

    utility1 = []
    utility2 = []

    #For all combinations of all values
    for i in range(len(V1)):
        for j in range(len(V2)):
            #Add utility for 1 and 2
            utility1.append(1.2*V1[i]-0.2*V2[j])
            utility2.append(-0.3 * V1[i] + 1.3 * V2[j])

    return utility1, utility2