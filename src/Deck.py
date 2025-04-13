# Deck class, face cards are considered quantam, other are regular cards

import random
from Card import Card, Suit


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
            cards.append(Card("Queen", suit, True, [-5, 5]))
            cards.append(Card("King", suit, True, [0, 10]))
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        rdealt_cards = [self.cards.pop() for _ in range(num_cards)]

        # Detect and entangle matching quantum face cards
        name_to_quantum_cards = {}

        for card in rdealt_cards:
            if card.is_quantum:
                name_to_quantum_cards.setdefault(card.name, []).append(card)

        for cards in name_to_quantum_cards.values():
            if len(cards) >= 2:
                # Entangle all with the first one
                cards[0].entangle_with(cards[1:])

        return rdealt_cards
