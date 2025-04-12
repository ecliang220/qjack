from enum import Enum
import random


class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Card:
    def __init__(self, name: str, suit: Suit, is_quantum: bool = False, state: list = None):
        """
        Initialize a card.
        
        :param name: Name of the card (e.g., "2", "10", "Ace", "King", etc.)
        :param suit: The card suit, an instance of the Suit enum.
        :param is_quantum: Flag to indicate whether this card is quantum (face card) or classical.
        :param : For quantum cards only, a list of possible integer values for this card.
        """
        self.name = name
        self.suit = suit
        self.is_quantum = is_quantum
        
        if is_quantum:
            # Quantum cards must have a list of possible states provided.
            if state is None or not isinstance(state, list) or not state:
                raise ValueError("Quantum cards must be initialized with a non-empty list of possible values.")
            self.state = state
            self.measured_value = None  # Not measured until later.
        else:
            self.state = None
            self.measured_value = self._calculate_classical_value()

    def _calculate_classical_value(self) -> int:
        """
        Determines the value of a classical card.
        For numeric cards, returns the int value.
        For Ace, returns 11 by default (could be switched to 1 based on game logic).
        For any other face card (when used as classical), uses 10.
        
        :return: Integer value of the card.
        """
        if self.name.isdigit():
            return int(self.name)
        elif self.name.upper() == "ACE":
            return 11  # Default value. Game logic can later adjust Ace as 1 or 11.
        else:
            # For classical face cards (if not chosen as quantum), assume a value of 10.
            return 10

    def get_value(self) -> int:
        """
        Getter for the card's value.
        
        For classical cards, returns the pre-calculated value.
        For quantum cards, returns the measured value if it has been resolved;
        otherwise, raises an error indicating the card has not yet been measured.
        
        :return: The integer value of the card.
        :raises ValueError: If a quantum card has not been measured yet.
        """
        if self.is_quantum:
            if self.measured_value is None:
                raise ValueError("Quantum card not measured yet. Please measure it first.")
            return self.measured_value
        else:
            return self.measured_value

    def measure(self, measurement_result: int = None) -> int:
        """
        "Measures" a quantum card, collapsing its state.
        
        If a measurement_result is provided, it must be one of the possible states;
        otherwise, the method randomly chooses one from the possible states.
        
        For classical cards, measurement simply returns the classical value.
        
        :param measurement_result: Optional explicit value from the possible state.
        :return: The measured integer value of the card.
        :raises ValueError: If the provided measurement_result is not in the card's possible states.
        """
        if not self.is_quantum:
            return self.measured_value

        # If already measured, simply return the value.
        if self.measured_value is not None:
            return self.measured_value

        if measurement_result is not None:
            if measurement_result not in self.state:
                raise ValueError("Provided measurement result is not in the card's possible state.")
            self.measured_value = measurement_result
        else:
            self.measured_value = random.choice(self.state)
        return self.measured_value

    def __str__(self) -> str:
        """
        String representation of the card, showing its name, suit, and either its value or quantum state.
        """
        if self.is_quantum:
            state_info = f"Possible states: {self.state}" if self.measured_value is None else f"Measured value: {self.measured_value}"
            return f"{self.name} of {self.suit.value} [Quantum Card | {state_info}]"
        elif self.name == 'Ace':
            return f"{self.name} of {self.suit.value} [Value: 1 or {self.measured_value}]"
        else:
            return f"{self.name} of {self.suit.value} [Value: {self.measured_value}]"




