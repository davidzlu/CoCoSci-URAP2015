from peg_solitaire import PegSolitaire
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


    "Takes in the current game state and returns a randomly selected move"
    def random_policy(self):
        game = self.game
        actions = game.possible_actions()
        return random.choice(actions)

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
        for i in range(n):
            results.append(game.play(game, policy))
        return results

if __name__ == '__main__':
    game = PegSolitaire()
    ext = Features(game)



