import peg_solitaire as ps
import JasperAndZot as jz
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from datascience import *

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
            allstates = self.results[i][0] 
            for state in allstates:
                # either self might be the state, or an actual state gets passed in
                numActs = len(self.game.possible_actions(state, state))
                subtotal += numActs
            N += len(allstates)
        average = subtotal / N
        return average

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
        means = []
        numGames = len(featureVects)
        for i in range(numGames):
            for vect in featureVects:
                means.append(np.mean(vect))
        std = np.std(means)
        return std
  

    def actionsStd(self): 
        means = []
        numGames = len(self.results)
        for i in range(numGames):
            allstates = self.results[i][0]
            actCounts = []
            for state in allstates:
                actCounts.append(len(self.game.possible_actions(state, state)))
            means.append(np.mean(actCounts))
        std = np.std(means)
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

    def plot_possible_actions(self, ngames):
        """return a table of Possible actions for every turn"""
        possible_actions = []
        for roundResult in self.results:
            possibleActionsNumber = []
            for possibleAction in roundResult[4]:
                possibleActionsNumber.append(len(possibleAction))
            possible_actions.append(possibleActionsNumber)
        max_turns = 0
        for pATotal in possible_actions:
            if max_turns < len(pATotal):
                max_turns = len(pATotal)
        total_number_each_turn = []
        for i in range(0, max_turns):
            total_number = 0
            for pATotal in possible_actions:
                if i < len(pATotal):
                    total_number += pATotal[i]
            total_number_each_turn.append(total_number)
        table = Table().with_columns(["round", np.arange(0, max_turns), "possible actions", [x / ngames for x in total_number_each_turn]])
        # return table
        return [x / ngames for x in total_number_each_turn]

    def plot_rewards(self, ngames):
        rewards = []
        max_turns = 0
        for roundResult in self.results:
            if max_turns < len(roundResult[2]):
                max_turns = len(roundResult[2])
        for i in range(0, max_turns):
            round_rewards = 0
            for roundResult in self.results:
                if i < len(roundResult[2]):
                    round_rewards += roundResult[2][i]
            rewards.append(round_rewards)
        # table = Table().with_columns(["round", np.arange(0, max_turns), "rewards", [x / ngames for x in rewards]])
        # return table
        return [x / ngames for x in rewards]

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
    ngames = 1
    # psinst = Features(ps.PegSolitaire)
    # psinst.generateGames(ps.random_policy, ngames)
    # list_moves = []
    # for target in psinst.results:
    #     list_moves.append(len(target[1]))
    # print(list_moves)
    
    # print(psinst.results[0][2])
    # print(psinst.plot_possible_actions(ngames))
    # print(psinst.plot_rewards(ngames))
    # psinst.generateFeatures("ps1")

    # jzinst = Features(jz.GameState)
    # jzinst.generateGames(jzinst.random_policy, ngames)
    # print(np.average(psinst.plot_possible_actions(ngames)), np.average(jzinst.plot_possible_actions(ngames)))
    # print(np.std(psinst.plot_possible_actions(ngames)), np.std(jzinst.plot_possible_actions(ngames)))
    list_moves = []
    for i in range(0, 1000):
        psinst = Features(ps.PegSolitaire)
        psinst.generateGames(ps.random_policy, ngames)
        list_moves.append(psinst.avgStepsToReward())
    print(list_moves)
    # print(jzinst.plot_possible_actions(ngames))
    # print(jzinst.plot_rewards(ngames))
    # jzinst.generateFeatures("jz1")
    

    # n_groups = 2
    # # Average Actions
    # pActAvg = psinst.possibleActions()
    # jzActAvg = jzinst.possibleActions()
    # pActStd = psinst.actionsStd()
    # jzActStd = jzinst.actionsStd()
    # ActMeans = (pActAvg, jzActAvg)
    # ActStddevs = (psinst.SEM(pActStd), jzinst.SEM(jzActStd))
    # print(pActAvg)
    # print(jzActAvg)
    # print(pActStd)
    # print(jzActStd)
    # print(ActMeans)
    # print(ActStddevs)


    # # Average Rewards
    # prewards = []
    # jzrewards = []
    # for i in range(ngames):
    #     prewards.append(psinst.results[i][2])
    #     jzrewards.append(jzinst.results[i][2])
    # pRewAvg = psinst.avg(prewards)
    # jzRewAvg = jzinst.avg(jzrewards)
    # pRewStd = psinst.stddev(prewards)
    # jzRewStd = jzinst.stddev(jzrewards)
    # RewMeans = (pRewAvg, jzRewStd)
    # RewStds = (psinst.SEM(pRewStd), jzinst.SEM(jzRewStd))


    # index = np.arange(n_groups)
    # bar_width = 0.35

    # opacity = 0.4
    # error_config = {'ecolor' : '0.3'}

    # plt.figure(1)
    # plt.bar(index, ActMeans, bar_width, alpha=opacity, yerr=ActStddevs, error_kw=error_config)

    # plt.xlabel('Game')
    # plt.ylabel('Average Number of Possible Moves')
    # plt.title('Average Number of Possible Moves by Game')
    # plt.xticks(index + bar_width / 2, ('Peg Solitaire', 'Jasper and Zot'))

    # plt.figure(2)
    # plt.bar(index, RewMeans, bar_width, alpha=opacity, yerr=RewStds, error_kw=error_config)

    # plt.xlabel('Game')
    # plt.ylabel('Average Reward')
    # plt.title('Average Reward Given by Game')
    # plt.xticks(index + bar_width / 2, ('Peg Solitaire', 'Jasper and Zot'))


    # plt.tight_layout()
    # plt.show()

