import peg_solitaire as ps
import JasperAndZot as jz
import random

class Features:

    def __init__(self, gameClass):
        self.game = gameClass # The GameState class or its equivalent
        self.results = [] # List of (states visited, actions taken, rewards gained) tuples
        self.currentGame = None

    def entropy(self, prob_matrix):
        """
        Parameters:
          prob_matrix: the transition probability matrix for the game
        Returns entropy of outcome distribution.
        https://en.wikipedia.org/wiki/Entropy_%28information_theory%29#Definition
        """
        return 0

    def possibleActions(self):
        """
        Parameters:
          actF: a function that returns possible actions.
        Returns number of possible actions in game. 
        """
        return len(self.game.possible_actions(self.game()))

    def winToFinal(self):
        """
        Returns ratio of win states to final states.
        """
        total_wins = 0
        for target in self.results:
            if target[3] == True:
                total_wins = total_wins + 1
        return total_wins / len(self.results)


    def loseToFinal(self):
        """
        Returns ratio of lose states to final states.
        """
        total_loses = 0
        for target in self.results:
            if target[3] == False:
                total_loses = total_loses + 1
        return total_loses / len(self.results)

    def movesToFinal(self):
        """
        Returns average number of moves before reaching a final state.
        """
        total_acts = 0
        for target in self.results:
            total_acts = total_acts + len(target[1])
        return total_acts / len(self.results)


    "Takes in the current game state and returns a randomly selected move"
    def random_policy(self):
        game = self.currentGame
        try:
            return game.random_policy()
        except AttributeError:
            actions = game.possible_actions()
            return random.choice(actions)
        #except TypeError:
            #return

    def generateGames(self, policy, n):
        """
        Takes in a game's initial state and a policy, then simulates actions and state
        transitions until terminal state reached. Returns tuple of 3 elements
          0) List of states visited
          1) List of actions taken
          2) List of rewards received
		Repeats this process n times, returning a list of each simulation's result.
        """
        self.results = []
        for i in range(n):
            gameStart = self.game()
            self.currentGame = gameStart
            self.results.append(self.currentGame.play(policy))
        return self.results

# if __name__ == '__main__':
#     jzinst = Features(jz.GameState)
#     jzinst.generateGames(jzinst.random_policy, 2)
