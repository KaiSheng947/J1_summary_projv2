import random

# Cards are referenced using a numerical ID
# Ace = 1, ... Jack = 11, ... King =
NAMES = {
    1: "A",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "Jack",
    12: "Queen",
    13: "King" 
}


SUIT_SYMBOL = {
    "DIAMOND": '♦',
    "CLUB": '♣', 
    "HEART": '♥',
    "SPADE": '♠'
}


class Card:
    """Represents a single playing card."""
    def __init__(self, suit: str, value: int):
        self.set_suit(suit)
        self.set_value(value)

    def set_suit(self, suit: str) -> None:
        """Setter for suit
        Checks for validity"""
        assert suit in SUIT_SYMBOL
        self.suit = suit
    
    def set_value(self, value: int) -> None:
        """"Setter for value
        Checks for validity"""
        assert value in NAMES
        self.value = value
        
    def as_string(self) -> str:
        """Returns card value and suit in string form
        Uses ANSI sequences to be highlighted."""
        return f"\033[7m[{NAMES[self.value]} of {SUIT_SYMBOL[self.suit]}]\033[27m"
    
    def same_as(self, other: "Card") -> bool:
        """Checks if this card is equivalent to the other card"""
        return self.as_string() == other.as_string()

def generate_card() -> Card:
    """Randomly generates the values
    and the suit symbol of a card 
    for the class Card 
    """
    random_value = random.randint(1, 13)
    random_suit = random.choice(list(SUIT_SYMBOL.keys()))

    card = Card(random_suit, random_value)
    return card

if __name__ == "__main__":
    card = generate_card()
    print(card.as_string())