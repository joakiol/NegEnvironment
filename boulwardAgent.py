import negotiationAgent as sup
import random


class boulwardAgent(sup.negotiationAgent):

    def __init__(self,agentjid, password, weights, startTime, totalTime, bidDomain, valueFunction, role, opponent):

        super().__init__(agentjid = agentjid, password = password, weights = weights, startTime = startTime,
                         totalTime = totalTime, bidDomain = bidDomain, valueFunction = valueFunction,
                         role = role, opponent = opponent)

        #Simple strategy for boulward agent
        self.beta = 0.5
        self.RU = 0.5
        self.S = 0.99

    def acceptOffer(self, bid):
        self.update()
        return self.getUtility(bid) >= self.S

    def update(self):
        self.S = 1 - (1 - self.RU) * self.getTime() ** (1 / self.beta)

    def proposeOffer(self):
        bids = self.getOffers(self.S, self.S + 0.01)
        selected = bids[random.randint(0, len(bids) - 1)]
        return selected