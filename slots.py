"""This module runs the slots game. This game has three pinwheels that
rotate, but only the top three vanes are visible. Each vane has a symbol
on it. {Match three symbols and win, match two and get money back, etc.}
{Different symbols worth different values for match three.} Game allows
for multiple lines, which opens up the other of the
three vanes to be applicable for matching. Each pinwheel has a 'wild'
multicolored symbol. {Matching three with one wild wins half of the
normal win, two wilds gives your bet back, but matching all three wilds
gives jackpot.} During play, first the first pinwheel will show, then
the second, then the third. 

"""


import textwrap
from random import randint, shuffle
import common
from time import sleep

dict = {
    'player_money': common.dict['player_money'],
    'money_type': common.dict['money_type'],
    'wins': 0,
    'losses': 0,
    'min_bet': 25,
    'middle_bet': 0,
    'left_bet': 0,
    'right_bet': 0
    }

tw = textwrap.TextWrapper()
tw.width = 100
tw.subsequent_indent = '  '
nl = '\n'


def wrap(string):
    string = string % dict
    print tw.fill(string), nl


def rwrap(string):
    """Wrap random string from list in common"""
    wrap(string[randint(0, len(string)-1)])


class Pinwheels(object):
    def __init__(self):
        self.pinwheel = ['wild', 'diamond', 'circle', 'circle', 'square',
                         'square', 'triangle', 'triangle', 'triangle']
        self.pin1 = self.pinwheel[:]
        self.pin2 = self.pinwheel[:]
        self.pin3 = self.pinwheel[:]
        self.first_spin = None
        self.second_spin = None
        self.third_spin = None

    def shuffle_pinwheels(self):
        self.pin1 = self.pinwheel[:]
        self.pin2 = self.pinwheel[:]
        self.pin3 = self.pinwheel[:]
        shuffle(self.pin1)
        shuffle(self.pin2)
        shuffle(self.pin3)

    # noinspection PyMethodMayBeStatic
    def spin_pin(self, pin):
        result = randint(0, len(pin)-1)
        if result == 0:
            left = len(pin) - 1
        else:
            left = result - 1

        if result == len(pin) - 1:
            right = 0
        else:
            right = result + 1
        return [pin[left], pin[result], pin[right]]

    def interpret(self, place):
        if place == 0:
            current_bet = dict['left_bet']
        elif place == 1:
            current_bet = dict['middle_bet']
        elif place == 2:
            current_bet = dict['right_bet']
        else:
            current_bet = 0
        column = [self.first_spin[place], self.second_spin[place],
                  self.third_spin[place]]
        if column.count('wild') == 3:
            return current_bet * 10000
        elif column.count('wild') == 2:
            return current_bet * 2
        elif column.count('diamond') == 3:
            return current_bet * 100
        elif column.count('circle') == 3:
            return current_bet * 50
        elif column.count('square') == 3:
            return current_bet * 10
        elif column.count('triangle') == 3:
            return current_bet * 6
        elif column.count('wild') == 1:
            if column.count('diamond') == 2:
                return current_bet * 50
            elif column.count('circle') == 2:
                return current_bet * 25
            elif column.count('square') == 2:
                return current_bet * 5
            elif column.count('triangle') == 2:
                return current_bet * 3
        return 0
        
    def spin(self):
        if dict['left_bet'] == dict['right_bet'] == dict['middle_bet'] == 0:
            wrap("You have made no bets.")
            return
        self.first_spin = self.spin_pin(self.pin1)
        self.second_spin = self.spin_pin(self.pin2)
        self.third_spin = self.spin_pin(self.pin3)
        self.printout()
        left_winnings = self.interpret(0)
        middle_winnings = self.interpret(1)
        right_winnings = self.interpret(2)
        total_winnings = left_winnings + middle_winnings + right_winnings
        dict['player_money'] += total_winnings
        total_bet = dict['left_bet'] + dict['middle_bet'] + dict['right_bet']
        winnings = total_winnings - total_bet
        if winnings >= 500:
            win()
            wrap("You won %d " % total_winnings + "%(money_type)ss!!!")
        elif total_winnings > 0:
            win()
            wrap("You win %d " % total_winnings + "%(money_type)ss.")
        else:
            loss()
        raw_input(" (Press enter to continue.)\n")
    
    def printout(self):
        data = [self.first_spin, self.second_spin, self.third_spin]
        col_width = 10
        sleep(1.5)
        print ('   |' + "  |".join(word.upper().rjust(col_width)
               for word in data[0])),
        print ' |\n'
        sleep(1)
        print ('   |' + "  |".join(word.upper().rjust(col_width)
               for word in data[1])),
        print ' |\n'
        sleep(1)
        print ('   |' + "  |".join(word.upper().rjust(col_width)
               for word in data[2])),
        print ' |\n'
        sleep(.75)


def win():
    dict['wins'] += 1


def loss():
    dict['losses'] += 1


def bet(which):
    if dict['player_money'] < dict['min_bet']:
        wrap("Sorry, bro. You are out of money. You can't place anymore bets.")
        return
    elif which == 'left':
        dict['left_bet'] += dict['min_bet']
        wrap("You add %(min_bet)d to the left bet.")
    elif which == 'right':
        dict['right_bet'] += dict['min_bet']
        wrap("You add %(min_bet)d to the right bet.")
    elif which == 'middle':
        dict['middle_bet'] += dict['min_bet']
        wrap("You add %(min_bet)d to the middle bet.")
    dict['player_money'] -= dict['min_bet']


def payouts():
    wrap("As you press the touch screen button, the screen changes to display "
         "the payouts for each symbol.")
    print """
        wild      symbol    symbol     -> HALF PAYOUT
        wild      wild      symbol     ->          2x
        triangle  triangle  triangle   ->          6x
        square    square    square     ->         10x
        circle    circle    circle     ->         50x
        diamond   diamond   diamond    ->        100x
        wild      wild      wild       ->      10000x
        """
    raw_input(" (Press enter to continue.)\n")


def play():
    dict['player_money'] = common.dict['player_money']
    wrap("As you insert your moneychip the screen lights up. In the center of "
         "the display are what looks like the tops of three pinwheels. Only "
         "the top three vanes of each are showing. Each vane of each pinwheel "
         "has a small symbol on it. The currently highlighted symbols are "
         "all rainbow colored circles with the word 'WILD' inside.")
    wrap("Below that, there is a box labeled 'Bets', and inside it reads "
         "'Left Bet: 0', 'Middle Bet: 0', and 'Right Bet: 0'. To the left is "
         "a button labeled 'Payouts'.")

    pins = Pinwheels()
    pins.shuffle_pinwheels()
    while True:
        wrap("Do you check (p)ayouts, bet (l)eft, bet (m)iddle, bet (r)ight, "
             "bet (a)ll, (s)pin, or (q)uit?")
        choice = raw_input(">").lower()
        if choice == 'l' or 'left' in choice:
            bet('left')
        elif choice == 'm' or 'middle' in choice:
            bet('middle')
        elif choice == 'r' or 'right' in choice:
            bet('right')
        elif choice == 'a' or 'all' in choice:
            bet('left')
            bet('middle')
            bet('right')
        elif choice == 's' or 'spin' in choice:
            pins.spin()
            dict['left_bet'] = dict['right_bet'] = dict['middle_bet'] = 0
        elif choice == 'p' or 'payout' in choice or 'check' in choice:
            payouts()
        elif choice == 'q' or 'quit' in choice:
            break
        print "    Bets:"
        print ("    Left Bet: %(left_bet)s    Middle Bet: %(middle_bet)s    "
               "Right Bet: %(right_bet)s" % dict)
        wrap("    You have %(player_money)d %(money_type)ss.")
