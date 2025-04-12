from Dealer import Dealer
from Deck import Deck
from Player import Player


class Game:
    def __init__(self):
        self.player = Player('Bob the Builder')
        self.dealer = Dealer()
        self.deck = Deck()
        self.deck.shuffle()

    def play_round(self):
        # Initial deal
        self.player.hand = self.deck.deal(2)
        self.dealer.cards = self.deck.deal(2)

        # Player turn
        while True:
            self.print_game_state()
            action = input("Hit, Stick, or Peek? (h/s/p): ").lower()
            if action == 'h':
                if (self.player.calculate_score() > 21):
                    break
                else:
                    self.player.add_card(self.deck.deal(1)[0])
            elif action == 's':
                break
            elif action == 'p':
                self.player.measure_hand()
            self.player.calculate_score()

        self.player.measure_hand()
        self.player.calculate_score()

        # Dealer turn
        for card in self.dealer.cards:
            if card.is_quantum:
                card.measure()
        self.dealer.calculate_score()

        while self.dealer.isHitting():
            new_card = self.deck.deal(1)[0]
            if new_card.is_quantum:
                new_card.measure()
            self.dealer.cards.append(new_card)
            self.dealer.calculate_score()


        print("-----------------------------------------")
        if not self.player.measure_used: self.player.measure_hand()
        self.print_game_state()
        self.evaluate_winner()

    def evaluate_winner(self):
        print("\nFinal Scores:")
        print(f"Player: {self.player.score} ({'Bust' if self.player.is_bust else 'Safe'})")
        print(f"Dealer: {self.dealer.score} ({'Bust' if self.dealer.is_bust else 'Safe'})")

        if self.player.is_bust:
            print("Dealer wins!")
        elif self.dealer.is_bust:
            print("Player wins!")
        elif self.player.score > self.dealer.score:
            print("Player wins!")
        elif self.player.score < self.dealer.score:
            print("Dealer wins!")
        else:
            print("It’s a tie!")

    def print_game_state(self):
        print("\nPlayer's Hand:")
        for card in self.player.hand:
            print(f" - {card}")
        print("\nDealer's Visible Card:")
        print(f" - {self.dealer.cards[0]}")