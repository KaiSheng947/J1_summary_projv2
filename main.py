import mud
# import data

def show_intro():
    """Display the game intro"""
    ...

def is_gameover():
    """Indicates end of game"""
    ...

def defeat():
    """Display the defeat screen"""
    print("Try again")

def victory():
    """Display the victory screen"""
    print("Congratulations, you've won!")

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