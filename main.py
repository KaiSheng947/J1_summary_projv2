import mud
# import data

import yaml

with open("text.yaml", "r") as file:
    config = yaml.safe_load(file)

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

def run_game():
    """Runs the game."""
    game = mud.Game()
    game.play()

    # while not game.is_over():
    #     room = game.get_current_room()
    #     room.show()
    #     outcome = room.play()
    #     game.update(outcome)
    #     game.display_outcome()
    #     if not game.player_lost():
    #         game.move_to_next_room()
    # if game.won():
    #     victory()
    # else:
    #     defeat()

if __name__ == "__main__":
    run_game()