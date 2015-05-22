"""
make a game
import a self-made module
one class per location

"""
import textwrap
import highlow
import slots
import coins
import dice
import common
from time import sleep
from random import randint, shuffle

highlow.ante = 50
highlow.face_cards = ['ace', 'giraffe', 'squid', 'ant-eater']
highlow.suit_cards = ['blacks', 'reds', 'yellows', 'greens']

dict = common.dict
# References common dict containing 'player_money' and 'money_type'

tw = textwrap.TextWrapper()
tw.width = 100
tw.subsequent_indent = '  '
nl = '\n'

game_dict_subdict = {'plays': 0,
                     }
games = {'highlow': game_dict_subdict.copy(),
         'coins': game_dict_subdict.copy(),
         'dice': game_dict_subdict.copy(),
         'slots': game_dict_subdict.copy()}
alt_path = 'No'


def wait():
    raw_input(" (Press enter to continue.)")


def wrap(string):
    string = string % dict
    print tw.fill(string), nl


def rwrap(string):
    """Wrap random string from list in common"""
    wrap(string[randint(0, len(string)-1)])


rand_sit_list = []


def random_sit():
    """Wrap random string from common.sitting_random without repeats"""
    global rand_sit_list
    if len(rand_sit_list) == 0:
        rand_sit_list = common.sitting_random[:]
        shuffle(rand_sit_list)
    wrap(rand_sit_list.pop())


inventory = []
short_inv = []


# inventory[:-1] allbutlast, inv[-1] last
def add_inv(item, short):
    inventory.append(item)
    short_inv.append(short)


def inv():
    if len(inventory) == 0:
        print "You have nothing."
    elif len(inventory) == 1:
        wrap("You have " + inventory[0] + ".")
    else:
        ilist = "You have "
        for i in inventory[:-1]:
            ilist = ilist + str(i) + ", "
        ilist = ilist + "and " + inventory[-1] + "."
        wrap(ilist)


class Players(object):
    """This contains potential opponents, and pulls them."""
    def __init__(self):
        self.players = [
            ('Fitch', 'nice'), ('Ritnuk', 'mean'), ('Werner', 'silly'),
            ('Bloogaz', 'silly'), ('Qintz', 'nice'), ('Adamadat', 'silly'),
            ('Rop', 'mean'), ('Crulken', 'nice'), ('Shenv', 'nice'),
            ('Krup', 'mean'), ('Paleor', 'nice'), ('Jupkurn', 'silly'),
            ('Xin', 'nice'), ('Obama', 'nice'), ('Ersh', 'silly'),
            ('Vik', 'mean'), ('Moob', 'nice'), ('Chimchar', 'nice'),
            ('Jenkla', 'nice'), ('Gelb', 'silly'), ('Orubo', 'nice'),
            ('Erkel', 'silly'), ('Huplak', 'mean'), ('Timothy', 'mean'),
            ('Pobo', 'silly'), ('Ferb', 'nice')
        ]
        shuffle(self.players)

    def pull(self):
        if len(self.players) == 0:
            self.__init__()
        return self.players.pop()
players = Players()


class Scene(object):
    def enter(self):
        print "Base scene class."


class Engine(object):
    def __init__(self, zone):
        self.map_class = zone
        self.end_zone = 'endgame'
        self.next_zone = 'act1'

    def start(self):
        while self.end_zone != self.map_class.current_scene:
            self.next_zone = self.map_class.current_map.enter()
            self.map_class.next_scene(self.next_zone)
        self.map_class.current_map.enter()


class ActOne(Scene):
    def enter(self):
        wrap("You are startled awake by a loud pounding noise.")
        wrap("You lean up in your bed and shake your head to clear away the "
             'drowsiness. "Again?" you sigh to yourself, shaking your head '
             "as you look up at the ceiling.")
        choice = raw_input(" (Press enter to continue.)")
        if choice == 'qwerty':
            add_inv('some "fashionable" pajamas', 'pajamas')
            add_inv('a translator', 'translator')
            add_inv('a money chip', 'chip')
            wrap("You skip to the gambling hall.")
            return 'hall'
        print "* BAM BAM BAM *\n"
        sleep(1)
        wrap("Another loud pounding sound reverberates through the walls of "
             'your appartment. "Sheesh, they are really going at it today,"'
             " you say to yourself. You lay back down with a groan and try "
             "repeatedly to fall back asleep, but just when you get close you "
             "are jolted awake again and again.")
        wrap("Feeling pretty fed up at this point, you give up on the idea"
             " of sleeping at all before work in the morning and instead "
             "decide to go upstairs and release some of your rage.")
        wait()
        wrap('You turn on the light and look down at the "fashionable" pajamas'
             " on the floor. Will you put them on, or leave wearing your "
             "purple g-string and see-through tank top?")
        while True:
            choice = raw_input("Do you put on the pajamas?\n>").lower()
            if choice == 'y' or choice == 'yes':
                wrap('You take the "fashionable" pajamas and put them on.')
                add_inv('some "fashionable" pajamas', 'pajamas')
                break
            elif choice == 'n' or choice == 'no':
                wrap('Those pajamas are awfully "fashionable" though. Are you '
                     "sure?")
                while True:
                    choice = raw_input('>').lower()
                    if choice == 'y' or choice == 'yes':
                        wrap("It's pretty cold out there, are you positive?")
                        while True:
                            choice = raw_input('>').lower()
                            if choice == 'y' or choice == 'yes':
                                wrap("Fine, I won't stop you. You leave the "
                                     "pajamas.")
                                add_inv('a purple g-string', 'g-string')
                                add_inv('a see-through tank top', 'tank top')
                                break
                            elif choice == 'n' or choice == 'no':
                                wrap("Good. You take the pajamas and put them "
                                     "on.")
                                add_inv('some "fashionable" pajamas',
                                        'pajamas')
                                break
                            else:
                                continue
                        break
                    elif choice == 'n' or choice == 'no':
                        wrap("Good. You take the pajamas and put them on.")
                        add_inv('some "fashionable" pajamas', 'pajamas')
                        break
                    else:
                        continue
                break
        wrap("You make a quick stop in the bathroom to make sure your hair is "
             "in order before heading to the front door and slipping your "
             "shoes on.")
        wait()
        if 'a purple g-string' in inventory:
            wrap("You take one last wistful look at the pajamas on the floor "
                 "before heading outside.")
            sleep(2)
        wrap("You step out into the hallway of the apartment building. The "
             "cool night air chills you, but the noise from upstairs refuels "
             "your anger and you continue on your way.")
        wrap("You make your way to the elevator, but something in the back of "
             "your mind tells you to take the stairs instead. Do you take the "
             "stairs?")
        while True:
            choice = raw_input('>').lower()
            if choice == 'y' or choice == 'yes':
                wrap("You open the door to the stairwell and notice a long "
                     "piece of string on the floor. Something tells you this"
                     " will be very important in the future. You pick it "
                     "up, stuff it in your pocket, and continue on your way.")
                add_inv('a long piece of string', 'string')
                break
            elif choice == 'n' or choice == 'no':
                wrap("You enter the elevator and press the button. After a "
                     "while you reach the floor above and the doors open.")
                break
        wait()
        wrap("You step into the hall and make your way towards the apartment "
             "above yours. You hear the sound again and suddenly recognize it "
             "as someone pounding on a doorway; your neighbor Fred's door, in"
             " fact, but as you turn the corner you notice nobody is there and"
             " the sound has suddenly stopped.")
        wrap("Fred is a nice, older gentleman you occasionally visit to help"
             " him out around the house. You decide to check up on him.")
        wrap('You knock on the door. "Hey, is everything alright, Fred?" you '
             "call out. The door opens.")
        wait()
        wrap('You walk inside, relieved to see good old Fred is okay, "Who was'
             ' that? Are those kids messing with you again?"')
        wrap('Fred replies, "No, don\'t worry about it, dear. But good of you '
             'to come check on me!" He seems to consider something for a '
             'moment and says, "Listen, I\'m leaving town soon, but I want you'
             ' to have something. It\'s a translator." He pulls something '
             "small from behind his ear and hands it to you.")
        add_inv('a translator', 'translator')
        wrap('You start to consider the cleanliness of Fred\'s ears, but, '
             "being the polite person you are, you kindly take it from him. It"
             " looks a lot like a small button battery.")
        wait()
        wrap("Just as you start to wonder if your good old pal Fred is going "
             "senile, the little disc begins beeping frantically. You see "
             "Fred's eyes light up in alarm as he quickly reaches out to "
             "snatch the object back from your hand, but suddenly your "
             "surroundings change.")
        wait()
        return 'customs'


class Customs(Scene):
    def enter(self):
        wrap("You find yourself in a very sterile little room with blindingly "
             "bright lights coming from above. Before you have a chance to "
             "find your bearings, a speaker near the ceiling begins emitting "
             "what sounds like a loud and garbled mess of syllables.")
        wrap("The sound from the speaker continues. It definitely sounds like "
             "it's angry. 'This can't be real. I'm definitely dreaming,' you "
             "think to yourself.")

        def customs_function():
            """Need a better way to break out of these while loops"""
            while True:
                wrap("Do you look around the room, or use an item?")
                choice = raw_input('>').lower()
                if 'use' in choice or 'item' in choice:
                    while True:
                        inv()
                        wrap("Which item do you use?")
                        choice = raw_input('>').lower()
                        if choice in inventory or choice in short_inv:
                            if (choice == 'a long piece of string' or
                                    choice == 'string'):
                                wrap("You pull the long piece of string out of"
                                     " your pocket and hold it out "
                                     "dramatically in front you.")
                                wrap("Nothing happens.")
                            elif (choice == 'a translator' or
                                  choice == 'translator'):
                                return
                            else:
                                print "You're already wearing that.\n"
                            wrap("The speaker continues it's barrage of what "
                                 "you can only imagine to be vicious insults.")
                            break
                elif 'look' in choice or choice == 'l':
                    wrap("You begin poking around the small room. There's "
                         "definitely a lot of chrome and stainless steel "
                         " around here. There doesn't look to be a way out.")
                    wrap("The speaker continues it's barrage of what you can "
                         "only imagine to be vicious insults.")
        customs_function()
        wrap("You look down at the little disk that you're still holding. "
             "What did he call it? A translator? You place the translator "
             "behind your ear where Fred was wearing it. The instant it "
             "touches your flesh it seems to fuse in and the voice suddenly "
             "becomes intelligible.")
        wait()
        wrap('"FINALLY! You think you can fool me?!" the grating voice yells.'
             '"I know it\'s you, Freg. Did you really think you could hide '
             'forever?!"')
        wrap('You attempt a reply, "But I\'m no-"')
        wrap('"You don\'t think I have connections?! It was only a matter of '
             "time before I found your translator, the guy that makes them "
             'comes here all the time."')
        wrap('You try to speak up again, "But-".')
        wrap('"Look, I don\'t have time for this! I need ten thousand florbs '
             "by the end of the day! If you can't get it, you'll be working "
             "here for the rest of your life. You're lucky I'm even giving you"
             ' a day after all the trouble I\'ve gone through finding you!"')
        wrap("As you attempt to speak up again the speaker clicks and a panel "
             "in the wall slides wide open. With a heavy groan you march your "
             "way out of the room, determined to figure out what the hell is "
             "going on.")
        wait()
        return 'mainhall'


class MainHall(Scene):

    def enter(self):
        wrap("You enter a massive domed hall buzzing with the activity of "
             "countless hundreds of strange alien creatures. You are "
             "currently on a railed second floor walkway overlooking the main "
             "floor. You'd be pretty freaked out right about now if you "
             "weren't sure you were dreaming.")
        wrap("Will you look around some more or head downstairs?")
        while True:
            choice = raw_input('>').lower()
            if 'look' in choice or 'down' in choice or choice in ('l', 'd'):
                if 'look' in choice or choice == 'l':
                    wrap("You take a short walk along the railing, looking "
                         "down at the multitude of strange creatures below.")
                    wrap("The hall reminds you of a casino back on earth, but "
                         "much larger than any you've ever seen. There are "
                         "all manner of games going on here. On closer "
                         "inspection, most of the games here resemble similar "
                         "games on earth. There are machines, card games, dice"
                         " games, and even some simple looking coin games.")
                wrap("As you make your way down the stairs, the frantic sounds"
                     " of hundreds of simultaneous games assaults you. 'It's "
                     "definitely a gambling hall of some sort,' you think to "
                     "yourself.")
                break
        wait()
        wrap("You feel very out of place here surrounded by all these strange,"
             " alien creatures, but none of them seem to notice you. As you "
             "step onto the main floor you are stopped by a tall, thin "
             'humanoid creature, "Hey Freb! Is that you? Where are your '
             'tentacles?"')
        wrap('"Ummm," you retort.')
        wrap('"I saw you come from Customs just now. Look, I heard what '
             'happened.. That\'s rough, man." the creature says.')
        wait()
        wrap('"What the hell is going on here?!" you shout. A couple nearby '
             "creatures glance at you for a moment before turning back to "
             "their games.")
        wrap('The tall creature sighs dejectedly and says, "Okay, okay.. I '
             "admit it.. I gave him your translator codes. Look, it was either"
             ' that or I\'d be stuck here for the rest of my life like you!" '
             "It covers its mouth with its slender, three-fingered hand, "
             '"I didn\'t mean that! Look, if anyone can make ten thousand in a'
             " day it's you, Freb. Look, I'll even give you the thousand "
             "%(money_type)s moneychip Ivarg gave me; said it was 'for my "
             'trouble.\' That bastard."')
        wrap("Before you have a chance to respond it presses something that "
             "looks like a computer chip into your hand and slinks away.")
        add_inv('a money chip', 'chip')
        wait()
        wrap("You look around helplessly, not sure of what to do next. There "
             "doesn't seem to be any doors in this place, and the only path "
             "away leads back to Customs. Everywhere else you are surrounded "
             "by games and the strange creatures that play them. You decide "
             "against heading back upstairs and instead proceed to the center "
             "of the massive room to try and find your bearings.")
        wait()
        return 'hall'


class Hall(Scene):
    def enter(self):
        wrap("You are currently in a massive hall surrounded by hundreds of "
             "alien creatures playing various games. The hall is a cacophony "
             "of sounds; creatures shouting, cheering, and crying, games "
             "dinging and ringing, cards slapping, dice rolling, coins "
             "bouncing. There seems to be no end to all the activity, and none"
             " of these creatures seems to even notice you are here.")
        
        if dict['player_money'] > 9999:
            wrap("It looks like you've made enough %(money_type)ss to pay off"
                 " Freb's debt. Are you ready to head back to Customs?")
            while True:
                choice = raw_input('>').lower()
                if choice == 'y' or choice == 'yes':
                    return 'endgame'
                elif choice == 'n' or choice == 'no':
                    break
        elif dict['player_money'] < 100:
            wrap("It looks like you're not doing too well paying off Freb's "
                 "debt. Are you ready to give up?")
            while True:
                choice = raw_input('>').lower()
                if choice == 'y' or choice == 'yes':
                    return 'alternate'
                elif choice == 'n' or choice == 'no':
                    break
        
        wrap("You are at a crossroads of sorts in the center of the hall. "
             "Nearby are various forms of what you believe to be seating. Do "
             "you sit down for a bit or try to look for a game to play?")
        while True:
            choice = raw_input('>').lower()
            if 'sit' in choice:
                wrap("You settle down on something that looks like a bench.")
                wrap("All of the sounds seem to blend into a kind of white "
                     "noise, and you are somehow able to relax despite all the"
                     " activity around you. Eventually, though, you start to "
                     "grow bored. Will you start to look for a game to play?")
                count = 0
                while True:
                    choice = raw_input('>').lower()
                    if choice == 'y' or choice == 'yes':
                        break
                    elif choice == 'n' or choice == 'no':
                        rwrap(common.sitting_bored)
                        if randint(1, 3) == 1 or count > 2:
                            random_sit()
                            count = 0
                        else:
                            count += 1
                        wrap("Are you ready to look for a game to play?")
                        continue
            elif ('look' in choice or 'play' in choice or 'game' in choice or
                  choice == 'l'):
                pass
            else:
                continue
            break
        wrap("There are literally hundreds of different games being played, "
             "but seeing as how you are new around here you decide to stick "
             "to some that are simple and more familiar.")
        wrap("Do you choose the slot machine, the card game, the dice game, or"
             " the coin flipping game?")
        while True:
            choice = raw_input('>').lower()
            if 'dice' in choice:
                return 'dice'
            elif 'card' in choice:
                return 'highlow'
            elif 'coin' in choice:
                return 'coins'
            elif 'slot' in choice or 'machine' in choice:
                return 'slots'


class Slots(Scene):
    def enter(self):
        if dict['player_money'] < slots.dict['min_bet']:
            wrap("You do not have enough money to play this game. You return "
                 "to the center of the casino.")
            wait()
            return 'hall'
        wrap("You approach a vacant slot machine. It's simple display reads, "
             '"Insert moneychip." To the right is a small slot and a very '
             "large lever. It looks like the type of game you don't need to "
             "understand very well to play.")
        self.play()
        return 'hall'

    # noinspection PyMethodMayBeStatic
    def play(self):
        while True:
            wrap("You take a seat at your machine and insert your moneychip "
                 "into the slot.")
            raw_input(" (Press enter to begin the game.)")
            slots.play()
            dict['player_money'] = slots.dict['player_money']
            games['slots']['plays'] += 1
            if dict['player_money'] < slots.dict['min_bet']:
                wrap("You do not have enough money to play this game. You "
                     "return to the center of the casino.")
                wait()
                return
            wrap("You withdraw your moneychip. Do you wish to play again?")
            while True:
                choice = raw_input('>').lower()
                if choice == 'y' or choice == 'yes':
                    break
                elif choice == 'n' or choice == 'no':
                    wrap("You return to the center of the casino.")
                    return


class Dice(Scene):
    def enter(self):
        if dict['player_money'] < dice.dict['min_bet']:
            wrap("You do not have enough money to play this game. You return "
                 "to the center of the casino.")
            wait()
            return 'hall'
        wrap("You walk over to some groups of creatures that are gambling with"
             " dice. They are using gambling chips. You see a conveniently "
             "placed machine nearby labeled \"Chip Dispenser.\" You insert "
             "your moneychip into the slot and receive %(player_money)d "
             "%(money_type)ss in chips.")
        wrap("Do you check the rulebook or look for a table with an opening?")
        while True:
            choice = raw_input('>').lower()
            if choice == 'l' or 'look' in choice:
                break
            elif 'rule' in choice:
                wrap("You approach a nearby table with a book on it. You thumb"
                     " through the book for a few seconds to become familiar "
                     "with the most important rules.")
                wrap("Betting and rolling goes clockwise starting with the "
                     "newcomer or loser. Instead of a six on these dice there "
                     "is a curious side labeled 'GLOOB'. If you roll one "
                     "'gloob' you automatically lose that round, but if you "
                     "roll two you instantly win the pot.")
                wrap("Otherwise, if the total of your roll is 6 or higher, "
                     "that is your 'keep'. Otherwise you roll again next "
                     "round. Once everyone is out or has a keep, the lowest "
                     "and most recently rolled keep wins!")
                wait()
                break
        self.play()
        return 'hall'

    # noinspection PyMethodMayBeStatic
    def play(self):
        while True:
            wrap("You approach a table with an opening. Each player has a "
                 "small screen on their side of the table displaying their "
                 "name.")
            dice_players = [players.pull()[0], players.pull()[0],
                            players.pull()[0]]
            wrap("It seems that you're opponents are %s, %s, and %s." %
                 (dice_players[0], dice_players[1], dice_players[2]))
            raw_input(" (Press enter to begin the game.)")
            # noinspection PyShadowingNames
            game = dice.Game(dice_players[0], dice_players[1], dice_players[2])
            game.start()
            dict['player_money'] = dice.dict['player_money']
            games['dice']['plays'] += 1
            wait()
            if dict['player_money'] < dice.dict['min_bet']:
                wrap("You do not have enough money to play this game. You "
                     "return to the center of the casino.")
                wait()
                return
            wrap("Do you wish to play again?")
            while True:
                choice = raw_input('>').lower()
                if choice == 'y' or choice == 'yes':
                    break
                elif choice == 'n' or choice == 'no':
                    wrap("You cash in your chips and and return to the center "
                         "of the casino.")
                    return


class Coins(Scene):
    def enter(self):
        if dict['player_money'] < coins.dict['min_bet']:
            wrap("You do not have enough money to play this game. You return "
                 "to the center of the casino.")
            wait()
            return 'hall'
        wrap("You approach a group of aliens playing some sort of coin game. "
             "There are a number of large glass pods here, each with two "
             "players on either side. Each player places their bet and calls "
             "heads or tails. They then press a button on the top of the pod "
             "that releases the coin behind the glass, and the winner collects"
             " the bet.")
        wrap("The obvious 'heads' side is the head of some kind of serpent-"
             "like creature. 'Tails' has too much detail to make out.")
        wait()
        self.play()
        return 'hall'

    # noinspection PyMethodMayBeStatic
    def play(self):
        while True:
            if games['coins']['plays'] == 0:
                wrap("You walk up to the first pod you find that has a "
                     "vacancy. "
                     "On the opposite side is a stocky creature with a face "
                     "that "
                     "looks perpetually frustrated.")
                wrap("The creature, upon noticing your arrival, points to a "
                     "sticker on it's chest that says 'Adame.' The creature "
                     "looks "
                     "like it's eager to begin the game. You insert your "
                     "moneychip"
                     " into the slot on the pod.")
                
                raw_input(" (Press enter to begin the game with Adame.)")
                opponent = coins.Game('Adame')
                opponent.start()
            else:
                opponent_name, manner = players.pull()
                if manner == 'nice':
                    wrap("You walk up to an vacant pod and insert your "
                         "moneychip.")
                    wrap('"Hello, stranger! I\'m %s' % opponent_name + '," the'
                         " creature across from you says.")
                    raw_input(" (Press enter to begin the game with %s.)" %
                              opponent_name)
                    opponent = coins.Game(opponent_name)
                    opponent.start()
                elif manner == 'mean':
                    wrap("You walk up to an vacant pod and insert your "
                         "moneychip.")
                    wrap('"Me %s!" your opponent says.' %
                         opponent_name)
                    raw_input(" (Press enter to begin the game with %s.)" %
                              opponent_name)
                    opponent = coins.Game(opponent_name)
                    opponent.start()
                elif manner == 'silly':
                    wrap("You walk up to an vacant pod and insert your "
                         "moneychip.")
                    wrap('"%s be my name!" the odd creature from across the ' %
                         opponent_name + "large pod says.")
                    raw_input(" (Press enter to begin the game with %s.)" %
                              opponent_name)
                    opponent = coins.Game(opponent_name)
                    opponent.start()

            dict['player_money'] = coins.dict['player_money']
            games['coins']['plays'] += 1
            wrap("You withdraw your moneychip and return it to your pocket.")
            wait()
            if dict['player_money'] < coins.dict['min_bet']:
                wrap("You do not have enough money to play this game. You "
                     "return "
                     "to the center of the casino.")
                wait()
                return
            wrap("Do you wish to find another opponent?")
            while True:
                choice = raw_input('>').lower()
                if choice == 'y' or choice == 'yes':
                    break
                elif choice == 'n' or choice == 'no':
                    wrap("You return to the center of the casino.")
                    return


class HighLow(Scene):
    """This class runs the highlow game."""
    def enter(self):
        if dict['player_money'] < highlow.ante:
            wrap("You do not have enough money to play this game. You return "
                 "to the center of the casino.")
            wait()
            return 'hall'
        wrap("You walk up to a simple looking card game. You notice that the "
             "players here are gambling with chips and see a conveniently "
             "placed machine nearby labeled \"Chip Dispenser.\" You withdraw "
             "%(player_money)d %(money_type)ss in chips from your moneychip. "
             "There are a number of games going on in here. Nearby there is a "
             "small table with a book on it and a sign posted above.")

        wrap("Will you approach the sign or join a game?")

        while True:
            choice = raw_input('>').lower()
            if 'sign' in choice or "approach" in choice:
                wrap("You read the text on the nearby sign made slightly "
                     "fuzzy by the translator:")

                print """Rules of the game:

                    1. Higher card wins.
                    2. Ante in before drawing.
                    3. Loser draws first.
                    4. Aces high.

                """
                wrap("  Ante/Bet increments: %d " % highlow.ante +
                     "%(money_type)ss")

                wait()

                wrap("Below the sign is a small table with a book labeled "
                     'Rules." You thumb through it a bit and get familiar with'
                     "the deck. The ace and number cards are easy, but then "
                     "there's a strange squid looking creature, a yellow thing"
                     " with a giraffe neck, and something that looks almost "
                     "like an ant-eater. It seems the order is ace, giraffe, "
                     "squid, ant-eater, and then the numbered cards. Suits are"
                     " ordered blacks, reds, yellows, then greens.")
                wait()
            elif 'game' in choice or 'join' in choice:
                pass
            else:
                continue
            break
        self.play()
        return 'hall'

    # noinspection PyMethodMayBeStatic
    def play(self):
        while True:
            if games['highlow']['plays'] == 0:
                wrap("You step down to the play area. There are a number of "
                     "small "
                     "tables here with stool on either end. It seems there is "
                     "only"
                     " one table with an opening.")

                wrap("You approach a meek looking alien at an empty table. He "
                     "gestures for you to sit down. He looks at you with his "
                     "bug-"
                     'like eyes and says, "I\'m Blorgenschmilkt. Good luck to'
                     ' you,'
                     ' stranger."')

                wrap('"Blor.. gen.. Can I call you Bob?" you ask. He shrugs '
                     "indifferently.")

                raw_input(" (Press enter to begin the game with Bob.)")
                opponent = highlow.CardAI('Bob', 2)
                opponent.game.start()
            else:
                opponent_name, manner = players.pull()
                if manner == 'nice':
                    wrap("You find an empty seat and settle in.")
                    wrap('"Hey there! My name is %s' % opponent_name + '," the'
                         " creature across from you says.")
                    raw_input(" (Press enter to begin the game with %s.)" %
                              opponent_name)
                    opponent = highlow.CardAI(opponent_name, 3)
                    opponent.game.start()
                elif manner == 'mean':
                    wrap("You find an empty seat and settle in.")
                    wrap('"Me %s!" your opponent says with a grimace.' %
                         opponent_name + " At least it looks like a grimace.")
                    raw_input(" (Press enter to begin the game with %s.)" %
                              opponent_name)
                    opponent = highlow.CardAI(opponent_name, 1)
                    opponent.game.start()
                elif manner == 'silly':
                    wrap("You find an empty seat and settle in.")
                    wrap('"%s be me!" the strange creature from across the ' %
                         opponent_name + "small table says.")
                    raw_input(" (Press enter to begin the game with %s.)" %
                              opponent_name)
                    opponent = highlow.CardAI(opponent_name, 5)
                    opponent.game.start()

            dict['player_money'] = highlow.player_money
            games['highlow']['plays'] += 1
            wait()
            if dict['player_money'] < highlow.ante:
                wrap("You do not have enough money to play this game. You "
                     "return "
                     "to the center of the casino.")
                wait()
                return
            wrap("Do you wish to play again?")
            while True:
                choice = raw_input('>').lower()
                if choice == 'y' or choice == 'yes':
                    break
                elif choice == 'n' or choice == 'no':
                    wrap("You cash in your chips and and return to the center "
                         "of "
                         "the casino.")
                    return


class AlternatePath(Scene):
    def enter(self):
        global alt_path
        alt_path = 'Yes'
        wrap("So, you give up. You aren't looking forward to sticking around "
             "here forever, but you gave it your best. Besides, you seem to "
             "have adjusted pretty well. You're pretty sure most people "
             "wouldn't have.")
        wrap("You give a forlorn sigh and begin walking around the casino "
             "floor. You occasionally notice the servers and begin to wonder "
             "where, in this place with no doors, the kitchen might be.")
        wrap("You begin following a pink-colored server holding an empty tray."
             " She (you assume it's a she, since it's pink) takes another "
             "creature's order and begins walking away. You decide to follow.")
        wait()
        wrap("She looks to be moving at a leisurely pace, but keeping up with "
             "her ends up being more difficult than you bargained for. "
             "Eventually, though, she reaches a wall and the a portion of it "
             "slides right open. You slip inside behind her.")
        wrap("You enter into a long corridor, but the server is nowhere in "
             "sight. You continue along the path until you reach a doorway. "
             "As you approach the doorway it slides open and you enter the "
             "room. Everything inside is bright and white and it takes a while"
             " for your eyes to adjust.")
        wait()
        wrap("Inside the room is an older, fair-skinned human with white hair "
             'and a beard. He gives you a serene smile and says, "Hello."')
        wait()
        wrap('"Who... Who are you?" you respond tentatively.')
        wait()
        wrap('"I am the architect. I created this casino. I\'ve been waiting '
             'for you. You have many questions. Though the process-"')
        wait()
        wrap('"Wait, wait.. Stop right there.. Don\'t tell me all this is just'
             ' some stupid computer generated reality or something.." you '
             "reply impatiently.")
        wait()
        wrap('He blinks incredulously at you and shakes his head, "What the '
             'hell are you talking about? I\'m the architect, Marvik, from '
             'Flerbon V? I just designed this casino. Your friend Freb got '
             'a message out to me, he told me what happened. I owed him, so I '
             'told him I\'d take care of it. Here is the ten thousand florbs '
             'you need to pay Ivarg. Freb says sorry for the trouble."')
        wait()
        wrap('"Ohh... ... Good.. Thanks," you respond gratefully. You suddenly'
             " notice the seven fingers on each hand, and large, pointy ears.")
        if 'a purple g-string' in inventory:
            wrap('The man adds, "Oh yeah, and Freb told me to get these to '
                 'you." He pulls out some "fashionable" pajamas and hands them'
                 " to you. Naturally, you quickly put them on.")
            add_inv('some "fashionable" pajamas', 'pajamas')
        dict['player_money'] += 10000
        wrap("You exit the room and head back to the main hall of the casino.")
        wait()
        return 'endgame'


class EndGame(Scene):
    def enter(self):
        wrap("After spending some time in the casino you almost forgot about "
             "the unpleasant experience back in Customs. You heave a big sigh "
             "and head back to the stairs that lead to the second floor.")
        wrap("You ascend the stairs and stop near the part of the wall where "
             "you first emerged into the main hall. Before you muster up the "
             "courage to knock, you hear another doorway slide open a couple "
             "paces along the wall. You see a large, fat, worm-like creature "
             "come slinking out and toward you.")
        wait()
        wrap('"I didn\'t think you could do it Freb. Boy did you prove me '
             'wrong!" the fat worm says in a happy tone. As he approaches, you'
             " become aware of his odor; while not quite as bad as you might "
             "imagine looking at him, it's still quite pungent. "
             '"Are you still wearing that getup?" he asks.')
        wrap('"I told you I\'m not Freb!" you huff.')
        wrap('"Heh, you already have the money! You know I keep my word," the '
             'creature says. "Why are you...?"')
        wrap("You smirk at the creature you presume to be Ivarg, giving it a "
             "couple moments to let the obvious sink in.")
        wait()
        wrap('"... Ohhhh crap.. Oh no.. This is not good.. You\'re not '
             'supposed to be here!" he shouts. "How did this happen?!"')
        wrap('"A friend of mine gave me this just before I was sent here," you'
             ' reply as you gesture towards the translator. "It started '
             'beeping and then suddenly I was here," you say. You start to '
             "wonder why you are speaking so casually about all this. Maybe "
             "you finally found your niche.")
        wrap('"Frobnit!" he curses. He thinks for a moment and says, "Okay, '
             'like I said, I keep my word. You are free to go, and you can '
             'even keep the money, but two things: Firstly, you can NOT tell '
             'anyone on your planet about this. It would not end well for '
             'them. Just trust me. And second, how would you like a really '
             'cushy job?"')
        wrap('"How\'s the pay?" you blurt out, genuinely surprised that you '
             "are even considering this giant slug's job offer.")
        wrap("Ivarg's fat wormy face gives what you can only imagine to be a "
             "big grin.")
        wrap("  (You won! Where will your adventures take you next? Whatever "
             "happened to Freb? How much is a florb worth in US dollars? "
             "Answers to all these questions and more in Episode 2: Attack of "
             "the Glones!")
        raw_input(" (Press enter to see your stats.)")
        print "\n Stats:"
        print "  Games Played:"
        print "   Cards:   %d" % games['highlow']['plays']
        print "    Wins:   %d" % highlow.dict['wins']
        print "    Losses: %d\n" % highlow.dict['losses']
        print "   Coins:   %d" % games['coins']['plays']
        print "    Wins:   %d" % coins.dict['wins']
        print "    Losses: %d\n" % coins.dict['losses']
        print "   Dice:    %d" % games['dice']['plays']
        print "    Wins:   %d" % dice.dict['wins']
        print "    Losses: %d\n" % dice.dict['losses']
        print "   Slots:   %d" % games['slots']['plays']
        print "    Wins:   %d" % slots.dict['wins']
        print "    Losses: %d\n" % slots.dict['losses']
        print "  Alternate Path Taken: %s\n" % alt_path
        print "  Total Florbs Accrued: %(player_money)d\n" % dict
        if 'a long piece of string' in inventory:
            wrap("You picked up a dirty piece of string from the floor for "
                 "some reason.")
        else:
            wrap("You missed a very important item during your journey.")
        if 'some "fashionable" pajamas' in inventory:
            wrap('You are wearing "fashionable" pajamas. Thank goodness.')
        else:
            wrap("You managed to win without the pajamas. Congratulations.")
        raw_input("")


class Zone(object):

    scenes = {
        'act1': ActOne(),
        'highlow': HighLow(),
        'mainhall': MainHall(),
        'hall': Hall(),
        'customs': Customs(),
        'coins': Coins(),
        'dice': Dice(),
        'slots': Slots(),
        'alternate': AlternatePath(),
        'endgame': EndGame()
    }

    def __init__(self, mapname):
        self.current_map = Zone.scenes[mapname]
        self.current_scene = mapname

    def next_scene(self, mapname):
        self.current_map = Zone.scenes[mapname]
        self.current_scene = mapname


startmap = Zone('act1')
game = Engine(startmap)
game.start()