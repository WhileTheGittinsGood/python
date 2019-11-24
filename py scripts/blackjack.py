import random
#from IPython.display import clear_output as clear
from time import sleep

# Global variables to decide if the game is being played or if the deck needs to be shuffled
playing = True
reshuffle = False
game_start = True
doubled = False

hand_count = 0

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
        for n in range(8):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(rank,suit))
        self.dis_deck = []
    
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
        self.deck += self.dis_deck
        self.dis_deck = []
        random.shuffle(self.deck)
        print('The deck has been shuffled.')
        #print(str(len(deck.deck)) + ' cards in deck')

            
    def deal(self):
        top_card = self.deck.pop()
        return top_card

    def discard(self, player, dealer):
        self.dis_deck.append(player)
        self.dis_deck.append(dealer)

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
            hand_comp += card.__str__() + ' '
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
        
    def blackjack(self):
        self.total += (self.bet * 1.5)
        self.total = round(self.total)

    def double_down(self):
        self.bet *= 2

# This function asks the user for their wager until the user enters an integer that is less than or equal to
# the value of their chips

def take_bet(chips):    
    prompt = f'Place your wager, you have {chips.total} chips: '
    while True:
        try:
            chips.bet = int(input(prompt))
            #clear(wait=True)        
        except:
            prompt = f'Enter an integer, you have {chips.total} chips:'
            #clear(wait=True)        
        else:            
            if chips.bet > chips.total:
                prompt = f'You only have {chips.total} chips to wager:'
            elif chips.bet < 1:
                prompt = f'Wager must be a positive amount, you have {chips.total}:'
            
            else:
                # print(f'You wagered {chips.bet} chip(s).')
                break


def double_down(chips, deck, hand):
    global doubled
    while True:
        try:
            n = input('Would you like to double down and hit, (y)es or (n)o? ')
        
            if n[0].lower() == 'y':
                chips.double_down()
                hit(deck, hand)
                doubled = True
                break
            elif n[0].lower() == 'n':
                break
            else:
                continue
        except:
            print('Enter (y) or (n)')

# Simple function that takes the deck and a hand as a parameter and adds a card from the deck that is passed
# to the card that is passed.
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.ace_adjust()

# This is repeated after the hand is dealt to ask the player if they would like to hit or stay
def hit_or_stay(deck, hand):
    global playing
    while True:
        #h = input(f'You have {hand.value}. Would you like to (h)it or (s)tay? ')
        h = input('Would you like to hit, (y)es or (n)o? ')
        try:
            if h[0].lower() == 'y':
                hit(deck, hand)
            elif h[0].lower() == 'n':
                # print('Player stays.')
                playing = False
            else:
                continue
            break
        except:
            print('Enter (y) or (n)')

# The following functions are used when either player or dealer reach a victory condition.
# The functions print out the winner and adjust the players chips accordingly.
def blackjack(player, dealer, chips):
    print(f'Blackjack! Win {round(chips.bet * 1.5)} chips.')
    chips.blackjack()
    print(f'{chips.total} chip(s) in bank.\n')

def win_hand(player, dealer, chips):
    print(f'Win {chips.bet} chip(s).')
    chips.win_bet()
    print(f'{chips.total} chip(s) in bank.\n')

def lose_hand(player, dealer, chips):
    print(f'Lose {chips.bet} chip(s).')
    chips.lose_bet()
    print(f'{chips.total} chip(s) in bank.\n')
    
def push(player, dealer, chips):
    print('Push.')
    print(f'{chips.total} chip(s) in bank.\n')

# The following functions are used after cards are dealt to display the cards
def show_deal(player, dealer):    
    print(f'Dealer shows: {dealer.hand[1].value}')
    print(f'XX {dealer.hand[1]}')
    
    print(f'Player has: {player.value}')
    print(player.__str__())

def show_all(player, dealer):
    print(f'Dealer has: {dealer.value}')
    print(dealer.__str__())
    
    print(f'Player has: {player.value}')
    print(player.__str__())

# Deals 4 cards alternating from the player to the dealer 
def deal(player, dealer, deck):    
    global hand_count
    for num in range(4):
        if num % 2 == 0:
            player.add_card(deck.deal())
        else:
            dealer.add_card(deck.deal())
    hand_count += 1

# This function is ran after a hand is finished
# If the deck has less cards remaining than specified
# by its num variable it will set the reshuffle boolean
# to True else it will set the playing boolean to true
def shuffle_check(deck):
    global reshuffle
    global playing

    num = 20

    if len(deck.deck) < num:
        reshuffle = True
    else:
        playing = True

# This function is called after the hand is completed.
# User input decides if another hand is dealt.
def new_game():
    
    while True:
        n = input('\nPlay another hand, (y)es or (n)o? ')        

        try:
            if n[0].lower() == 'y':
                shuffle_check(deck)
                break
            elif n[0].lower() == 'n':
                print('exiting')
                exit()
            else:
                continue
        except:
            print('Enter (y) or (n)')

def repeat_bet(chips):
    global doubled

    if doubled:
        chips.bet /= 2
        chips.bet = round(chips.bet)
        doubled = False

    while True:
        r = input(f'Repeat bet {chips.bet} chip(s), (y)es or (n)o? ')

        try:
            if r[0].lower() == 'y':
                chips.bet = chips.bet
                break
            elif r[0].lower() == 'n':
                take_bet(chips)
                break
            else:
                continue
        except:
            print('Enter (y)es or (n)o')



# This is where the game logic begins
while True:
    # Setup chips object. Default value is 100
    chips = Chips()

    while game_start:
        
        #print('Welcome to Blackjack!')
        
        reshuffle = False
        playing = True
        
        # Setup deck object. There are 8 decks when a deck object is initialized (416 cards)
        deck = Deck()
        deck.shuffle()
        
        while not reshuffle:
            
            if chips.bet == 0:
                take_bet(chips)
            else:
                repeat_bet(chips)

            dealer = Hand()
            player = Hand()

            deal(player, dealer, deck)
            print(f'Hands dealt: {hand_count}')
                
            # Player was dealt a blackjack
            if player.value == 21:
                show_all(player, dealer)
                blackjack(player, dealer, chips)
                sleep(3)
                continue

            if dealer.hand[1].value == 11:
                print('INSURANCE FUNCTION')

            if player.value == 11:
                show_deal(player, dealer)
                double_down(chips, deck, player)
            

            # Player was dealt anything except blackjack
            while playing and player.value < 21:

                show_deal(player, dealer)

                # Asks player if they want to hit or stay
                hit_or_stay(deck, player)

                # Player hit and busts
                if player.value > 21:
                    show_deal(player, dealer)
                    lose_hand(player, dealer, chips)
                    break

            # Player stays
            if player.value <= 21:
                
                while dealer.value < 17:
                    hit(deck, dealer)

                show_all(player, dealer)

                if dealer.value > 21:
                    # show_all(player, dealer)
                    win_hand(player, dealer, chips)
                elif dealer.value > player.value:
                    # show_all(player, dealer)
                    lose_hand(player, dealer, chips)
                elif dealer.value < player.value:
                    # show_all(player, dealer)
                    win_hand(player, dealer, chips)
                else:
                    # show_all(player, dealer)
                    push(player, dealer, chips)

            # Went all in and lost
            if chips.total == 0:                
                show_all(player, dealer)
                print('\nBANKRUPT')
                print('\nGAME OVER')
                exit()

                    
            # Asks to deal another hand
            else:
                new_game()