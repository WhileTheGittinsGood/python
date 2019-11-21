import random

ranks = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
suits = ('\u2661', '\u2662', '\u2664', '\u2667')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':0, 'J':0, 'Q':0, 'K':0, 'A':1}

playing = True
bet_placed = False
wager_placed = False

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[self.rank]

    def __str__(self):
        return self.rank + self.suit

class Deck:

    def __init__(self):
        self.deck = []
        for num in range(8):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(rank, suit))

    def __str__(self):
        deck_comp = '\n'
        for card in self.deck:
            deck_comp += ' ' + card.__str__()
        return deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        try:
            
            top_card = self.deck.pop()
            return top_card
        except IndexError:
            random.shuffle(self.deck)

class Hand:

    def __init__(self):
        self.hand = []
        self.value = 0
        self.cards = 0

    def __str__(self):
        hand_comp = '\n'
        
        for card in self.hand:
            hand_comp += ' ' + card.__str__()

        return hand_comp

    def add(self, card):
        self.hand.append(card)
        self.value += values[card.rank]
        self.value = self.value % 10
        self.cards += 1

class Chips:

    def __init__(self, total=100):
        self.total = total
        self.wager = 0
        self.bet = ' '

    def win_wager(self):
        self.total += self.wager

    def lose_wager(self):
        self.total -= self.wager

def deal_hand(player, banker, deck):

    for num in range(4):
        if num % 2 == 0:
            player.add(deck.deal())
        else:
            banker.add(deck.deal())

# def extra_card(hand, deck):

#     hand.add(deck.deal())

def player_or_banker(chips):

    global bet_placed

    while not bet_placed:
        chips.bet = input('(p)layer or (b)anker: ')

        try:
            if chips.bet[0].lower() == 'p':
                chips.bet = 'player'
                bet_placed = True
            elif chips.bet[0].lower() == 'b':
                chips.bet = 'banker'
                bet_placed = True
            else:
                continue
        except:
            print('error')

    print(chips.bet)

def ante_up(chips):

    global wager_placed
    prompt = f'ante up, you have {chips.total} chips: '

    while not wager_placed:
        try:
            chips.wager = int(input(prompt))
        except:
            prompt = f'enter an integer, you have {chips.total}'
        else:
            if chips.wager > chips.total:
                prompt = f'max wager {chips.total}'
            else:
                print(f'wager is {chips.wager}')
                wager_placed = True



def player_win(chips):

    print('player wins')
    if chips.bet == 'player':
        chips.win_wager()
    else:
        chips.lose_wager()

def banker_win(chips):

    print('banker wins')
    if chips.bet == 'banker':
        chips.win_wager()
    else:
        chips.lose_wager()

def check_deal(player, banker, deck):

    def extra_card(hand, deck):

        hand.add(deck.deal())

    def win_check(player, banker):

        if player.value > banker.value:
            if player.cards == 2 and banker.cards == 2:
                print('player natural')
            else:
                print('player wins')
        elif player.value < banker.value:
            if player.cards == 2 and banker.cards == 2:
                print('banker natural')
            else:
                print('banker wins')
        else:
            print('tie hand')

        playing = False

    if player.cards == 2 and banker.cards == 2:
        if player.value >= 8 or banker.value >= 8:
            win_check(player, banker)
        else:
            if player.value < 6:
                extra_card(player, deck)

    else:
        
        if banker.cards == 2:
            if banker.value <= 2:
                extra_card(banker, deck)
            elif banker.value == 3:
                if player.value != 8:
                    extra_card(banker, deck)
                else:
                    pass
            elif banker.value == 4:
                if player.value in range(2,8):
                    extra_card(banker, deck)
                else:
                    pass
            elif banker.value == 5:
                if player.value in range(4,8):
                    extra_card(banker, deck)
                else:
                    pass
            elif banker.value == 6:
                if player.value in range(6,8):
                    extra_card(banker, deck)
                else:
                    win_check(player, banker)
            else:
                win_check(player, banker)
        else:
            win_check(player, banker)


deck = Deck()
# print(deck)
deck.shuffle()
# print(deck)

player = Hand()
banker = Hand()
chips = Chips()

player_or_banker(chips)
ante_up(chips)

deal_hand(player, banker, deck)

print(f'Player: {player.value}{player}')
print(f'Banker: {banker.value}{banker}')
check_deal(player, banker, deck)

print(f'Player: {player.value}{player}')
print(f'Banker: {banker.value}{banker}')
check_deal(player, banker, deck)

print(f'Player: {player.value}{player}')
print(f'Banker: {banker.value}{banker}')
check_deal(player, banker, deck)
