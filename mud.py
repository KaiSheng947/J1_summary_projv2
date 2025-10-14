import config
from room import (
    Blackjack,
    Baccarat,
    Poker,
    Roulette,
    Room
)


class Game:
    rooms: list[type[Room]] = [Blackjack, Baccarat, Poker, Roulette] # Note: supposed to have poker lol

    def show_intro(self):
        """Display the game intro"""
        print(config.text["WELCOME"])

    def is_gameover(self):
        """Indicates end of game"""
        print(config.text["EXIT_MSG"])

    def defeat(self):
        """Display the defeat screen"""
        print(config.text["GAME_LOSE"])

    def victory(self):
        """Display the victory screen"""
        print(config.text["GAME_WIN"])

    

    def play(self) -> None:
        """main game loop
        """
        room_list = ["blackjack", "baccarat", "poker", "russian_roulette"]
        score = 0

        #displays intro
        self.show_intro()
        score = 0
        for idx, room_class in enumerate(self.rooms):
            room = room_class()
            room.show()
            delta_score = room.play(score)
            score += delta_score
            
            # Dont show for last room.
            # Last room handles game win/gameover
            if idx != len(self.rooms) - 1:
                print(f"You've completed this trial...")
                print(f"Your current score: {score}, ({delta_score} in this room)")
