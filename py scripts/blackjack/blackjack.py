import random
import log

# Global variables to decide if the game is being played or if the deck needs to be shuffled
playing = True
reshuffle = False
game_start = True
doubled = False

hands_dealt_total = 0
hands_dealt_shoe = 0

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
        random.shuffle(self.deck)
        print('The deck has been shuffled.')
            
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

    def split(self):
        split_card = self.hand.pop()
        return split_card

# This class creates a chips object to be assigned to the players hand.
class Chips:
    
    def __init__(self,total=100):
        self.total = total
        self.bet = 0
        self.insurance = 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet
        
    def blackjack(self):
        self.total += (self.bet * 1.5)
        self.total = round(self.total)

    def double_down(self):
        if self.bet * 2 < self.total:
            self.bet *= 2
        else:
            self.bet = self.total

    def win_in(self):
        self.total += (self.insurance * 2)

    def lose_in(self):
        self.total -= self.insurance

# This function asks the user for their wager until the user enters an integer that is less than or equal to
# the value of their chips
def take_bet(chips):    
    prompt = f'Place your wager, you have {chips.total} chips: '
    while True:
        try:
            chips.bet = int(input(prompt))       
        except:
            prompt = f'Enter an integer, you have {chips.total} chips:'  
        else:            
            if chips.bet > chips.total:
                prompt = f'You only have {chips.total} chips to wager:'
            elif chips.bet < 1:
                prompt = f'Wager must be a positive amount, you have {chips.total}:'
            
            else:
                break

# Deals 4 cards alternating from the player to the dealer 
def deal(player, dealer, deck):    
    global hands_dealt_total
    global hands_dealt_shoe
    for num in range(4):
        if num % 2 == 0:
            player.add_card(deck.deal())
        else:
            dealer.add_card(deck.deal())
    hands_dealt_total += 1
    hands_dealt_shoe += 1
    player.ace_adjust()
    dealer.ace_adjust()

def double_down(chips, deck, hand):
    global doubled
    global playing
    while True:
        try:
            n = input('Would you like to double down and hit, (y)es or (n)o? ')
        
            if n[0].lower() == 'y':
                chips.double_down()
                hit(deck, hand)
                doubled = True
                playing = False
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

# Function executes when the deallers face up card is an A
# Insurance is 1/2 of the wager and pays 2:1
def insurance(chips):

    while True:
        i = input('Would you like insurance against dealer blackjack, (y)es or (n)o?')
        try:
            if i[0].lower() == 'y':
                chips.insurance = chips.bet/2
                chips.insurance = round(chips.insurance)
                break
            elif i[0].lower() == 'n':
                break
            else:
                continue
        except:
            print('Enter (y)es or (n)o')

# If the player has already played a hand this function will ask if you
# would like to repeat the same wager
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
                if chips.bet <= chips.total:
                    chips.bet = chips.bet
                else:
                    chips.bet = chips.total
                break
            elif r[0].lower() == 'n':
                take_bet(chips)
                break
            else:
                continue
        except:
            print('Enter (y)es or (n)o')

# This function will be used in the victory condtion functions that follow.
# It has been added to visually simplify the game in terminal.
def proceed():
    while True:
        p = input('Continue? ')
        break

# The following functions are used when either player or dealer reach a victory condition.
# The functions print out the winner and adjust the players chips accordingly.
def blackjack(chips):
    proceed()
    print(f'Blackjack! Win {round(chips.bet * 1.5)} chips.\n')
    chips.blackjack()
    print(f'{chips.total} chip(s) in bank.')

def win_hand(chips):
    proceed()
    print(f'Win {chips.bet} chip(s).\n')
    chips.win_bet()
    print(f'{chips.total} chip(s) in bank.')

def lose_hand(chips):
    proceed()
    print(f'Lose {chips.bet} chip(s).\n')
    chips.lose_bet()
    print(f'{chips.total} chip(s) in bank.')
    
def push(chips):
    proceed()
    print('Push.\n')
    print(f'{chips.total} chip(s) in bank.')

def win_insurance(chips):
    print(f'Win insurance: {chips.insurance*2}')
    chips.win_in()
    playing = False

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

# This function is ran after a hand is finished
# If the deck has less cards remaining than specified
# by its num variable it will set the reshuffle boolean
# to True else it will set the playing boolean to true
def shuffle_check(deck):
    global reshuffle
    global playing
    global hands_dealt_shoe

    num = 20

    if len(deck.deck) < num:
        reshuffle = True
        hands_dealt_shoe = 0
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
                playing = False
                break
            else:
                continue
        except:
            print('Enter (y) or (n)')


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

            dealer = Hand()
            player = Hand()            
            
            if chips.bet == 0:
                take_bet(chips)
            else:
                #print(f'Playing = {playing}') debug
                repeat_bet(chips)

            deal(player, dealer, deck)
            print(f'Total hands dealt: {hands_dealt_total} Hands this shoe: {hands_dealt_shoe}')
                
            # Player was dealt a blackjack
            if player.value == 21:
                show_all(player, dealer)
                blackjack(chips)
                continue

            if dealer.hand[1].value == 11:
                show_deal(player, dealer)
                insurance(chips)
                show_all(player, dealer)
                if dealer.value == 21:
                    if chips.insurance > 0:
                        win_insurance(chips)
                        lose_hand(chips)
                        continue
                    else:
                        lose_hand(chips)
                        continue
                else:
                    if chips.insurance > 0:
                        chips.lose_in()
                        print(f'Lose insurance bet of {chips.insurance}')

            if player.value == 11:
                show_deal(player, dealer)
                double_down(chips, deck, player)
            

            # Player was dealt anything except blackjack
            while playing and player.value < 21:

                if dealer.hand[1].value == 11:
                    show_all(player, dealer)
                else:
                    show_deal(player, dealer)

                # Asks player if they want to hit or stay
                hit_or_stay(deck, player)

                # Player hit and busts
                if player.value > 21:
                    if dealer.hand[1].value == 11:
                        show_all(player, dealer)
                        lose_hand(chips)
                        break
                    else:
                        show_deal(player, dealer)
                        lose_hand(chips)
                        break

            # Player stays
            if player.value <= 21:
                
                while dealer.value < 17:
                    hit(deck, dealer)

                show_all(player, dealer)

                if dealer.value > 21:
                    # show_all(player, dealer)
                    win_hand(chips)
                elif dealer.value > player.value:
                    # show_all(player, dealer)
                    lose_hand(chips)
                elif dealer.value < player.value:
                    # show_all(player, dealer)
                    win_hand(chips)
                else:
                    # show_all(player, dealer)
                    push(chips)

            # Went all in and lost
            if chips.total < 1:                
                #show_all(player, dealer)
                print('\nBANKRUPT')
                print('\nGAME OVER')
                exit()
                    
            # Asks to deal another hand
            else:
                new_game()
                if not playing:
                    exit()