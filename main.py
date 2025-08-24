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
    if __name__ == "__main__":
        game = mud.Game()
        show_intro()
        while not game.is_over():
            room = game.get_current_room()
            room.show()
            outcome = room.play()
            game.update(outcome)
            game.display_outcome()
            if not game.player_lost():
                game.move_to_next_room()
        if game.won():
            victory()
        else:
            defeat()
        # mud.welcome()
        # player = data.create_player()
        # game.add_player(player)
        # while not game.is_gameover():
        #     choices = game.get_options()
        #     choice = data.prompt_player_choice(choices)
        #     actions = game.get_actions(choice)
        #     game.execute(actions)
        #     data.display(game.status())
        # mud.epilogue()

run_game()