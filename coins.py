"""This module runs the coins game. Seeing as how only heads or tails
is possible, no AI needed. Bets will be high, 100 each player for each
round. Randomly, the 'three-sided coin' will be invoked. It will be
treated like a normal coin except that if it lands on the third side,
nobody wins and each player will add 200 to the pot, and the same coin
will be flipped again, potentially adding up to a very huge pot,
potentially an all-in situation. The opponent will have a random
quit chance variable.

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
    'min_bet': 100,
    'bet': 0
    }

tw = textwrap.TextWrapper()
tw.width = 100
tw.subsequent_indent = '  '
nl = '\n'


class Game(object):
    """This class runs the game."""
    
    def __init__(self, name):
        self.name = name
        self.dict = dict
        self.dict['player_money'] = common.dict['player_money']
        self.quit_var = randint(2, 4)
        self.all_in = False
        self.ai_win = 0
        self.ai_loss = 0
        self.ai_quits = False
        self.tscoin = False
        self.end = False
    
    def wrap(self, string):
        string = string.format(dict, self.name, dict['min_bet']*2)
        print tw.fill(string), nl

    def rwrap(self, string):
        """Wrap random string from list in common"""
        self.wrap(string[randint(0, len(string)-1)])
    
    def ai_quit(self):
        if self.ai_loss - self.ai_win > self.quit_var:
            if randint(1, 5) == 1:
                self.ai_quits = True
    
    def start(self):
        self.wrap(common.game_begins)
        sleep(1)
        self.match()
    
    def match(self):
        self.dict['bet'] = 0
        choose = 'player'
        third_side = False
        while not self.ai_quits and not self.all_in and not self.end:
            if self.dict['player_money'] < self.dict['min_bet']:
                self.wrap(common.no_money)
                break
            elif not third_side:
                self.bet()
                self.wrap(common.buy_in)
            else:
                self.bet()
                self.bet()
                if self.all_in:
                    self.wrap(common.all_in)
                else:
                    self.wrap(common.third_side_bet)
            self.wrap(common.current_pot)
            
            if choose == 'player':
                self.wrap("(H)eads or (t)ails?")
                while True:
                    choice = raw_input('>').lower()
                    if choice == 'h' or 'head' in choice:
                        self.wrap("You select 'heads' on the console.")
                        heads = 'player'
                        break
                    elif choice == 't' or 'tail' in choice:
                        self.wrap("You select 'tails' on the console.")
                        heads = 'opponent'
                        break
            elif choose == 'opponent':
                sleep(1.4)
                if randint(0, 1) == 0:
                    self.wrap("{} chooses 'heads'.".format(self.name))
                    heads = 'opponent'
                else:
                    self.wrap("{} chooses 'tails'.".format(self.name))
                    heads = 'player'
            sleep(1)
            
            if randint(1, 2) == 2:
                self.tscoin = True
            
            result = self.flip()
            if self.tscoin:
                self.rwrap(common.ts_coin)
            else:
                self.rwrap(common.coin_drop)
            sleep(1.6)
            if result == 0:
                print "The coin lands on HEADS."
                if heads == 'player':
                    self.win()
                    choose = 'opponent'
                else:
                    self.lose()
                    choose = 'player'
                self.dict['bet'] = 0
                self.tscoin = False
                third_side = False
            elif result == 1:
                print "The coin lands on TAILS."
                if heads == 'player':
                    self.lose()
                    choose = 'player'
                else:
                    self.win()
                    choose = 'opponent'
                self.dict['bet'] = 0
                self.tscoin = False
                third_side = False
            elif result == 2:
                self.rwrap(common.third_side)
                third_side = True
                
            else:
                print 'Error'
                break
            
            self.wrap(" (Enter 'q' to quit.)")
            choice = raw_input('>').lower()
            if choice == 'q' or 'quit' in choice:
                break
            self.ai_quit()
        if self.ai_quits:
            self.rwrap(common.ai_quits)
    
    def flip(self):
        if self.tscoin:
            return randint(0, 2)
        else:
            return randint(0, 1)  # 0: heads, 1: tails
    
    def bet(self):
        if not self.all_in:
            if self.dict['player_money'] <= self.dict['min_bet']:
                value = self.dict['player_money']
                self.dict['bet'] += self.dict['player_money'] * 2
                self.dict['player_money'] = 0
                self.all_in = True
                return value
            else:
                self.dict['bet'] += self.dict['min_bet'] * 2
                self.dict['player_money'] -= self.dict['min_bet']
                return self.dict['bet']
    
    def win(self):
        if self.all_in:
            self.all_in = False
        self.dict['player_money'] += self.dict['bet']
        self.dict['wins'] += 1
        self.ai_loss += 1
        self.wrap(common.winner)
        
    def lose(self):
        self.dict['losses'] += 1
        self.ai_win += 1
        self.wrap(common.loser)
