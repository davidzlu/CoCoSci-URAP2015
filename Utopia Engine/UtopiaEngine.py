import random
import ast
from minigame import *
from copy import deepcopy

possible_minigames = ["Search", "Activation", "Connection"]

# List of valid combinations of constructs and components, and boolean marking if they have been connected.
connection_comb = [["Scrying Lens", "Seal of Balance", "Silver", False],
                   ["Seal of Balance", "Hermetic Mirror", "Silica", False],
                   ["Golden Chassis", "Seal of Balance", "Quartz", False],
                   ["Hermetic Mirror", "Void Gate", "Wax", False],
                   ["Void Gate", "Golden Chassis", "Gum", False],
                   ["Golden Chassis", "Crystal Battery", "Lead", False]]


def random_policy(options, minigame=False):
    """options needs to be a list, for example, a list of actions"""
    if minigame:
        return random.sample(options, 2)
    else:
        return random.choice(options)


def human_player(options, minigame=False):
    print("Your available moves are: ")
    print(options)
    if minigame:  # make two choices
        moves = []
        response = input("Select the first spot where you'd like to place a number: ")
        my_move = ast.literal_eval(response)
        while my_move not in options:
            my_move = ast.literal_eval(input("Please enter a valid move: "))
        move1 = moves.append(my_move)
        response = input("Select the second spot where you'd like to place a number: ")
        my_move = ast.literal_eval(response)
        while my_move not in options:
            my_move = ast.literal_eval(input("Please enter a valid move: "))
        move2 = moves.append(my_move)
        return moves
    my_move = input("Enter the choice you'd like to make: ")
    if type(options[0]) is not str:
        my_move = ast.literal_eval(my_move)
    return my_move


class Enemy:
    def __init__(self, level, attack, hit, area, spirit = False):
        self.level = level
        self.attack = attack
        self.hit = hit
        self.spirit = spirit
        self.area = area


class Area:
    def __init__(self, number, daytracker, construct, component, treasure, searchbox=6):
        self.number = number
        self.daytracker = daytracker
        self.construct = construct
        self.component = component
        self.treasure = treasure
        self.event = None
        self.events = ["Fleeting visions", "Foul Water", "Good Forture", "Active Monsters"]

    def eventcycle(self):
        self.event = random.choice(None, random.choice(self.events))


class Area1(Area):
    def __init__(self):
        Area.__init__(self, 1, [1, 1, 0, 1, 0, 0], "Seal of Balance", "Silver", "Ice Plate")
        self.enemy1 = Enemy(1, [1], [5, 6], self)
        self.enemy2 = Enemy(2, [1], [6], self)
        self.enemy3 = Enemy(3, [1, 2], [6], self)
        self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
        self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self)


class Area2(Area):
    def __init__(self):
        Area.__init__(self, 2, [1, 0, 0, 1, 0, 0], "Hermetic Mirror", "Quartz", "Bracelet of Ios")
        self.enemy1 = Enemy(1, [1, 2], [5, 6], self)
        self.enemy2 = Enemy(2, [1], [6], self)
        self.enemy3 = Enemy(3, [1], [6], self)
        self.enemy4 = Enemy(4, [1, 2, 3], [5, 6], self)
        self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self, True)


class Area3(Area):
    def __init__(self):
        Area.__init__(self, 3, [1, 0, 1, 0, 1, 0], "Void Gate", "Gum", "Shimmering Moonlace")
        self.enemy1 = Enemy(1, [1], [5, 6], self)
        self.enemy2 = Enemy(2, [1, 2], [6], self)
        self.enemy3 = Enemy(3, [1, 2], [6], self)
        self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
        self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self)


class Area4(Area):
    def __init__(self):
        Area.__init__(self, 4, [1, 0, 1, 0, 1, 0], "Golden Chassis", "Silica", "Scale of the Infinity Wurm")
        self.enemy1 = Enemy(1, [1], [5, 6], self)
        self.enemy2 = Enemy(2, [1], [6], self)
        self.enemy3 = Enemy(3, [1, 2], [6], self, True)
        self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
        self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self)


class Area5(Area):
    def __init__(self):
        Area.__init__(self, 5, [1, 0, 0, 1, 0, 0], "Scrying Lens", "Wax", "The Ancient Record")
        self.enemy1 = Enemy(1, [1], [5, 6], self)
        self.enemy2 = Enemy(2, [1], [6], self, True)
        self.enemy3 = Enemy(3, [1, 2], [6], self, True)
        self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
        self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self, True)


class Area6(Area):
    def __init__(self):
        Area.__init__(self, 6, [1, 1, 0, 1, 0, 0], "Crystal Battery", "Lead", "The Molten Shard")
        self.enemy1 = Enemy(1, [1], [5, 6], self)
        self.enemy2 = Enemy(2, [1, 2], [5, 6], self)
        self.enemy3 = Enemy(3, [1, 2, 3], [5, 6], self)
        self.enemy4 = Enemy(4, [1, 2, 3], [6], self, True)
        self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self, True)


class GameBoard:

    tpm = {}

    def __init__(self):
        self.area1 = Area1()
        self.area2 = Area2()
        self.area3 = Area3()
        self.area4 = Area4()
        self.area5 = Area5()
        self.area6 = Area6()
        self.possible_areas = {'Area 1': self.area1, 'Area 2': self.area2, 'Area 3': self.area3,
                               'Area 4': self.area4, 'Area 5' : self.area5, 'Area 6' : self.area6}
        self.tools = ["Dowsing Rod", "Paralysis Wand", "Focus Charm"]
        self.construct = {}  # dictionary: key->name of construct, value->activation pts
        self.treasure = []
        self.hit = 6
        self.component = {}  # dictionary: key->name of component, value->numbers in hold
        self.skull = 8
        self.day = 0
        self.end_day = 22  # when self.day = self.end_day - self.skull, game ends
        self.eventdays = [1, 4, 7, 10, 13, 16, 19]
        self.godhand = 0  # energy in god hand device
        self.finalAct = 0
        self.numConnected = 0
        self.wastebasket = []
        self.activationStarted = False
        self.score = 36  # unused equipment = 10 * 3, hitpoint = 6 * 1

    def transition_prob_matrix(self):
        return self.tpm

    def transition_prob_vector(self, action):
        return

    def next_states(self, action):
        return

    def eventcycle(self):
        if self.day in self.eventdays:
            self.area1.eventcycle()
            self.area2.eventcycle()
            self.area3.eventcycle()
            self.area4.eventcycle()
            self.area5.eventcycle()
            self.area6.eventcycle()

    def take_damage(self, n):
        self.hit = self.hit - n
        self.score = self.score - n

    def combat(self, enemy):
        damage_taken = 0
        self_dice = 0
        enemy_dice = 0
        while self_dice not in enemy.hit:
            result = roll_dice(2)
            self_dice = result[0]
            enemy_dice = result[1]
            if enemy_dice in enemy.attack:
                damage_taken += 1
        self.take_damage(damage_taken)
        # get_item_or_not = roll_dice(1)
        # if get_item_or_not <= enemy.level:
        # 	if enemy.level == 5:
        # 		return enemy.area.treasure
        # 	else:
        # 		return enemy.area.component

    def score(self):
        score = 0
        for x in self.construct:
            if self.construct[x] >= 999:
                score += 5
        score += 10 * len(self.construct)

    def rest(self):
        if "Void Gate" in self.construct and self.construct["Void Gate"] >= 999:
            self.hit += 2
        else:
            self.hit += 1
        self.day += 1

    def merge_results(self, states_visited, actions_taken, rewards_gained, legal_actions, results):
        """Helper function for play. Appends results from minigame to lists tracking all results.
        """
        states_visited += results[0]
        actions_taken += results[1]
        rewards_gained += results[2]
        legal_actions += results[3]

    def can_connect(self):
        """Helper function for play, returns True if at least 2 constructs and at least 1 component
        """
        return (len(self.construct) >= 2) and (len(self.component) != 0)

    def get_constructs_and_components_to_connect(self, strategy):
        """Helper function for play. Returns 2 constructs and 1 component for Connection.
        """
        constructs = list(self.construct.keys())
        construct_to_connect1 = strategy(constructs)
        constructs.remove(construct_to_connect1)
        construct_to_connect2 = strategy(constructs)
        component_to_connect = strategy(list(self.component.keys()))

        return construct_to_connect1, construct_to_connect2, component_to_connect

    def valid_connection(self, construct1, construct2, component):
        """Helper function for play. Manages the check for a valid combination of constructs
           and components.
        """
        connectable = False
        set_to_connect = []
        for comb in connection_comb:
            if construct1 in comb and construct2 in comb and component == comb[2]:
                connectable = True
                set_to_connect = comb
                connection_comb.remove(comb)
                connection_comb.remove([comb[1], comb[0], comb[2]])
        return connectable, set_to_connect

    def start_final_activation(self, strategy, actions_taken):
        """Helper function for play. Takes care of starting final activation.
        """
        if not self.activationStarted:
            hitpts_to_spend = strategy(list(range(self.hit + 1)))
            actions_taken.append(hitpts_to_spend)
            self.hit -= hitpts_to_spend
            self.finalAct -= hitpts_to_spend
            self.activationStarted = True
            
    def play(self, strategy):
        states_visited = [deepcopy(self)] # Sequence of states visited during a game
        actions_taken = []  # Sequential actions taken during a game
        rewards_gained = []  # Sequence of rewards obtained during a game
        legal_actions = []
        self.activationStarted = False
        global possible_minigames
        global connection_comb
        
        while self.day < self.end_day - self.skull:
            action_to_take = strategy(possible_minigames)
            actions_taken.append(action_to_take)
            if action_to_take == "Search":
                search_game = Search()
                search_area = strategy(sorted(self.possible_areas.keys()))
                search_area = self.possible_areas[search_area]
                if len(search_area.daytracker) == 0:
                    self.day += 1
                else:
                    self.day += search_area.daytracker.pop()
                outcome, results = search_game.play(strategy)
                self.merge_results(states_visited, actions_taken, rewards_gained, legal_actions, results)
                if outcome == 0:  # find construct and activate: natural zero
                    self.score += 20
                    if search_area.construct is None:
                        if search_area.component in self.component:
                            self.component[search_area.component] += 2
                        else:
                            self.component[search_area.component] = 2
                    else:
                        print("You found a construct! You got the " + search_area.construct)
                        print("It's already activated!")
                        self.construct[search_area.construct] = 999  # automatically activate
                        self.score += 15
                        search_area.construct = None
                elif 1 <= outcome <= 10:  # find construct
                    if search_area.construct is None:
                        if search_area.component in self.component:
                            self.component[search_area.component] += 2
                        else:
                            self.component[search_area.component] = 2
                    else:
                        print("You found a construct! You got the " + search_area.construct)
                        self.construct[search_area.construct] = 0
                        self.score += 10
                        search_area.construct = None
                elif 11 <= outcome <= 99:  # find component
                    if search_area.component in self.component:
                        self.component[search_area.component] += 1
                    else:
                        self.component[search_area.component] = 1
                elif outcome in range(100, 200) or outcome in range(-100, 0):  # combat lv1
                    self.combat(search_area.enemy1)
                    get_item_or_not = roll_dice(1)[0]
                    if get_item_or_not <= 1:
                        if search_area.component in self.component:
                            self.component[search_area.component] += 1
                        else:
                            self.component[search_area.component] = 1
                elif outcome in range(200, 300) or outcome in range(-200, -100):  # combat lv2
                    self.combat(search_area.enemy2)
                    get_item_or_not = roll_dice(1)[0]
                    if get_item_or_not <= 2:
                        if search_area.component in self.component:
                            self.component[search_area.component] += 1
                        else:
                            self.component[search_area.component] = 1
                elif outcome in range(300, 400) or outcome in range(-300, -200):  # combat lv3
                    self.combat(search_area.enemy3)
                    get_item_or_not = roll_dice(1)[0]
                    if get_item_or_not <= 3:
                        if search_area.component in self.component:
                            self.component[search_area.component] += 1
                        else:
                            self.component[search_area.component] = 1
                elif outcome in range(400, 500) or outcome in range(-400, -300):  # combat lv4
                    self.combat(search_area.enemy4)
                    get_item_or_not = roll_dice(1)[0]
                    if get_item_or_not <= 4:
                        if search_area.component in self.component:
                            self.component[search_area.component] += 1
                        else:
                            self.component[search_area.component] = 1
                elif outcome in range(500, 556) or outcome in range(-555, -400):  # combat lv5
                    self.combat(search_area.enemy5)
                    get_item_or_not = roll_dice(1)[0]
                    if get_item_or_not <= 5:
                        if search_area.treasure not in self.treasure:
                            self.treasure.append(search_area.treasure)
                            self.score += 10
                if self.hit < 0:  # run out of life
                    break
                elif self.hit == 0:  # rest till restore
                    if "Void Gate" in self.construct and self.construct["Void Gate"] >= 999:
                        self.rest()
                        self.rest()
                        self.rest()
                    else:
                        self.rest()
                        self.rest()
                        self.rest()
                        self.rest()
                        self.rest()
                        self.rest()
            elif action_to_take == "Activation":  # activation
                if len(self.construct) != 0:  # no construct can be activated
                    construct_to_activate = strategy(list(self.construct.keys()))
                    # elif self.construct[construct_to_activate] >= 200 and self.construct[construct_to_activate] < 999:
                    # # haven't been activated and used up 2 chances
                    # 	self.construct[construct_to_activate] = 999
                    # elif self.construct[construct_to_activate] < 999:
                    # 	activation_game = Activation()
                    # 	outcome = activation_game.play(strategy, self.construct[construct_to_activate])
                    # 	self.take_damage(outcome[1])
                    # 	self.construct[construct_to_activate] = outcome[0]
                    # 	if outcome[0] != 999:
                    # 		self.construct[construct_to_activate] += 100
                    if self.construct[construct_to_activate] == 0:
                        self.day += 1
                        activation_game = Activation()
                        outcome, results = activation_game.play(strategy, self.construct[construct_to_activate])
                        self.construct[construct_to_activate] = outcome[0]
                        self.take_damage(outcome[1])
                        self.merge_results(states_visited, actions_taken, rewards_gained, legal_actions, results)
                        if outcome[0] < 4:
                            self.day += 1
                            activation_game2 = Activation()
                            outcome2 = activation_game2.play(strategy, self.construct[construct_to_activate])
                            self.construct[construct_to_activate] += outcome2[0]
                            self.take_damage(outcome2[1])
                            self.merge_results(states_visited, actions_taken, rewards_gained, legal_actions, results)
                        if self.construct[construct_to_activate] < 4:
                            self.day += 1
                        self.construct[construct_to_activate] = 999
                        self.score += 5  # activated
            elif action_to_take == "Connection":
                if self.can_connect():
                    construct_to_connect1, construct_to_connect2, component_to_connect = \
                        self.get_constructs_and_components_to_connect(strategy)
                    connectable, set_to_connect = self.valid_connection(construct_to_connect1, 
                                                                      construct_to_connect2, 
                                                                      component_to_connect)
                    if connectable:
                        connection_game = Connection(self)
                        link_num, results = connection_game.play(strategy)
                        self.merge_results(states_visited, actions_taken, rewards_gained, legal_actions, results)
                        if link_num >= 0:
                            self.finalAct += link_num
                            set_to_connect[3] = True  # these components are connected
                            self.numConnected += 1
                            self.score += 5
                            if self.numConnected == 6:
                                possible_minigames = ["Final Activation"]
            elif action_to_take == "Final Activation":
                self.start_final_activation(strategy, actions_taken)
                final_game = FinalActivation(self.finalAct)
                activated, results = final_game.play(strategy)
                self.merge_results(states_visited, actions_taken, rewards_gained, legal_actions, results)
                if activated:
                    print("You've activated the Utopia Engine and saved the world!")
                    self.score += 50
                    self.score += (self.end_day - self.skull - self.day) * 5
                    break
                else:
                    self.day += 1
                    self.hit -= 1

            states_visited.append(deepcopy(self))

        return states_visited, actions_taken, rewards_gained, legal_actions


if __name__ == '__main__':
    ue = GameBoard()
    #sts, act, rwd, lAct = ue.play(random_policy)