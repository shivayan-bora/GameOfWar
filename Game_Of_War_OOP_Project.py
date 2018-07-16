#####################################
### WELCOME TO YOUR OOP PROJECT #####
#####################################

# This is an implementation of the popular card game "War" in Pyhton. The rules
# are as follows:
#
# The deck is divided evenly, with each player receiving 26 cards, dealt one
# at a time, face down. Anyone may deal first. Each player places his stack of
# cards face down, in front of him.
#
# The Play:
#
# Each player turns up a card at the same time and the player with the higher
# card takes both cards and puts them, face down, on the bottom of his stack.
#
# If the cards are the same rank, it is War. Each player turns up three cards
# facedown and one card face up. The player with the higher cards takes both
# piles (six cards). If the turned-up cards are again the same rank, each
# player places another card face down and turns another card face up. The
# player with the higher card takes all 10 cards, and so on.
#
# We are ignoring "double" wars  for now
#
# https://en.wikipedia.org/wiki/War_(card_game)

from random import shuffle

# Two useful variables for creating Cards.
SUITES = 'H D S C'.split()
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()


class Deck:
    """
    This is the Deck Class. This object will create a deck of cards to initiate
    play. You can then use this Deck list of cards to split in half and give to
    the players. It will use SUITE and RANKS to create the deck. It should also
    have a method for splitting/cutting the deck in half and Shuffling
    the deck.
    """

    def __init__(self):
        print("Creating New Ordered Deck")
        self.deck_list = [(suite, rank) for suite in SUITES for rank in RANKS]

    def shuffle_deck(self):
        print("Shuffling the deck")
        shuffle(self.deck_list)

    def split_deck(self):
        print("Splitting the deck")
        return (self.deck_list[:26], self.deck_list[26:])


class Hand:
    '''
    This is the Hand class. Each player has a Hand, and can add or remove
    cards from that hand. There should be an add and remove card method here.
    '''

    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return f"Contains {len(self.cards)} cards"

    def add_card(self, added_cards):
        self.cards.extend(added_cards)

    def remove_card(self):
        return self.cards.pop()


class Player:
    """
    This is the Player class, which takes in a name and an instance of a Hand
    class object. The Payer can then play cards and check if they still
    have cards.
    """

    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def play_card(self):
        print(f"{self.name} playing a card from hand")
        drawn_card = self.hand.remove_card()
        print(f"{self.name} has placed: {drawn_card}")
        print("\n")
        return drawn_card

    def remove_war_cards(self):
        war_cards = []
        if len(self.hand.cards) < 3:
            return self.hand.cards
        else:
            for x in range(3):
                war_cards.append(self.hand.remove_card())

            return war_cards

    def check_hand(self):
        print(f"Checking the number of cards in hand for {self.name}")
        return len(self.hand.cards) != 0


######################
#### GAME PLAY #######
######################
print("Welcome to War, let's begin...")

# Use the 3 classes along with some logic to play a game of war!
# Create a new deck
deck = Deck()
deck.shuffle_deck()
half1, half2 = deck.split_deck()

# Create both players
comp = Player("Computer", Hand(half1))

name = input("What is your name?")
user = Player(name, Hand(half2))

total_rounds = 0
war_count = 0

# If both the players have card in hand
while user.check_hand() and comp.check_hand():
    # Start of new round
    total_rounds += 1
    print("Time for a new round!")
    print("Here are the current standings")
    print(f"{user.name} has the count: {str(len(user.hand.cards))}")
    print(f"{comp.name} has the count: {str(len(comp.hand.cards))}")
    print("Play a card!")
    print("\n")

    table_cards = []

    # Play cards
    c_card = comp.play_card()
    p_card = user.play_card()

    # Add to table_cards
    table_cards.append(c_card)
    table_cards.append(p_card)

    # Checking if War occurred
    if c_card[1] == p_card[1]:
        war_count += 1
        print("WAR!!!")

        table_cards.extend(user.remove_war_cards())
        table_cards.extend(comp.remove_war_cards())

        # Play cards
        c_card = comp.play_card()
        p_card = user.play_card()

        # Add to table_cards
        table_cards.append(c_card)
        table_cards.append(p_card)

        # User card is greater
        if RANKS.index(c_card[1]) < RANKS.index(p_card[1]):
            user.hand.add_card(table_cards)
        # Second round of war
        elif c_card[1] == p_card[1]:
            while True:
                if not user.check_hand() or not comp.check_hand():
                    break
                war_count += 1
                print("WAR AGAIN!!!")
                table_cards.append(user.hand.remove_card())
                table_cards.append(comp.hand.remove_card())

                # Play cards
                c_card = comp.play_card()
                p_card = user.play_card()

                # Add to table_cards
                table_cards.append(c_card)
                table_cards.append(p_card)

                if RANKS.index(c_card[1]) < RANKS.index(p_card[1]):
                    user.hand.add_card(table_cards)
                    break
                elif c_card[1] == p_card[1]:
                    continue
                else:
                    comp.hand.add_card(table_cards)
                    break
        # Computer card is greater
        else:
            comp.hand.add_card(table_cards)
    # If War didn't occur
    else:
        if RANKS.index(c_card[1]) < RANKS.index(p_card[1]):
            user.hand.add_card(table_cards)
        else:
            comp.hand.add_card(table_cards)

print("Game Over!!")
print(f"Total number of Rounds: {total_rounds}")
print(f"Total number of time War occurred: {war_count}")

print(f"Does the computer still has cards? {str(comp.check_hand())}")
print(f"Does {user.name} still has cards? {str(user.check_hand())}")
