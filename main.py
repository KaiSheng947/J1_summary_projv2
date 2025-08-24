import mud
# import data

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