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
        # Check for entanglement opportunity
        if card.is_quantum:
            same_type = [c for c in self.hand if c.name == card.name and c.is_quantum and c != card]
            if same_type:
                card.entangle_with(same_type)
    
    def measure_hand(self):
        self.measure_used = True
        for card in self.hand:
            if card.is_quantum and card.measured_value is None:
                card.measure()

    def calculate_score(self):
        total = 0
        ace_count = 0

        for card in self.hand:
            if card.is_quantum:
                if card.measured_value == None:
                    value = card.get_quatum_low_value()
                else: value = card.measured_value
            else: value = card.get_value()
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
    
    def calculate_tentative_score(self):
        total = 0
        ace_count = 0

        for card in self.hand:
            if card.is_quantum:
                if card.measured_value == None:
                    continue
                else: value = card.measured_value
            else: value = card.get_value()
            if value == 11:
                ace_count += 1
            total += value

        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return total
    
    def stick(self):
        self.is_sticking = True

    # For clean printout/logging
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name} | Hand: [{hand_str}] | Score: {self.score} | Bust: {self.is_bust}"