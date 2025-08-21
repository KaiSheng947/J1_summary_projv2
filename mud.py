from room import (
    Blackjack,
    Baccarat,
    Poker,
    Room
)

class Game:
    rooms = [Blackjack, Baccarat, ...]
    def __init__(self):
        pass

    def show_intro(self) -> None:
        """Show the intro message to the game"""
        print("Welcome to the \033[1;5;4;3;31md u n g e o n\033[0m")
        print("Hope you get through your three trials...")
    
    def play(self) -> None:
        self.show_intro()
        score = 0
        for room_class in self.rooms:
            room = room_class()
            delta_score = room.play(score)
            print(f"You've completed this trial...")
            print(f"Your current score: {score}, ({delta_score} in this room)")