
dict = {'player_money': 1000,
        'money_type': "florb"}


# -------------------------------------------------
# Strings for main module

sitting_bored = ["You spend a couple minutes swinging your feet, bored.", "You"
                 " stretch and yawn, feeling pretty bored.", "You look around "
                 "aimlessly, feeling bored."]

sitting_random = ["A creature nearby stands from his table and begins cheering"
                  " wildly. You start to feel like there might be some fun to "
                  "be had here.", "A tentacled creature with a single, large "
                  "eye winks at you. You begin to feel confused and "
                  "uncomfortable.", "An excited crowd seems to have gathered "
                  "around a crab-like creature sitting at"
                  " a slot machine.", "A group of unicorn-like "
                  "creatures passes"
                  ' by, chanting, "BROS! BROS! BROS! BROS!"', "A pink, curvy, "
                  "feminine-looking creature walks by, offering drinks to "
                  "customers in a very gruff voice.", "A creature that reminds"
                  " you of an armadillo walks by, playing a loud, annoying "
                  "instrument that looks just like an accordion."]

# -------------------------------------------------
# Strings for Coins module. {0} is dict, {1} is opponent name, {2} = doublebet

game_begins = "The game with {1} begins."

no_money = "You do not have enough money to continue."

buy_in = ("You each submit your {0[min_bet]} {0[money_type]} "
          "buy-in. You have {0[player_money]} {0[money_type]}s left.")

all_in = ("You are helpless as the console adds the remainder "
          "of your money to the pot.")

third_side_bet = ("You are helpless as the console adds {2} {0[money_type]}s "
                  "each to the pot. You have {0[player_money]} "
                  "{0[money_type]}s left.")

current_pot = "The current pot is {0[bet]} {0[money_type]}s."

ts_coin = ["The coin is dropped within the pod. There's something "
           "strange about this coin that you can't quite place.", "The coin "
           "drops from it's slot. It looks very odd as it bounces.", "The coin"
           " is released inside the pod. It has a strange glimmer as it "
           "falls."]

coin_drop = ["The coin is released inside the pod. It bounces a few times.",
             "The coin is dropped.", "The coin is released and falls to the "
             "ground with a jingling sound."]

third_side = ["The coin lands on it's third side. Nobody wins.", "The coin "
              "stops. You can't quite make out which side it landed on."]

ai_quits = ["{1} withdraws it's moneychip and leaves the game.", "{1} grumbles"
            " a bit before pulling it's moneychip and walking away.", "{1} "
            "shakes it's head as it pulls it's moneychip and exits the game."]

winner = ("You won {0[bet]} {0[money_type]}s! You currently have "
          "{0[player_money]} {0[money_type]}s left.")

loser = ("You lost. You currently have {0[player_money]} {0[money_type]}s "
         "left.")

# -------------------------------------------------
# Strings for dice module. {0} is dict, {1,2,3} is player 1, 2, and 3


# -------------------------------------------------
# Strings for highlow module
bet_strings = ["You try to examine your opponent for any"
               " sign of a high or low card.", "You look down at your card.",
               "%(name)s rubs his chin as he looks at his card."]

quit_strings = ["%(name)s shakes his head and throws his cards on the "
                "table. You smirk as he walks away.", "%(name)s "
                'shakes his head and places his cards down, "I\'m done."']

ante_in = ["You each put in your %(ante)d %(dollar)s ante. "
           "You have %(money)d %(dollar)ss left."]

game_end = ["The game with %(name)s ends. You have %(money)d %(dollar)ss."]

bet_end = ["Betting ends. The current bet is %(bet)d %(dollar)ss.\n"]

game_start = ["The game with %(name)s begins.\n"]

raise2 = ["You raise as well. You add %(ante2)d %(dollar)ss.\n", "You "
          "also raise. You add %(ante2)d %(dollar)ss to the bet.\n"]

raise1 = ['"Raise!" you call out as you place %(ante)d %(dollar)ss'
          " worth of chips near the deck.\n", "You push %(ante)d %(dollar)ss "
          "worth of chips to the center of the table to signal your raise.\n",
          '"I raise," you say to %(name)s as you add %(ante)d %(dollar)ss '
          "worth of chips to the pile.\n"]

call2 = ["You call. You add %(ante)d %(dollar)ss to the pile.\n", '"Call," you'
         " say as you push %(ante)d %(dollar)ss worth of chips near the "
         "deck.\n"]

call1 = ["You check.\n", '"Check," you say as you rap your knuckle against the'
         " the table.\n"]

quitwin = ["You collect your %(bet)d %(dollar)ss.\n"]

opfirstbet = ['"I\'ll start with a bet," %(name)s says. %(name)s puts %(ante)d'
              " %(dollar)ss worth in chips on the table.\n", "%(name)s adds "
              "%(ante)d %(dollar)ss worth in chips to the bet to raise.\n"]

opbet = ['"I\'ll raise that," %(name)s says as he places %(ante2)d '
         '%(dollar)ss worth of chips down.\n', '"I\'ll raise," %(name)s says '
         'as'
         " he pushes %(ante2)d %(dollar)ss worth in chips to the center of the"
         " table.\n"]

opfirstcall = ['%(name)s says, "Check."\n', "%(name)s taps the table and says,"
               ' "I check."\n']

opcall = ['%(name)s says, "Call." He adds %(ante)d %(dollar)ss to the pile.\n',
          '%(name)s adds %(ante)d %(dollar)ss to the pile and says, "I call."'
          "\n"]

opnodeck = ["%(name)s pushes the two discard piles together."]

nodeck = ["You gather up the two discard piles."]

firstdraw = ["You draw the first card, and %(name)s draws immediately after"
             " you.\n"]

seconddraw = ["You draw your card after %(name)s draws his.\n"]

lastcard = ["You draw the last card.\n"]

oplastcard = ["%(name)s draws the last card.\n"]

playerwon = ["\nYou won! You have %(money)d %(dollar)ss left.\n"]

playerlost = ["\nYou lost. You have %(money)d %(dollar)ss left.\n"]

opshuffle = ["%(name)s expertly shuffles the deck. He pushes it over to you"
             " to cut."]

cut = ["You cut the deck."]

nocut = ["You give a quick tap on the top of the deck with your knuckle."]

shuffle = ["You nimbly shuffle the deck. You place it on the table "
           "and push it to %(name)s."]

opcut = ["He cuts the deck."]

opnocut = ["He taps."]