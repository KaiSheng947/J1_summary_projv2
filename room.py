import cards

class Room:
    """Parent class of all rooms. 
    Each room has a specific game."""
    def __init__(self):
        self.points = 0
        self.player_score = 0
        self.bot_score = 0

class Blackjack(Room):
    """Room with blackjack.
    Implements the blackjack game"""
    VALUES = { # Card values for this game.
        1: 11, # Ace starts at 11 for blackjack
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8,
        9: 9,
        10: 10,
        11: 10, # Jack
        12: 10, # Queen
        13: 10  # King
    }
   
    def __init__(self):
        super().__init__()
        
    
    def show(self) -> None:
        """Display room info and rules"""
        print("Blackjack room (placeholder)")

    def draw_card(self) -> cards.Card:
        """Randomly generates the values
        and the suit symbol of a card 
        for the class Card 
        """
        # Not simulating a deck; just generating
        # random cards
        return cards.generate_card()

    def hand_value(self):
        """Calculate value of cards"""
        sum()

    def play(self):
        """TODO: docstring"""
        while self.player_score < 3:
            player_hand = [self.draw_card(), self.draw_card()]
            bot_hand = [self.draw_card(), self.draw_card()]

class Baccarat(Room):
    """Room with Baccarat.
    Implements the Baccarat Game"""
    def __init__(self):
        super().__init__()
        self.VALUES = 
    
    def show(self) -> None:
        """Display room info."""
        print("Baccarat room (placeholder)")

    def play(self):
        pass

class Poker(Room):
    """Room with Poker.
    Implements the Poker Game"""
    def __init__(self):
        super().__init__()

    def show(self) -> None:
        """Display room info."""
        print("Poker room (placeholder)")

    def play(self):
        pass

