import unittest
import random

from room import (
    InputOverride,
    Blackjack,
    Baccarat
)

import mud

class TestBlackjack(unittest.TestCase):
    def test_blackjack_initialiser(self):
        """Test that the blackjack object can be constructed"""
        room = Blackjack()

    def test_blackjack_play_random(self):
        """Test-play blackjack with random yes/no"""
        room = Blackjack()
        with InputOverride(lambda _: random.choice(["y", "n"])): 
            score = room.play(0)
        self.assertIsInstance(score, int)
    
    def test_blackjack_play_set(self):
        """Test-play blackjack with all yes, all no and all invalid."""
        room = Blackjack()
        for text in ["y", "n", "THISTEXTISINVALID"]:
            print(f"Currently testing on text {text}")
            with InputOverride(lambda _: text): 
                score = room.play(0)
            self.assertIsInstance(score, int)

class TestBaccarat(unittest.TestCase):
    def test_baccarat_initialiser(self):
        """Test that the baccarat object can be constructed"""
        room = Baccarat()

    def test_baccarat_play_random(self):
        """Test-play baccarat with random Player/Banker/Tie"""
        room = Baccarat()
        with InputOverride(lambda _: random.choice(["Player", "Banker", "Tie"])): 
            score = room.play(0)
        self.assertIsInstance(score, int)
    
    def test_baccarat_play_set(self):
        """Test-play baccarat with all Player, all Banker, all Tie and all invalid."""
        room = Baccarat()
        for text in ["Player", "Banker", "Tie"]:
            print(f"Currently testing on text {text}")
            with InputOverride(lambda _: text): 
                score = room.play(0)
            self.assertIsInstance(score, int)
        
    def test_baccarat_play_invalid(self):
        """Test baccarat on invalid inputs"""
        # Baccarat re-prompts with no progress on invalid text. 
        # Thus, we need to try invalid text then complete the room with valid text.
        testcase = ["THISTEXTISINVALID"] * 20
        def invalid_test_input(_):
            if testcase:
                return testcase.pop()
            else:
                return "Banker" # After testcase, use valid inputs to progress game.

        room = Baccarat()
        with InputOverride(invalid_test_input): 
            score = room.play(0)
        self.assertIsInstance(score, int)

class TestGame(unittest.TestCase):
    def test_intro(self):
        """Test game intro"""
        game = mud.Game()
        game.show_intro()

if __name__ == '__main__':
    unittest.main()