from room import (
    Blackjack,
    Baccarat,
    Poker,
    Room
)


import yaml

with open("text.yaml", "r") as file:
    config = yaml.safe_load(file)


class Game:
    rooms = [Blackjack, Baccarat, ...]
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

    def save_game(self):
        pass

    def quit_game(self):
        pass

    def show_intro():
        """Display the game intro"""
        print(config["text"]["WELCOME"])

    def is_gameover():
        """Indicates end of game"""
        print(config["text"]["EXIT_MSG"])

    def defeat():
        """Display the defeat screen"""
        print(config["text"]["GAME_LOSE"])

    def victory():
        """Display the victory screen"""
        print(config["text"]["GAME_LOSE"])

    

    def play(self) -> None:
        """main game loop
        """
        room_list = ["blackjack", "baccarat", "poker", "russian_roulette"]
        score = 0
        
        #displays intro
        self.show_intro()


        for current_room, room_class in enumerate(self.rooms):
            room = room_class()
            room.show()
            delta_score = room.play(score)
            score += delta_score
            print(config[room_list[current_room]]["GAME_WIN"])
            print(f"Your current score: {score}, ({delta_score} in this room)")
            print(config["TRANSITION"])
            for i in range(5):
                    print(".", end = "", flush = True)
                    time.sleep(0.5)
            print("")          

