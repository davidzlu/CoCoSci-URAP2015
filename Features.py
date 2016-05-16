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
        estimated_entropy = 0.0
        # for game in self.results:
        #     game_states = game[0]
        for state, action, _nextState in tpm.keys():
            prob_vector = state.getMatrixRow(action)
            log_vector = np.log(prob_vector)
            vector_ent = 0.0
            for i in range(len(prob_vector)):
                if prob_vector[i] != 0:
                    vector_ent += prob_vector[i]*log_vector[i]
            estimated_entropy += vector_ent
        return -estimated_entropy/len(tpm)

    def possibleActions(self):
        """
        Returns the average number of moves possible at any state in the game.
        """
        subtotal = 0
        N = 0
        for i in range(len(self.results)):
            #subtotal = 0
            allstates = self.results[i][0] 
            for state in allstates:
                # either self might be the state, or an actual state gets passed in
                numActs = len(self.game.possible_actions(state, state))
                subtotal += numActs
            N += len(allstates)
        average = subtotal / N
        return average

    # def otherStd(self):
    #     varTotal = 0
    #     N = len(self.results)
    #     for i in range(N):
    #         allstates = self.results[i][0]
    #         actCounts = []
    #         for state in allstates:
    #             actCounts.append(len(self.game.possible_actions(state, state)))
    #         varTotal += np.var(actCounts)
    #     std = math.sqrt((varTotal / N))
    #     return std

    def avg(self, featureVects):
        """Takes in a list of lists, where each list represents a game and the values
        in that list are the values per time step that you want the stddev of
        e.g. average possible moves, rewards gained

        Returns the weighted mean for all samples"""
        
        subtotal = 0
        N = 0
        for i in range(len(featureVects)): 
            for vect in featureVects:
                subtotal += np.sum(vect)
                N += len(vect)
        average = subtotal / N
        return average

    def stddev(self, featureVects):
        """Takes in a list of lists, where each list represents a game and the values
        in that list are the values per time step that you want the stddev of
        e.g. average possible moves, rewards gained

        Returns the overall stddev for all the games played"""
        average = self.avg(featureVects)
        grandN = 0
        subtotal = 0
        numGames = len(featureVects)
        for i in range(numGames):
            for vect in featureVects:
                Ni = len(vect)
                grandN += Ni
                subtotal += (Ni - 1) * (np.std(vect) ** 2) + \
                    (Ni * (np.mean(vect) ** 2))
        sqrd = (subtotal - (grandN * (average ** 2))) / (grandN - 1)
        std = math.sqrt(sqrd)
        return std


    def actionsStd(self):
        # """ Returns the corrected sample standard deviation of possible moves
        #  over all the games"""

    #     average = self.possibleActions()
    #     total = 0
    #     N = len(self.results)
    #     for i in range(N):
    #         subtotal = 0
    #         allstates = self.results[i][0] 
    #         for state in allstates:
    #             # either self might be the state, or an actual state gets passed in
    #             subtotal += (len(self.game.possible_actions(state, state)) - average) ** 2
    #     std = math.sqrt((1 / (N - 1)) * subtotal)
    #     return std   

        # Code for overall stddev of nonoverlapping subsamples
        average = self.possibleActions()
        grandN = 0
        subtotal = 0
        numGames = len(self.results)
        for i in range(numGames):
            allstates = self.results[i][0]
            Ni = len(allstates)
            grandN += Ni
            actCounts = []
            for state in allstates:
                actCounts.append(len(self.game.possible_actions(state, state)))
            subtotal += (Ni - 1) * (np.std(actCounts) ** 2) + \
                (Ni * (np.mean(actCounts) ** 2))
        sqrd = (subtotal - (grandN * (average ** 2))) / (grandN - 1)
        std = math.sqrt(sqrd)
        return std     

    def SEM(self, std):
        N = len(self.results)
        return std / math.sqrt(N)

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

    def avgStepsToReward(self):
        """
        Returns average number of actions taken before a nonzero reward recieved.
        """
        steps_to_reward = []
        for game in self.results:
            rewards = game[2]
            steps = 0.0
            for reward in rewards:
                steps += 1.0
                if reward != 0:
                    steps_to_reward.append(steps)
                    steps = 0.0

        total_steps = 0.0
        n = 0.0
        for i in steps_to_reward:
            if i != 0:
                total_steps += i
                n += 1
        return total_steps/n

    def avgRewardAtEachTimeStep(self):
        """
        Calculates mean of rewards at each time step, and returns as a list.
        """
        averages = []
        for game in self.results:
            rewards = game[2]
            for reward in rewards:
                break

        return averages

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
        toWrite.write("avgStepsToReward " + str(self.avgStepsToReward()) + "\n")

        toWrite.close()


if __name__ == '__main__':
    # psinst = Features(ps.PegSolitaire)
    # psinst.generateGames(ps.random_policy, 1000)
    # psinst.generateFeatures("ps1")
    # jzinst = Features(jz.GameState)
    # jzinst.generateGames(jzinst.random_policy, 1000)
    # jzinst.generateFeatures("jz1")

