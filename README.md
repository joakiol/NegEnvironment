# Project for Multi-Agent Systems, UPV

In this project we've been making a bilateral negotiation environment in Python using Spade. 

- Report-Trabajo-SMA.pdf contains project report. 

- problem.py contains definition of negotiation problem. 

- simulator.py creates environment and starts negotiation agents, which automatically will start negotiating. 

- negotiationAgent.py contains protocol for negotiation. 

- boulwardAgent.py contains a simple negotiation strategy. 

- concederAgent.py contains a simple negotiation strategy. 

- main.py handles console inputs and starts simulator. 

Run program in console by: 

python main.py <sellerAgentName> <buyerAgentName> <negotiationTime(seconds)> <host(xmpp server name)>
Default agents name: concederAgent, boulwardAgent