class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.is_bust = False
        self.score = 0
        self.is_sticking = False
        self.measure_used = False

    def add_card(self, card):
        self.hand.append(card)
    
    def measure_hand(self):
        if self.measure_used:
            print("No more peeking!!! :(") 
            return
        self.measure_used = True
        for card in self.hand:
            if card.is_quantum and card.measured_value is None:
                card.measure()

    def calculate_score(self):
        total = 0
        ace_count = 0

        for card in self.hand:
            value = card.measured_value if card.is_quantum else card.get_value()

            if value == 11:
                ace_count += 1
            total += value

        # Handle Ace logic: downgrade to 1 if total exceeds 21
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        self.score = total
        self.is_bust = total > 21
        return self.score
    
    def stick(self):
        self.is_sticking = True

    # For clean printout/logging
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name} | Hand: [{hand_str}] | Score: {self.score} | Bust: {self.is_bust}"