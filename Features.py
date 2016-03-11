from peg_markov import state2board, possibleActions
from JasperAndZot import *
import random

class Features:

    def __init__(self, game):
        self.game = game # Maybe the game's initial state? So for peg solitaire a full board?

    def entropy(self, prob_matrix):
        """
        Parameters:
          prob_matrix: the transition probability matrix for the game
        Returns entropy of outcome distribution.
        https://en.wikipedia.org/wiki/Entropy_%28information_theory%29#Definition
        """
        return 0

    def possibleActions(self, actF):
        """
        Parameters:
          actF: a function that returns possible actions.
        Returns number of possible actions in game. 
        """
        return 0

    def winToFinal(self):
        """
        Returns ratio of win states to final states.
        """
        return 0


    def loseToFinal(self):
        """
        Returns ratio of lose states to final states.
        """
        return 0

    def movesToFinal(self):
        """
        Returns average number of moves before reaching a final state.
        """
        return 0

    def generateGames(self, game, policy, n):
        """
        Takes in a game's initial state and a policy, then simulates actions and state
        transitions until terminal state reached. Returns tuple of 3 elements
          0) List of states visited
          1) List of actions taken
          2) List of rewards received
		Repeats this process n times, returning a list of each simulation's result.
        """
        results = []
        for i in xrange(n):
        	results.append(game.policy)
        return results

    "Takes in the current game state and returns a randomly selected move"
    def random_policy(self, gamestate):
        game = self.game
        if game == 'Peg Solitaire': #not sure about what type 'game' is so need to double check
            board = peg_markov.state2board(gamestate)
            actions = peg_markov.possibleActions(board)
        elif game == 'Jasper and Zot':
            if gamestate.phase == 2:
                roll = JasperAndZot.diceRoll()
                dice1 = roll[0]
                dice2 = roll[1]
                actions = JasperAndZot.possible_moves_2(gamestate, dice1, dice2)
            elif gamestate.phase == 3:
                actions = JasperAndZot.possible_moves_3(gamestate)
            elif gamestate.phase == 4:
                actions = JasperAndZot.possible_moves_4(gamestate)
        return random.choice(actions)



