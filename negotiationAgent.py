import time
import random
import spade


class negotiationAgent(spade.agent.Agent):
    def __init__(self, agentjid, password, weights, startTime, totalTime, bidDomain, valueFunction, role, opponent):
        super().__init__(jid = agentjid, password = password)

        #Role to decide who starts bid
        self.role = role

        #Times to know when to start and end
        self.startTime = startTime
        self.totalTime = totalTime

        #Information to calculate utility
        self.weights = weights
        self.bidDomain = bidDomain
        self.valueFunction = valueFunction

        #Jid for opponent
        self.opponent = opponent

        #These lists will be filled with utility for sent and received bids
        #They will be plotted in the simulator during negotiation
        self.receivedUtility = []
        self.sentUtility = []


    #Behaviour for receiving bid, determine whether to accept or not, and send message back with "accepted" or new bid
    class manageBidBehaviour(spade.behaviour.CyclicBehaviour):
        def __init__(self, agent):
            super().__init__()
            self.agent = agent

        async def on_start(self):
            print("manageBidBehaviour started")

        async def run(self):
            msg = await self.receive(timeout=20)
            if msg:
                print(str(self.agent.jid)+" received message at time "+ str(self.agent.getTime()))
                #check if negotiation is timing out
                if time.time()>self.agent.startTime + self.agent.totalTime:
                    print("Time up, no agreement"+"\n")
                    self.kill(exit_code=10)

                # check if the other agent accepted this agent's last bid
                if msg.body == "True":
                    print("last offer from "+str(self.agent.jid)+" accepted by "+self.agent.opponent)
                    print("terminating agent"+"\n")
                    # stop the negotiation
                    self.kill(exit_code=10)
                else:
                    print("last offer from "+str(self.agent.jid)+" not accepted by "+self.agent.opponent)

                    #decode bid, add to list for plotting
                    bid = msg.body.split(',')
                    for i in range(len(bid)):
                        bid[i]=float(bid[i])
                    self.agent.receivedUtility.append(self.agent.getUtility(bid))

                    # If the received offer is accepted by this agent, send message to other agent and stop negotiation
                    if self.agent.acceptOffer(bid):
                        msg = spade.message.Message()
                        msg.set_metadata("performative", "bid")
                        msg.body = "True"
                        msg.to = self.agent.opponent
                        print(str(self.agent.jid)+" accepts new offer received from "+self.agent.opponent)
                        print("terminating agent"+"\n")
                        await self.send(msg)
                        self.agent.isFinished=True
                        self.kill(exit_code=10)
                    else:
                        # else calculate new bid and send

                        bid = self.agent.proposeOffer()

                        #recode bid
                        stringBid = ""
                        for i in range(len(bid)):
                            if i == len(bid)-1:
                                stringBid += str(bid[i])
                            else:
                                stringBid += str(bid[i])+','

                        msg = spade.message.Message()
                        msg.set_metadata("performative", "bid")
                        msg.body = stringBid
                        msg.to = self.agent.opponent
                        print(str(self.agent.jid)+" sending offer " + stringBid + " to "+str(msg.to)+"\n")

                        #add new bid to list for plotting
                        self.agent.sentUtility.append(self.agent.getUtility(bid))
                        await self.send(msg)

            else:
                print("no msg")


    #Behaviour for sending first offer
    class startNegotiationBehaviour(spade.behaviour.OneShotBehaviour):
        def __init__(self, agent):
            super().__init__()
            self.agent = agent

        async def run(self):
            #Wait for starttime to send first bid
            while time.time() < self.agent.startTime:
                continue
            print("Negotiation started")

            #make bid, recode to string, add to list for plotting, and send
            bid = self.agent.proposeOffer()
            stringBid = ""
            for i in range(len(bid)):
                if i == len(bid) - 1:
                    stringBid += str(bid[i])
                else:
                    stringBid += str(bid[i]) + ','
            msg = spade.message.Message()
            msg.set_metadata("performative", "bid")
            msg.body = stringBid
            msg.to = self.agent.opponent
            msg.sender = str(self.agent.jid)
            self.agent.sentUtility.append(self.agent.getUtility(bid))
            await self.send(msg)
            print("Message 1 sent!")

            self.kill(exit_code=10)



    def setup(self):
        print("Agent starting...")

        #Behaviour for receiving and sending bids
        b1 = self.manageBidBehaviour(self)
        template = spade.template.Template()
        template.set_metadata("performative","bid")
        self.add_behaviour(b1, template)

        #Behaviour for sending first bid only
        if self.role == "buyer":
            b2 = self.startNegotiationBehaviour(self)
            self.add_behaviour(b2)



    #Calculates utility for agent based on its weights, and the offer (and valueFunction)
    def getUtility(self, offer):
        values=[]
        for i in range(len(self.valueFunction)):
            #Calculating value by V_i = a + ((x//b)/c)*d to get V as even grid from a to a+d with c steps
            values.append(self.valueFunction[i][0] + ((offer[i]//self.valueFunction[i][1])/self.valueFunction[i][2])*self.valueFunction[i][3])

        utility = 0
        for i in range(len(self.weights)):
            #Applying weights to value
            utility += self.weights[i]*values[i]

        return utility

    #Makes 20 random offers, and uses a kind of gradient descent to achieve utility between SLow and SHigh
    def getOffers(self, SLow, SHigh):

        length  =len(self.weights)

        #To decide whether we must go "uphill" or "downhill" in utility function to get to goal
        def fitness(offer):
            utility = self.getUtility(offer)
            if SLow - utility > 0:
                return 1
            elif utility - SHigh > 0:
                return -1
            else:
                return 0

        #Make random offer
        def spawn_instance():
            return [random.uniform(self.bidDomain[i][0], self.bidDomain[i][1]) for i in range(length)]

        # Moves one step in the direction of the weights (negative direction if it must go downhill)
        def one_step_gradient_descent(offer):
            fitnessOffer = fitness(offer)
            for i in range(length):
                newstep = 1 * self.weights[i] * self.valueFunction[i][1]
                #Ensures that we don't move out of the domain
                if (offer[i] + newstep * fitnessOffer> self.bidDomain[i][0]) and (offer[i] + newstep * fitnessOffer < self.bidDomain[i][1]):
                    offer[i] += newstep * fitnessOffer
            return offer

        offers = []
        for i in range(20):
            offers.append(spawn_instance())



        #perform one-step function until all bids are in range (or timeout)
        for i in range(len(offers)):
            counter=0
            while fitness(offers[i]) != 0 and counter<500:
                offers[i] = one_step_gradient_descent(offers[i])
                counter += 1

        return offers

    #Returns relative time used (0 to 1)
    def getTime(self):
        return (time.time() - self.startTime) / self.totalTime

    #To be modified for strategy
    def acceptOffer(self, bid):
        return

    # To be modified for strategy
    def update(self):
        return

    # To be modified for strategy
    def proposeOffer(self):
        return
