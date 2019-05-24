import problem
import simulator as sim
import sys
from importlib import import_module


if __name__ == "__main__":
    # read command line arguments
    totalTime = int(sys.argv[3])
    agentNameSeller = sys.argv[1]
    agentNameBuyer = sys.argv[2]
    sel = getattr(import_module(agentNameSeller), agentNameSeller)
    buy = getattr(import_module(agentNameBuyer), agentNameBuyer)
    host = sys.argv[4]

    # get problem information from problem-file
    sellerWeights, buyerWeights, bidDomain, valueFunction, allBidsUtility1, allBidsUtility2 = problem.problem1()

    # Create simulator. The simulator starts agents and the negotiation, and starts plotting at init
    simulator = sim.Simulator(buyerWeights, sellerWeights, bidDomain, valueFunction, totalTime, sel, buy, host,
                              allBidsUtility1, allBidsUtility2)
