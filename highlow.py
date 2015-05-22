"""This module is used to create a higher/lower card game.
The rules are simple, the loser starts the bet, two cards are drawn,
higher card wins.

Attributes:
    player_money    Starting money of game
    money_type      Singular monetary unit name
    ante            ante and betting increment
    num_card        List of two numbers, high number and low number
    face_cards      face card list from highest to lowest
    suit_cards      list of card suits from high to low
"""


from random import randint, shuffle
import common
from time import sleep

# Set the starting money of the player.
player_money = 1000
money_type = 'dollar'
# noinspection PyBroadException
try:
    player_money = common.dict['player_money']
    money_type = common.dict['money_type']
except:
    pass

dict = {'wins': 0, 'losses': 0}

# Default 10 unit ante and bet increments
ante = 10

# Numbered card list, max, min, for numbered cards, default 10, 2
num_cards = [10, 2]

# List of face card names, default normal deck,
# ordered high to low
face_cards = ['ace', 'king', 'queen', 'jack']

# List of card suits, plural, default normal deck, ordered high to low
suit_cards = ['spades', 'hearts', 'diamonds', 'clubs']


# Create rank list of all cards
def make_card_list():

    num_card_list = []
    for i in range(num_cards[0] - num_cards[1] + 1):
        num_card_list.append(i + num_cards[1])

    num_card_list = num_card_list[::-1]

    card_list = face_cards[:]

    for i in range(len(num_card_list)):
        card_list.append(str(num_card_list[i]))
    return card_list


# Now create a list of every card in a standard deck,
# ordered from the highest card (eg A spades) to the lowest (eg 2 clubs)
def make_deck():

    card_list = make_card_list()

    deck_list = []
    for i in range(len(card_list)):

        for q in range(len(suit_cards)):
            deck_list.append(card_list[i] + ' of ' + suit_cards[q])
    return deck_list


class CardAI(object):
    """Using very simple AI, will randomly raise or call on bet
    After NET losing random number of games over quit_var will quit in
    20% chance increments.

    Attributes:
        name      Opponent name
        quit_var  How many net losses before chance of quitting
    """

    def __init__(self, name, quit_var):
        self.name = name
        self.quit_var = quit_var
        self.losses = 0
        self.wins = 0
        self.net_losses = 0
        self.quit_chance = 0
        self.game = TheGame(self)

        chance = randint(1, 3)
        self.bet_aggro = chance

    def quit_odds(self):

        self.net_losses = self.losses - self.wins
        if self.net_losses > self.quit_var:
            self.quit_chance = (self.net_losses - self.quit_var
                                ) * 20
        else:
            self.quit_chance = 0

    def lost_game(self):

        self.losses += 1
        self.quit_odds()

        if randint(1, 100) <= self.quit_chance:
            return 'quit'

    def won_game(self):

        self.wins += 1
        self.quit_odds()

    def bet(self):

        card_rank = make_deck().index(self.game.ai_card)
        bet_aggro = self.bet_aggro
        if self.quit_chance >= 10:
            bet_aggro = 1
        if card_rank < 12:
            bet_aggro = 3
        if card_rank == 0:
            return 'bet'
        if card_rank > 36:
            bet_aggro = 1
        if card_rank > 43:
            return 'pass'

        chance = randint(1, 100)
        if chance <= (25 * bet_aggro):
            return 'bet'
        else:
            return 'pass'


class TheGame(object):
    """ This is the actual game class, it need designate who draws first in
    each match (player first match, then loser), operate the betting
    system(rotating starting with first drawer), pop cards from the deck,
    designate a winner, give money to player if they win, shuffle deck
    once empty, and start over.

    Attributes:
        self.opponent   CardAI object (opponent class)
        self.game_dict  Dictionary with values to put into strings
        self.deck       This is the deck of cards list
    """

    def __init__(self, opponent):
        self.opponent = opponent
        global player_money
        player_money = common.dict['player_money']
        self.game_dict = {
            'name': self.opponent.name, 'ante': ante, 'dollar': money_type,
            'money': player_money, 'bet': 0, 'ante2': ante*2
            }
        self.first_draw = 'player'
        self.deck = make_deck()
        self.player_card = None
        self.ai_card = None
        self.ai_quits = False
        self.ended = False

    def pprint(self, string):
        print (string[randint(0, len(string)-1)] %
               self.game_dict)

    def lost_money(self, amount):
        global player_money
        player_money -= amount
        self.game_dict['money'] -= amount

    def won_money(self, amount):
        global player_money
        player_money += amount
        self.game_dict['money'] += amount
        dict['wins'] += 1

    def add_bet(self, amount):
        self.game_dict['bet'] += amount

    def start(self):
        self.ended = False
        self.pprint(common.game_start)
        sleep(0.5)
        self.shuffle()
        self.match_start()

    def match_start(self):
        while True:
            if player_money < ante:
                print "You do not have enough money to continue."
                self.end_game()
            if self.ended:
                return
            self.add_bet(ante*2)
            self.lost_money(ante)
            self.pprint(common.ante_in)
            self.draw()
            self.bet()
            if self.ended:
                self.pprint(common.game_end)
                return
            else:
                self.pprint(common.bet_end)
                self.compare_cards()

    def player_won(self):
        self.won_money(self.game_dict['bet'])
        self.game_dict['bet'] = 0
        if self.opponent.lost_game() == 'quit':
            self.ai_quits = True
        self.first_draw = 'opponent'

    def opponent_won(self):
        self.game_dict['bet'] = 0
        self.opponent.won_game()
        self.first_draw = 'player'
        dict['losses'] += 1

    def bet(self):
        bet_round = 0
        bet_continue = True
        first_round = True
        first_called = False
        if randint(1, 4) == 4:
            self.pprint(common.bet_strings)

        if self.first_draw == 'player':
            betting = 'player'
        else:
            betting = 'opponent'

        while bet_continue and not self.ended:

            if betting == 'player':
                while True:
                    if first_round:
                        sleep(0.6)
                        print 'Do you wish to (c)heck, (r)aise, or (q)uit?'
                    else:
                        sleep(0.6)
                        print 'Do you wish to (c)all, (r)aise, or (q)uit?'
                    choice = raw_input('>')
                    if choice.lower() == 'r' or choice.lower() == 'raise':
                        if not first_round:
                            if player_money < ante*2:
                                bet_continue = False
                                print "You go all in."
                                self.add_bet(player_money)
                                self.lost_money(player_money)
                                break
                            self.pprint(common.raise2)
                            self.add_bet(ante*2)
                            self.lost_money(ante*2)
                        else:
                            if player_money < ante*2:
                                bet_continue = False
                                print "You go all in."
                                self.add_bet(player_money)
                                self.lost_money(player_money)
                                break
                            self.pprint(common.raise1)
                            self.add_bet(ante)
                            self.lost_money(ante)
                            first_round = False
                        betting = 'opponent'
                        break
                    elif (choice.lower() == 'c' or choice.lower() == 'call' or
                            choice.lower() == 'check'):
                        if not first_round:
                            if player_money < ante*2:
                                bet_continue = False
                                print "You go all in."
                                self.add_bet(player_money)
                                self.lost_money(player_money)
                                break
                            self.pprint(common.call2)
                            self.add_bet(ante)
                            self.lost_money(ante)
                            bet_continue = False
                        else:
                            self.pprint(common.call1)
                            if first_called:
                                bet_continue = False
                            first_called = True
                        betting = 'opponent'
                        break
                    elif choice.lower() == 'q' or choice.lower() == 'quit':
                        self.opponent_won()
                        self.end_game()
                        break
            else:
                if self.ai_quits:
                    sleep(0.6)
                    self.pprint(common.quit_strings)
                    self.pprint(common.quitwin)
                    self.player_won()
                    self.end_game()
                    break

                if self.opponent.bet() == 'bet':
                    sleep(0.6)
                    if first_round:
                        self.pprint(common.opfirstbet)
                        self.add_bet(ante)
                        first_round = False
                    else:
                        self.pprint(common.opbet)
                        self.add_bet(ante*2)
                    betting = 'player'
                else:
                    sleep(0.6)
                    if first_round:
                        self.pprint(common.opfirstcall)
                        if first_called:
                            bet_continue = False
                        first_called = True
                    else:
                        self.pprint(common.opcall)
                        self.add_bet(ante)
                        bet_continue = False
                    betting = 'player'

            bet_round += 1

    def draw(self):

        if len(self.deck) == 0:
            if self.first_draw == 'player':
                self.pprint(common.opnodeck)
            else:
                self.pprint(common.nodeck)
            self.shuffle()

        if self.first_draw == 'player':
            self.player_card = self.deck.pop(0)
            self.pprint(common.firstdraw)
            if len(self.deck) == 1:
                self.pprint(common.oplastcard)
            self.ai_card = self.deck.pop(0)
            print 'Your card is the %s.\n' % self.player_card
        else:
            self.ai_card = self.deck.pop(0)
            self.pprint(common.seconddraw)
            if len(self.deck) == 1:
                self.pprint(common.lastcard)
            self.player_card = self.deck.pop(0)
            print 'Your card is the %s.\n' % self.player_card

    def compare_cards(self):
        player = make_deck().index(self.player_card)
        opponent = make_deck().index(self.ai_card)
        print 'You place your %s down on the table.' % self.player_card
        print 'Your opponent puts his %s down on the table.' % self.ai_card
        if player < opponent:
            self.player_won()
            self.pprint(common.playerwon)
        else:
            self.opponent_won()
            self.pprint(common.playerlost)
        sleep(0.6)
        print "Enter 'q' to end the game."
        choice = raw_input('>')
        if choice.lower() == 'q' or choice.lower() == 'quit':
            self.end_game()
            self.pprint(common.game_end)

    def shuffle(self):
        if self.first_draw == 'player':
            self.pprint(common.opshuffle)
            sleep(0.6)
            print 'Do you cut?'
            choice = raw_input('>')
            if choice.lower() == 'yes' or choice.lower() == 'y':
                self.pprint(common.cut)
            else:
                self.pprint(common.nocut)
            print 'You push the deck back to the center of the table.\n'
        else:
            self.pprint(common.shuffle)
            if randint(1, 4) > 1:
                self.pprint(common.opcut)
            else:
                self.pprint(common.opnocut)
            print ('Your opponent moves the shuffled deck back to the center '
                   'of the table.\n')

        self.deck = make_deck()
        shuffle(self.deck)

    def end_game(self):
        self.ended = True