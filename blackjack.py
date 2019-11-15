import random
from IPython.display import clear_output as clear

# Global variables to decide if the game is being played or if the deck needs to be shuffled
playing = True
shuffle_deck = False

# These are the tuples and dictionary that is used to create cards and decipher their values

ranks = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
suits = ('\u2661', '\u2662', '\u2664', '\u2667')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}

# This class initiates a card object that has a rank, suit, and value

class Card:
    
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        self.value = values[self.rank]
        
    def __str__(self):
        return self.rank + self.suit

# This class initiates a deck object that uses nested for loops to assign each suit and rank to a card object.
# Each deck object will store 52 card objects unless the suits and/or ranks variables are changed from their
# default values.

class Deck:
    
    def __init__(self):
        self.deck = []
        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(rank,suit))
                
    #def __str__(self):
        #deck_comp = ''
        #for card in self.deck:
            #deck_comp += '\n' + card.__str__()
        #return deck_comp
    
    def __str__(self):
        deck_comp = ''
        c = len(self.deck)
        for card in self.deck:
            if c % 13 == 0:
                deck_comp += '\n\n' + card.__str__() + ' '
                c -= 1
            else:
                deck_comp += card.__str__() + ' '
                c -= 1
        return deck_comp
    
    def shuffle(self):
        for i in range(5):
            random.shuffle(self.deck)
            
    def deal(self):
        top_card = self.deck.pop()
        return top_card

# This class creates a hand object which has a method that allows the hand to grab a card from the deck and
# add it to itself. Cards added to the hand are stored in a list.

class Hand:
    
    def __init__(self):
        self.hand = []
        self.value = 0
        self.aces = 0
        
    def __str__(self):
        hand_comp = ''
        for card in self.hand:
            hand_comp += '\n' + card.__str__()
        return hand_comp
    
    def add_card(self,card):
        self.hand.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1
            
    def ace_adjust(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# This class creates a chips object to be assigned to the players hand.

class Chips:
    
    def __init__(self,total=100):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet

# This function asks the user for their wager until the user enters an integer that is less than or equal to
# the value of their chips

def take_bet(chips):
    
    prompt = 'Place your wager:'
    
    while True:
        
        try:
            clear()
            chips.bet = int(input(prompt + '\n'))
            clear()
        
        except:
            prompt = 'Please enter an integer:'
        
        else:
            
            if chips.bet > chips.total:
                prompt = f'Sorry, you only have {chips.total} chips to wager:'
            
            else:
                print(f'You wagered {chips.bet} chips.')
                break

# Simple function that takes the deck and a hand as a parameter and adds a card from the deck that is passed
# to the card that is passed.

def hit(deck, hand):
    
    hand.add_card(deck.deal())
    hand.ace_adjust()

# This is repeated after the hand is dealt to ask the player if they would like to hit or stay

def hit_hand(deck, hand):
    
    global playing
    
    while True:
        clear()
        h = input(F'You have {hand.value}. Would you like to (h)it or (s)tay?')
        
        if h[0].lower() == 'h':
            hit(deck, hand)
        elif h[0].lower() == 's':
            playing = False
        else:
            continue
        break
    clear()
    print(f'You have {hand.value}.')

