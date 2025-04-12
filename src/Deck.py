# Deck class, face cards are considered quantam, other are regular cards

class Deck:
    def __init__(self):
        self.cards = self._generate_deck()

    def _generate_deck(self):
        cards = []
        for suit in Suit:
            for i in range(2, 11):
                cards.append(Card(str(i), suit))
            cards.append(Card("Ace", suit))
            cards.append(Card("Jack", suit, True, [1, 11]))
            cards.append(Card("Queen", suit, True, [5, -5]))
            cards.append(Card("King", suit, True, [10, 0]))
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
