from room import (
    Blackjack,
    Baccarat,
    Poker,
    Room
)

class Game:
    def __init__(self):
        pass

    def get_current_room(self) -> Room:
        pass

    def update(self, outcome):
        pass

    def display_outcome(self):
        pass

    def player_lost(self):
        pass

    def move_to_next_room(self):
        pass

    def is_over(self) -> bool:
        pass