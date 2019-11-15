import random
from IPython.display import clear_output as clear
from time import sleep

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
    
    global shuffle_deck
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
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
            shuffle_deck = False
            
    def deal(self):
        
        try:
            top_card = self.deck.pop()
            return top_card
        except IndexError:
            shuffle_deck = True

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
        
    def blackjack(self):
        self.total += self.bet * 1.5

# This function asks the user for their wager until the user enters an integer that is less than or equal to
# the value of their chips

def take_bet(chips):
    
    prompt = f'Place your wager, you have {chips.total} chips:'
    
    while True:
        
        try:
            chips.bet = int(input(prompt + '\n'))
            clear(wait=True)
        
        except:
            prompt = f'Please enter an integer, you have {chips.total} chips:'
            clear(wait=True)
        
        else:
            
            if chips.bet > chips.total:
                prompt = f'Sorry, you only have {chips.total} chips to wager:'
            elif chips.bet < 1:
                prompt = f'Wager must be a positive amount, you have {chips.total}:'
            
            else:
                print(f'You wagered {chips.bet} chip(s).')
                break

# Simple function that takes the deck and a hand as a parameter and adds a card from the deck that is passed
# to the card that is passed.

def hit(deck, hand):
    
    hand.add_card(deck.deal())
    hand.ace_adjust()

# This is repeated after the hand is dealt to ask the player if they would like to hit or stay

def hit_or_stay(deck, hand):
    
    global playing
    
    while True:
        #h = input(f'You have {hand.value}. Would you like to (h)it or (s)tay?')
        h = input('Would you like to (h)it or (s)tay?\n')
        
        try:
            if h[0].lower() == 'h':
                hit(deck, hand)
            elif h[0].lower() == 's':
                print('Player stays.')
                playing = False
            else:
                continue
            break
        except:
            continue
            
    print(f'You have {hand.value}.')

# The following functions are used when either player or dealer reach a victory condition.
# The functions print out the winner and adjust the players chips accordingly.

def player_blackjack(player, dealer, chips):
    
    print('Blackjack!')
    chips.blackjack()

def player_bust(player, dealer, chips):
    
    print('Player bust')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    
    print('Player wins')
    chips.win_bet()

def dealer_bust(player, dealer, chips):
    
    print('Dealer bust, Player wins')
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    
    print('Dealer wins')
    chips.lose_bet()
    
def push(player, dealer, chips):
    
    print('Push')

# The following functions are used after cards are dealt to display the cards

def show_none():

    print(f'\nDealer:')
    print('\n')
    print('')
    
    print(f'\nPlayer:')
    print('\n')
    print('')

def show_deal(player, dealer):
    
    print(f'\nDealer shows: {dealer.hand[1].value}')
    print('\nXX ')
    print(dealer.hand[1])
    
    print(f'\nPlayer has: {player.value}')
    print('\n' + player.__str__())

def show_all(player, dealer):
    
    print(f'\nDealer has: {dealer.value}')
    print('\n' + dealer.__str__())
    
    print(f'\nPlayer has: {player.value}')
    print('\n' + player.__str__())

def deal(player, dealer, deck):
    
    for num in range(4):
        if num % 2 == 0:
            player.add_card(deck.deal())
        else:
            dealer.add_card(deck.deal())

def shuffle_check(deck):
    
    global shuffle_deck
    
    try:
        deck.deck[0]
    except IndexError:
        print('No more cards in the deck. Resuffle')
        shuffle_deck = True
    else:
        pass

while True:
    
    #print('Welcome to Blackjack!')
    
    playing = True
    clear(wait=True)
    
    deck = Deck()
    deck.shuffle()
    
    chips = Chips()
    
    #sleep(3)
    
    while not shuffle_deck:
        
        print('Welcome to Blackjack!')
        show_none()
        
        take_bet(chips)

        dealer = Hand()
        player = Hand()

        shuffle_check(deck)
        deal(player, dealer, deck)
        show_deal(player, dealer)
        
        if player.value == 21:
            clear(wait=True)
            player_blackjack(player, dealer, chips)
            show_all(player, dealer)
            break

        while playing:
            
            hit_or_stay(deck, player)
            clear()

            shuffle_check(deck)
            
            print(f'You wagered {chips.bet} chip(s).')
            show_deal(player, dealer)
        
            if player.value > 21:
                clear(wait=True)
                player_bust(player, dealer, chips)
                show_all(player, dealer)
                break

        if player.value <= 21:
            
            while dealer.value < 17:
                hit(deck, dealer)
                shuffle_check(deck)
                clear(wait=True)
                print(f'You wagered {chips.bet} chip(s).')
                show_all(player, dealer)
                

            if dealer.value > 21:
                clear(wait=True)
                dealer_bust(player, dealer, chips)
                show_all(player, dealer)
            elif dealer.value > player.value:
                clear(wait=True)
                dealer_wins(player, dealer, chips)
                show_all(player, dealer)
            elif dealer.value < player.value:
                clear(wait=True)
                player_wins(player, dealer, chips)
                show_all(player, dealer)
            else:
                clear(wait=True)
                push(player, dealer, chips)
                show_all(player, dealer)

        if chips.total == 0:
            
            t = 10
            
            while t > -1:
                clear(wait=True)
                print('\nYou have no more chips.')
                show_all(player, dealer)
                print(f'\nGAME OVER {t}')
                sleep(1)
                t -= 1

            break
            # new_game = input('Play another hand, (y)es or (n)o?\n')
            # clear(wait=True)

            # if new_game[0].lower() == 'y':
            #     playing = True
            #     shuffle_deck = True
            #     continue
            # else:
            #     print('exiting')
            #     break
                
        else:
            new_game = input('Play another hand, (y)es or (n)o?\n')
            clear(wait=True)

            if new_game[0].lower() == 'y':
                playing = True
                continue
            else:
                print('exiting')
                break
    
        break
    break

shuffle_deck = False