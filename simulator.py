import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Simulator:
    def __init__(self, buyerWeights, sellerWeights, bidDomain, valueFunction, totalTime, sellerAgent, buyerAgent,
                 host, allBidsUtility1, allBidsUtility2):

        #Time to start and length of negotiation
        self.startTime = time.time() + 200 #the true startTime will be set after agents are created, since this action can vary in time
        self.totalTime = totalTime

        #Lists of all possible bids, for plotting
        self.allBidsUtility1 = allBidsUtility1
        self.allBidsUtility2 = allBidsUtility2

        #Info to pass to agents, which they can use for calculating utility
        self.buyerWeights = buyerWeights
        self.sellerWeights = sellerWeights
        self.bidDomain = bidDomain
        self.valueFunction = valueFunction

        #Server info
        self.host = host
        self.buyer = "buyer"+"@"+self.host
        self.seller = "seller"+"@"+self.host
        self.sellerPassword = "5678"
        self.buyerPassword = "1234"

        #Make agents
        self.sellerAgent = sellerAgent(self.seller, self.sellerPassword, weights=self.sellerWeights,
                                             startTime=self.startTime, totalTime=self.totalTime, bidDomain=self.bidDomain,
                                             valueFunction=self.valueFunction, role="seller", opponent = self.buyer)
        self.sellerAgent.start()
        time.sleep(2)
        self.buyerAgent = buyerAgent(self.buyer, self.buyerPassword, weights = self.buyerWeights,
                                            startTime=self.startTime, totalTime=self.totalTime, bidDomain=self.bidDomain,
                                            valueFunction = self.valueFunction, role = "buyer", opponent = self.seller)

        #start agents (and thereby negotiation)
        self.buyerAgent.start()

        self.startTime = time.time() + 3

        self.sellerAgent.startTime = self.startTime
        self.buyerAgent.startTime = self.startTime

        #Plot the negotiation
        self.plotting(self.allBidsUtility1, self.allBidsUtility2)


        #Closing the plot window will kill the agents
        self.sellerAgent.stop()
        self.buyerAgent.stop()

    def plotting(self, allBidsUtility1, allBidsUtility2):
        fig, ax = plt.subplots()
        plt.xlabel("Utility seller")
        plt.ylabel("Utility buyer")

        #All possible bids
        ln0, = plt.plot(allBidsUtility1, allBidsUtility2, 'o', ms=1, animated=True)
        #Bids by buyeragent
        ln1, = plt.plot([], [], marker = 'o', ms=2.5, animated=True)
        #Bids by selleragent
        ln2, = plt.plot([], [], marker = 'o', ms=2.5, animated=True)
        #Last bid of buyeragent
        ln3, = plt.plot([], [], marker = 's', ms=6, animated=True)
        #Last bid of selleragent
        ln4, = plt.plot([], [], marker = 'v', ms=6, animated=True)

        #Using the animation library of matplotlib, which needs a init and a update function
        def init1():
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            return ln0, ln1, ln2, ln3, ln4,

        def update(frame):
            #Get current list of utility of offers
            X1 = self.sellerAgent.receivedUtility.copy()
            Y1 = self.buyerAgent.sentUtility.copy()
            X2 = self.sellerAgent.sentUtility.copy()
            Y2 = self.buyerAgent.receivedUtility.copy()

            #Ensure that the lengths are compatible
            if len(X1) == len(Y1) and len(X1) > 0:
                ln1.set_data(X1, Y1)
                ln3.set_data(X1[-1], Y1[-1])
            if len(X2) == len(Y2) and len(X2) > 0:
                ln2.set_data(X2, Y2)
                ln4.set_data(X2[-1], Y2[-1])

            return ln0, ln1, ln2, ln3, ln4,

        #This will now continuously update plot by running update function
        ani1 = FuncAnimation(fig, update, init_func=init1, blit=True)

        #Show figure
        plt.show()
