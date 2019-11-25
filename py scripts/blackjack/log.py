import blackjack

hands_dealt_total = 0
hands_dealt_shoe = 0
shoes_dealt_total = 0

class Complete_Hand:
    
    def __itit__(self, hands_dealt_total, hands_dealt_shoe, dealer, player, wager, doubled, insurance, winner):
        self.hand_id = f'hand_id# {hands_dealt_total}-{hands_dealt_shoe}'
        self.cards_dealt = 0
        self.dealer = dealer
        self.player = player
        self.wager = wager
        self.doubled = False
        insurance = False
        winner = False