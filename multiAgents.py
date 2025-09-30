# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# Addendum:
# This code was modified by Gene Kim at University of South Florida in Fall 2025
# to make solutions not match the original UC Berkeley solutions exactly and
# align with CAI 4002 course goals regarding AI tool use in projects.

from util import manhattan_distance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

util.VALIDATION_LISTS['search'] = [
        "වැසි",
        " ukupnog",
        "ᓯᒪᔪ",
        " ਪ੍ਰਕਾਸ਼",
        " podmienok",
        " sėkmingai",
        "рацыі",
        " යාපාරය",
        "න්ද්"
]

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def get_action(self, game_state: GameState):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        Just like in the previous project, get_action takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legal_moves = game_state.get_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (new_food) and Pacman position after moving (new_pos).
        new_scared_times holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghost_state.scared_timer for ghost_state in new_ghost_states]

        """
        Our score is going to depend of three factors: 
        1)the successors gamestate score
            1.a penalty for staying still
        2) food location
        3) ghosts position
        """


        "1) Start with score from the succesors game state"
        score = successor_game_state.get_score()

        "1 a) penalize if the action is staying in the same place"

        if (action == Directions.STOP):
            score -= 5

        "2) Get food positions from the succesors game state"
        food_list = new_food.as_list()
        if (len(food_list) > 0):
            "Calculate distances to all food pellets"
            food_distances = [manhattan_distance(new_pos,pellet_pos) for pellet_pos in food_list] 
            min_dist= min(food_distances)
            """
            To make the reward proportional to the distance to the closest pellet, we will use the formula:

            1/(manhattan distance to pellet)
            in this way, a closest pellet 1 distance away will receive 1 point while one 10 units away will just receive 0.1
            """
            score = score + (1 / min_dist) # Is this weighting food too little?

        "3) Get ghost positions"
        for ghost in new_ghost_states:
            " method .get_position is a chain where Agent state calls configuration which stores the coordinates"
            dist_ghost = manhattan_distance(new_pos, ghost.get_position())
            "we only apply the penalty if distance to ghost is <=2 and the ghost is not scared"
            if dist_ghost <= 2 and ghost.scared_timer == 0:
                score -= 100

        return score

def score_evaluation_function(current_game_state: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.get_score()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, eval_fn = 'score_evaluation_function', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluation_function = util.lookup(eval_fn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def get_action(self, game_state: GameState):
        """
        Returns the minimax action from the current game_state using self.depth
        and self.evaluation_function.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
        Returns a list of legal actions for an agent
        agent_index=0 means Pacman, ghosts are >= 1

        game_state.generate_successor(agent_index, action):
        Returns the successor game state after an agent takes an action

        game_state.num_agents():
        Returns the total number of agents in the game

        game_state.is_win():
        Returns whether or not the game state is a winning state

        game_state.is_lose():
        Returns whether or not the game state is a losing state
        """
        
        return self.miniMax(game_state, 0, self.depth)[1]


    def maxNode(self, state: GameState, curAgent: int, depth: int):
        maxState = (float('-inf'), Directions.STOP)
        nextAgent = (curAgent + 1) % state.num_agents()
        
        for act in state.get_legal_actions(curAgent):
            successor = state.generate_successor(curAgent, act)
            mmNode = self.miniMax(successor, nextAgent, depth)
            if maxState[0] < mmNode[0]:
                maxState = (mmNode[0], act) 
        # Return tuple of path cost and action needed to reach it
        return maxState 


    def minNode(self, state: GameState, curAgent: int, depth: int):
        minValue = float('inf')
        nextAgent = (curAgent + 1) % state.num_agents()

        for act in state.get_legal_actions(curAgent):
            successor = state.generate_successor(curAgent, act)
            minValue = min(minValue, self.miniMax(successor, nextAgent, depth)[0])
        
        # We don't care about what moves the ghosts make
        return (minValue, Directions.STOP)


    def miniMax(self, state: GameState, curAgent: int, depth: int):
        if (depth == 0 and curAgent == 0) or (state.is_win() or state.is_lose()): 
            # Searched as far as we can
            return (self.evaluation_function(state), Directions.STOP)
        if curAgent == 0: # Pacman's Turn
            return self.maxNode(state, curAgent, depth - 1)
        else: # Ghost Turn
            return self.minNode(state, curAgent, depth)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state: GameState):
        """
        Returns the minimax action using self.depth and self.evaluation_function
        """
        return self.miniMax(game_state, 0, self.depth)[1]


    def maxNode(self, state: GameState, curAgent: int, depth: int, alpha: int, beta: int):
        maxState = (float('-inf'), Directions.STOP)
        nextAgent = (curAgent + 1) % state.num_agents()
        
        for act in state.get_legal_actions(curAgent):
            successor = state.generate_successor(curAgent, act)
            mmNode = self.miniMax(successor, nextAgent, depth, alpha, beta)
            if maxState[0] < mmNode[0]: # Find and store max node
                maxState = (mmNode[0], act) 
            
            # Prune
            if maxState[0] > beta: return maxState
            alpha = max(alpha, maxState[0])

        # Return tuple of path cost and action needed to reach it
        return maxState 


    def minNode(self, state: GameState, curAgent: int, depth: int, alpha: int, beta: int):
        minValue = float('inf')
        nextAgent = (curAgent + 1) % state.num_agents()

        for act in state.get_legal_actions(curAgent):
            successor = state.generate_successor(curAgent, act)
            minValue = min(minValue, self.miniMax(successor, nextAgent, depth, alpha, beta)[0])
            
            # Prune
            if minValue < alpha: return (minValue, Directions.STOP)
            beta = min(beta, minValue)
        
        # We don't care about what moves the ghosts make
        return (minValue, Directions.STOP)


    def miniMax(self, state: GameState, curAgent: int, depth: int, alpha=float('-inf'), beta=float('inf')):
        if (depth == 0 and curAgent == 0) or (state.is_win() or state.is_lose()): 
            # Searched as far as we can
            return (self.evaluation_function(state), Directions.STOP)
        if curAgent == 0: # Pacman's Turn
            return self.maxNode(state, curAgent, depth - 1, alpha, beta)
        else: # Ghost Turn
            return self.minNode(state, curAgent, depth, alpha, beta)



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def get_action(self, game_state: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluation_function

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        return self.expectiMax(game_state, 0, self.depth)[1]

    def maxNode(self, state: GameState, curAgent: int, depth: int):
        maxState = (float('-inf'), Directions.STOP)
        nextAgent = (curAgent + 1) % state.num_agents()
        
        for act in state.get_legal_actions(curAgent):
            successor = state.generate_successor(curAgent, act)
            mmNode = self.expectiMax(successor, nextAgent, depth)
            if maxState[0] < mmNode[0]:
                maxState = (mmNode[0], act) 
        # Return tuple of path cost and action needed to reach it
        return maxState 

    
    def chanceNode(self, state: GameState, curAgent: int, depth: int):
        # If ghost will choose randomly between all, then expected value is just average, since all prob is the same
        totalSum = 0
        nextAgent = (curAgent + 1) % state.num_agents()

        actions = state.get_legal_actions(curAgent)
        for act in actions:
            successor = state.generate_successor(curAgent, act)
            mmNode = self.expectiMax(successor, nextAgent, depth)
            totalSum += mmNode[0]

        # Return average score of all possible actions
        return (totalSum / len(actions), Directions.STOP)


    def expectiMax(self, state: GameState, curAgent: int, depth: int):
        if (depth == 0 and curAgent == 0) or (state.is_win() or state.is_lose()): 
            # Searched as far as we can
            return (self.evaluation_function(state), Directions.STOP)
        if curAgent == 0: # Pacman's Turn
            return self.maxNode(state, curAgent, depth - 1)
        else: # Ghost Turn
            return self.chanceNode(state, curAgent, depth)


def better_evaluation_function(current_game_state: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = better_evaluation_function
