Matthew West & Miguel Mateo Osorio Vela

https://github.com/MWest17/proj2-multi-agent-search

Engineering Process:

For Q1, 

For Q2-4, we first implemented Minimax using the dispatch approach. 
It took a little to generalize it to more than 2 agents and to make it depth limited.
But once we got a working minimax, the rest was relatively simple. 
Alpha Beta pruning was just minimax again, but slightly changed
Expectimax was also quick to implement since the min node function was just needed to be replaced with a chance node function
Since all actions for the ghost were random, the expectimax value was just the average of the legal actions.

For Q5,

AI Use:
Matthew - I didn't use AI beyond python syntax

Miguel Mateo - 
