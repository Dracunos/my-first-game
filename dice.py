"""Dice game module. The dice game is a group game, played with
yourself and three others. Everyone must ante in or leave the game.
Betting and rolling is clockwise, starting with winner, order is
you, player1, player2, and then player3. Each player starts with a
multiple of 50 cash, bets are done by 50s, each player has one chance
to raise each round, so everyone starts at 50, max of four raises, then
the rest have to match the pot or 'fold'. First bet and roll goes to
winner. Two dice, 1 thru 5, then sixth is 'gloob'. Rolling a gloob
automatically means you lose, rolling two gloobs means you automatically
win; no more rolls. Rolling anything under a 6 (1-5) means pass. Once
you roll a 6-10 that is your keep number, no more rolls. the last person
to roll the lowest keep number wins. IE two players, A rolls a 6, then
B rolls a 6, then A rolls a 6, A wins the pot.
"""

import textwrap
from random import randint
import common
from time import sleep

dict = {
    'player_money': common.dict['player_money'],
    'money_type': common.dict['money_type'],
    'wins': 0,
    'losses': 0,
    'min_bet': 50,
    'bet': 0
    }

tw = textwrap.TextWrapper()
tw.width = 100
tw.subsequent_indent = '  '
nl = '\n'


class Game(object):
    """This class runs the game."""

    def __init__(self, name1, name2, name3):
        self.players = [
            {'name': name1, 'cash': randint(10, 20)*50, 'fold': False,
             'out': False, 'keep': None, 'bet': 0, 'aggro': randint(1, 3)},

            {'name': name2, 'cash': randint(10, 20)*50, 'fold': False,
             'out': False, 'keep': None, 'bet': 0, 'aggro': randint(1, 3)},

            {'name': name3, 'cash': randint(10, 20)*50, 'fold': False,
             'out': False, 'keep': None, 'bet': 0, 'aggro': randint(1, 3)},

            {'name': 'player', 'fold': False, 'out': False, 'keep': None,
             'bet': 0}
            ]

        self.dict = dict
        self.dict['player_money'] = common.dict['player_money']
        self.first = 3  # 0-2 is opponent 1-3, 3 is player

    def wrap(self, string, newline=nl):
        string = string.format(
            dict, self.players[0]['name'],
            self.players[1]['name'], self.players[2]['name']
            )
        print tw.fill(string), newline

    def rwrap(self, string):
        """Wrap random string from list in common"""
        self.wrap(string[randint(0, len(string)-1)])

    def start(self):
        self.wrap("The game begins.")
        self.match()

    def match(self):
        while not self.players[3]['out']:
            self.reset()
            if self.dict['player_money'] < dict['min_bet']:
                self.wrap("You do not have enough money to continue.")
                break
            self.ante_in()

            self.wrap("Betting begins.")
            self.bet()
            if self.players[3]['out']:
                    break
            still_in = []
            for i in self.players:
                if i['fold'] or i['out']:
                    still_in.append(False)
                else:
                    still_in.append(True)
            if still_in.count(False) == 3:
                self.winner(still_in.index(True))
                continue

            self.wrap("Betting ends. The current bet is {0[bet]} "
                      "{0[money_type]}s.")
            sleep(1)
            winner = self.roll()
            self.winner(winner)
            choice = raw_input(" (Enter 'q' to quit.)").lower()
            if choice == 'q' or 'quit' in choice:
                self.wrap("You quit the game and gather up your remaining "
                          "chips.")
                break
        self.wrap("You leave the table.")

    def reset(self):
            self.players[0]['bet'] = 0
            self.players[0]['keep'] = None
            self.players[0]['fold'] = False

            self.players[1]['bet'] = 0
            self.players[1]['keep'] = None
            self.players[1]['fold'] = False

            self.players[2]['bet'] = 0
            self.players[2]['keep'] = None
            self.players[2]['fold'] = False

            self.players[3]['bet'] = 0
            self.players[3]['keep'] = None
            self.players[3]['fold'] = False

            self.dict['bet'] = 0

    def ante_in(self):
        if self.players[0]['out']:
            pass
        elif self.players[0]['cash'] < dict['min_bet']:
            self.players[0]['out'] = True
            self.wrap("{1} takes its remaining chips and leaves the "
                      "table.", '')
        else:
            self.players[0]['bet'] += dict['min_bet']
            self.dict['bet'] += dict['min_bet']
            self.wrap("{1} antes in.", '')
            self.players[0]['cash'] -= dict['min_bet']

        if self.players[1]['out']:
            pass
        elif self.players[1]['cash'] < dict['min_bet']:
            self.players[1]['out'] = True
            self.wrap("{2} takes its remaining chips and leaves the "
                      "table.", '')
        else:
            self.players[1]['bet'] += dict['min_bet']
            self.dict['bet'] += dict['min_bet']
            self.wrap("{2} antes in.", '')
            self.players[1]['cash'] -= dict['min_bet']

        if self.players[2]['out']:
            pass
        elif self.players[2]['cash'] < dict['min_bet']:
            self.players[2]['out'] = True
            self.wrap("{3} takes its remaining chips and leaves the "
                      "table.", '')
        else:
            self.players[2]['bet'] += dict['min_bet']
            self.dict['bet'] += dict['min_bet']
            self.wrap("{3} antes in.", '')
            self.players[2]['cash'] -= dict['min_bet']

        self.dict['bet'] += dict['min_bet']
        self.dict['player_money'] -= dict['min_bet']
        self.players[3]['bet'] += dict['min_bet']
        self.wrap("You add your ante. You have {0[player_money]} "
                  "{0[money_type]} left.")

    def bet(self):
        bet = 0
        better = self.first
        while bet != 4:
            bet += 1
            if better == 3:
                betted = self.player_bet()
                if self.players[3]['out']:
                    return
            else:
                sleep(1)
                betted = self.ai_bet(better)
            if betted:
                self.match_bet(better)
                if self.players[3]['out']:
                    return
            if better == 3:
                better = 0
            else:
                better += 1

    def ai_bet(self, better):
        if self.players[better]['out'] or self.players[better]['fold']:
            return False
        elif (self.players[better]['aggro'] >= randint(1, 8) and
                self.players[better]['cash'] >= dict['min_bet']):
            self.wrap(self.players[better]['name'] + " raises the bet by "
                      "{0[min_bet]} {0[money_type]}s.")
            self.players[better]['bet'] += dict['min_bet']
            self.dict['bet'] += dict['min_bet']
            self.players[better]['cash'] -= dict['min_bet']
            return True
        else:
            self.wrap(self.players[better]['name'] + " checks.")
            return False

    def player_bet(self):
        if self.players[3]['fold']:
            return False
        else:
            if self.dict['player_money'] < dict['min_bet']:
                self.wrap("You do not have enough money to raise.")
                return False
            self.wrap("Do you wish to raise?")
            while True:
                choice = raw_input('>').lower()
                if choice == 'y' or 'yes' in choice:
                    self.dict['bet'] += dict['min_bet']
                    self.dict['player_money'] -= dict['min_bet']
                    self.players[3]['bet'] += dict['min_bet']
                    self.wrap("You raise the bet by {0[min_bet]} "
                              "{0[money_type]}s. You have {0[player_money]} "
                              "{0[money_type]}s left.")
                    return True
                elif choice == 'n' or 'no' in choice:
                    self.wrap("You check.")
                    return False

    def match_bet(self, raiser):
        better = raiser
        if better == 3:
            better = 0
        else:
            better += 1
        while self.players[better]['bet'] < self.players[raiser]['bet']:
            if self.players[better]['out'] or self.players[better]['fold']:
                pass
            elif better == 3:
                if self.dict['player_money'] < dict['min_bet']:
                    self.wrap("You do not have enough money to continue.")
                    self.players[3]['out'] = True
                    return
                self.wrap("Do you (c)all, (f)old, or (q)uit?", '')
                while True:
                    choice = raw_input('>').lower()
                    if choice == 'c' or 'call' in choice:
                        self.dict['bet'] += dict['min_bet']
                        self.dict['player_money'] -= dict['min_bet']
                        self.players[3]['bet'] += dict['min_bet']
                        self.wrap("You call. You add {0[min_bet]} "
                                  "{0[money_type]}s to the pot. You have "
                                  "{0[player_money]} {0[money_type]}s "
                                  "left.", '')
                        break
                    elif choice == 'f' or 'fold' in choice:
                        self.players[3]['fold'] = True
                        self.wrap("You fold.")
                        break
                    elif choice == 'q' or 'quit' in choice:
                        self.wrap("You quit the game.")
                        self.players[3]['out'] = True
                        return

            else:
                if self.players[better]['fold']:
                    pass
                elif self.players[2]['cash'] < dict['min_bet']:
                    sleep(0.5)
                    self.players[better]['fold'] = True
                    self.wrap(self.players[better]['name'] + " folds.", '')
                elif randint(1, 50) == 13:
                    sleep(0.5)
                    self.players[better]['fold'] = True
                    self.wrap(self.players[better]['name'] + " folds.", '')
                else:
                    sleep(0.5)
                    self.wrap(self.players[better]['name'] + " calls. It adds "
                              "{0[min_bet]} {0[money_type]}s to the bet.", '')
                    self.players[better]['bet'] += dict['min_bet']
                    self.dict['bet'] += dict['min_bet']
                    self.players[better]['cash'] -= dict['min_bet']

            if better == 3:
                better = 0
            else:
                better += 1
        print '\n'

    def roll(self):
        next_round = True
        roller = self.first
        lowest_keep = (20, 20)  # tuple with index of winner and it's keep
        while next_round:
            if self.players[roller]['out']:
                pass
            elif self.players[roller]['fold']:
                if roller == 3:
                    self.wrap("You are out this round. You skip your roll.")
                else:
                    self.wrap(self.players[roller]['name'] + " is out this "
                              "round. He skips his roll.")
                raw_input(" (Press enter to continue.)")
            elif self.players[roller]['keep']:
                if roller == 3:
                    self.wrap("You already have a keep of " +
                              str(self.players[roller]['keep']) + ".")
                else:
                    self.wrap(self.players[roller]['name'] + " already has a "
                              "keep of "
                              + str(self.players[roller]['keep']) + ".")
                raw_input(" (Press enter to continue.)")
            elif roller == 3:
                self.wrap("It's your turn. You take the two dice from the "
                          "table.")
                raw_input(" (Press enter to roll.)")
                self.wrap("You roll the dice.")
                sleep(1)
                result = self.player_roll()  # 'fold','pass',keep number, win
                if result == 'fold':
                    self.wrap('"Gloob! Gloob! Gloob!" your opponents chant. '
                              "You automatically lose this round.")
                    self.players[roller]['fold'] = True
                elif result == 'win':
                    self.wrap('"Gloob! Gloob! Gloob!" your opponents chant. '
                              "You automatically WON this round!")
                    return roller
                elif result == 'pass':
                    self.wrap("You didn't get a keep. You pass this round.")
                else:
                    self.players[roller]['keep'] = result
                    self.wrap("Your keep is " + str(result) + ".")
                    if lowest_keep[1] >= result:
                        self.wrap("This is the current lowest keep.")
                        lowest_keep = (roller, result)
                raw_input(" (Press enter to continue.)")

            else:
                self.wrap(self.players[roller]['name'] + " picks up the dice "
                          "and rolls them.")
                sleep(1)
                result = self.ai_roll(roller)
                if result == 'fold':
                    self.wrap('"Gloob! Gloob! Gloob!" you join in the chant. '
                              + self.players[roller]['name'] + " automatically"
                              " loses this round.")
                    self.players[roller]['fold'] = True
                elif result == 'win':
                    self.wrap('"Gloob! Gloob! Gloob!" you join in the chant. '
                              + self.players[roller]['name'] + " automatically"
                              " WINS this round.")
                    return roller
                elif result == 'pass':
                    self.wrap(self.players[roller]['name'] + " didn't get a "
                              "keep. It passes.")
                else:
                    self.players[roller]['keep'] = result
                    self.wrap(self.players[roller]['name'] + " got a keep of "
                              "" + str(result) + ".")
                    if lowest_keep[1] >= result:
                        self.wrap("This is the current lowest keep.")
                        lowest_keep = (roller, result)
                raw_input(" (Press enter to continue.)")

            interp = self.interpret(lowest_keep)
            if interp == 'continue':
                pass
            else:
                return interp

            if roller == 3:
                roller = 0
            else:
                roller += 1

    def ai_roll(self, index):
        die1 = self.roll_die()
        die2 = self.roll_die()
        self.wrap(self.players[index]['name'] + " rolled a " + str(die1) + " "
                  "and a " + str(die2) + ".")
        if die1 == 'GLOOB' and die2 == 'GLOOB':
            return 'win'
        elif die1 == 'GLOOB' or die2 == 'GLOOB':
            return 'fold'
        elif die1 + die2 > 5:
            return die1 + die2
        else:
            return 'pass'

    def player_roll(self):
        die1 = self.roll_die()
        die2 = self.roll_die()
        self.wrap("You rolled a " + str(die1) + " and a " + str(die2) + ".")
        if die1 == 'GLOOB' and die2 == 'GLOOB':
            return 'win'
        elif die1 == 'GLOOB' or die2 == 'GLOOB':
            return 'fold'
        elif die1 + die2 > 5:
            return die1 + die2
        else:
            return 'pass'

    # noinspection PyMethodMayBeStatic
    def roll_die(self):
        roll = randint(1, 6)
        if roll == 6:
            return 'GLOOB'
        else:
            return roll

    def interpret(self, lowest_keep):
        still_in = []
        for i in self.players:
            if i['fold'] or i['out']:
                still_in.append(False)
            else:
                still_in.append(True)
        if still_in.count(False) == 3:
            return still_in.index(True)
        for i in self.players:
            if not i['keep'] and not i['out'] and not i['fold']:
                return 'continue'
        return lowest_keep[0]

    def winner(self, index):
        if index == 3:
            self.dict['player_money'] += self.dict['bet']
            self.wrap("You won the {0[bet]} {0[money_type]} bet! You have "
                      "{0[player_money]} {0[money_type]}s.")
            self.dict['wins'] += 1
            self.first = 3
        else:
            self.players[index]['cash'] += self.dict['bet']
            self.wrap(self.players[index]['name'] + " wins the {0[bet]} "
                      "{0[money_type]} pot! You have "
                      "{0[player_money]} {0[money_type]}s.")
            self.dict['losses'] += 1
            self.first = index
