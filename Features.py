import peg_solitaire as ps
import JasperAndZot as jz
import random
import math
import numpy as np

class Features:

    def __init__(self, gameClass):
        self.game = gameClass # The GameState class or its equivalent
        self.results = [] # List of (states visited, actions taken, rewards gained) tuples
        self.currentGame = None

    def entropy(self):
        """
        Returns entropy of outcome distribution.
        https://en.wikipedia.org/wiki/Entropy_%28information_theory%29#Definition
        """
        tpm = self.game().transition_prob_matrix()
        logtpm = np.log(tpm)
        ent = 0.0
        for i in range(len(tpm)):
            if tpm[i] != 0:
                ent += tpm[i]*logtpm[i]
        return -ent

    def possibleActions(self):
        """
        Returns the average number of moves possible at any state in the game.
        """
        total = 0
        for i in range(len(self.results)):
            subtotal = 0
            allstates = self.results[i][0] 
            for state in allstates:
                # either self might be the state, or an actual state gets passed in
                subtotal += len(self.game.possible_actions(state, state)) 
            total += subtotal / len(allstates)
        average = total / len(self.results)
        return average

    def actionsStd(self):
        """ Returns the average standard deviation of possible moves
         over all the games"""

        average = self.possibleActions()
        total = 0
        for i in range(len(self.results)):
            subtotal = 0
            allstates = self.results[i][0] 
            for state in allstates:
                # either self might be the state, or an actual state gets passed in
                subtotal += (len(self.game.possible_actions(state, state)) - average) ** 2
            total += math.sqrt(subtotal / len(allstates))
        std = total / len(self.results)
        return std

    def winToFinal(self):
        """
        Returns ratio of win states to final states.
        """
        total_wins = 0
        for target in self.results:
            if target[3] == True:
                total_wins = total_wins + 1
        return float(total_wins) / float(len(self.results))

    def numWinStates(self):
        diff_wins = 0
        winStates = []
        for target in self.results:
            if target[3] == True:
                if target[0][-1] not in winStates:
                    winStates.append(target[0][-1])
                    diff_wins += 1
        return diff_wins


    def loseToFinal(self):
        """
        Returns ratio of lose states to final states.
        """
        total_loses = 0
        for target in self.results:
            if target[3] == False:
                total_loses = total_loses + 1
        return float(total_loses) / float(len(self.results))

    def movesToFinal(self):
        """
        Returns average number of moves before reaching a final state.
        """
        total_acts = 0
        for target in self.results:
            total_acts = total_acts + len(target[1])
        return float(total_acts) / (len(self.results))


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
            if i > 0 and i % 4999 == 0:
                self.generateFeatures("temp")
            # print("Finished game number", i)
        return self.results

    def clearResults(self):
        """
        Deletes results from generated games by replacing self.results with empty list.
        """
        yesSet = {"Y", "y", "yes", "Yes"}
        userConfirm = raw_input("Are you sure you want to clear the results? Y/N")
        if userConfirm in yesSet:
            self.results = []
            print("Results cleared.")
        else:
            print("Results not cleared.")

    def generateFeatures(self, fileName):
        """
        Calls all feature methods and writes results to text file.
        """
        fileName += ".txt"
        toWrite = open(fileName, "w")
        toWrite.write( "Results from " + str(len(self.results)) + " games\n" )

        # Features to calculate below
        toWrite.write("Entropy " + str(self.entropy()) + "\n")
        toWrite.write("possibleActions " + str(self.possibleActions()) + "\n")
        toWrite.write("winToFinal " + str(self.winToFinal()) + "\n")
        toWrite.write("loseToFinal " + str(self.loseToFinal()) + "\n")
        toWrite.write("movesToFinal " + str(self.movesToFinal()) + "\n")

        toWrite.close()


if __name__ == '__main__':
    psinst = Features(ps.PegSolitaire)
    psinst.generateGames(ps.random_policy, 10)
    # # psinst.generateFeatures("ps1")
    # jzinst = Features(jz.GameState)
    # jzinst.generateGames(jzinst.random_policy, 10000)
    # jzinst.generateFeatures("jz1")
