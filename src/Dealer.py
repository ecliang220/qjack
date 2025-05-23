class Dealer:
    #initializes
    def __init__(self):
        self.cards=[]
        self.score=0
        self.is_bust=False

    # adds card to cards
    def add_card(self, card):
        self.cards.append(card)
        self.calculate_score()
        # Check for entanglement opportunity
        if card.is_quantum:
            same_type = [c for c in self.hand if c.name == card.name and c.is_quantum and c != card]
            if same_type:
                card.entangle_with(same_type)

    # calculates dealer score from list of cards
    def calculate_score(self):
        self.score=0
        aces=0
        for card in self.cards:
            self.score+=card.get_value()
            if card.name.upper() == "ACE":
                aces+=1
        while self.score >21 and aces>0:
            self.score-=10
            aces-=1
        self.is_bust=self.score>21
    
    # check in game class, if dealer's score is less than 16 they have to hit
    def isHitting(self):
        return self.score<16
    
    # if dealer's score is > 21 they bust
    def is_bust(self):
        return self.score>21