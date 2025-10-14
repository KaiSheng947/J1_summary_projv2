from typing import Callable, Literal

import cards
import config
import random
import text


class InputOverride:
    def __init__(self, override):
        self.original = None
        self.override = override
    
    def __enter__(self):
        global INPUT_FUNCTION
        self.original = INPUT_FUNCTION
        INPUT_FUNCTION = self.override
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        global INPUT_FUNCTION
        INPUT_FUNCTION = self.original

INPUT_FUNCTION: Callable[[object], str] = input
def prompt(question: str) -> str:
    """This function behaves the same as input().
    The pattern is to allow for automated testing."""
    return INPUT_FUNCTION(question)


def prompt_choice(
        question: str,
        choices: list[str],
        reprompt_on_error: bool = True,
        error_msg: str = "Invalid choice, try again.",
        separator: str = "/"
    ) -> str:
    """Prompt the user to choose from a list of choices.
    
    Choices are displayed inline
    """
    prompt_str = f"{question} ({separator.join(choices)}): "
    choice = prompt(prompt_str)
    while reprompt_on_error and choice not in choices:
        text.display_line(error_msg)
        choice = prompt(prompt_str)
    return choice


def prompt_continue(
        prompt_text: str = "[Press enter to continue]"
) -> None:
    """Prompt the user to press enter to continue."""
    prompt(prompt_text)

class Room:
    """Parent class of all rooms. 
    Each room has a specific game."""
    name: str

    def __init__(self):
        self.points = 0
        self.player_score = 0
        self.bot_score = 0

    def play(self, score: int = 0) -> int:
        """Plays the room. Returns the score gain/loss due to the game.
        Eg. if you gained 20, return 20. If you lost 20, return -20."""
        raise NotImplementedError("play() must be implemented in the subclass.")

    def show(self) -> None:
        """Show info about this room"""
        prompt_continue()
        text.clear_previous_line()
        text.display_line(config.rooms[self.name]["description"])
        text.wait_visible(5)
        text.display_line(config.rooms[self.name]["rules"])


class Blackjack(Room):
    """Room with blackjack.
    Implements the blackjack game"""
    name = "blackjack"
    VALUES = {
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

    def draw_card(self, hand: list[cards.Card], num: int = 1) -> cards.Card:
        """Draw a card from the deck and add to hand.
        
        Returns the last card drawn.
        """
        # Not simulating a deck; just generating
        for _ in range(num):
            card = cards.create_random_card()
            hand.append(card)
        return hand[-1]

    def calculate_hand_value(self, hand: list[cards.Card]) -> int:
        """Calculates value of hand"""
        total = 0
        aces = 0
        for card in hand:
            total += self.VALUES[card.value]
            # Account for aces as it can be 11 or 1
            if card.value == 1:
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def show_hand(self, owner: str, hand: list[cards.Card]) -> None:
        """displays the hand bot and player have"""
        text.display_line(f"{owner} hand: {', '.join(card.as_string() for card in hand)}")
        text.display_line(f"{owner} Total: {self.calculate_hand_value(hand)}")
    
    def bot_turn(self, hand: list[cards.Card]) -> None:
        """Handles the bot's turn"""
        while 17 < self.calculate_hand_value(hand) < 21:
            self.draw_card(hand)
            self.show_hand('Bot', hand)
            text.linebreak()
    
    def player_turn(self, hand: list[cards.Card]) -> None:
        """Handles the player's turn"""
        while len(hand) < 5 and self.calculate_hand_value(hand) <= 21:
            redraw = prompt_choice(
                'Do you want to draw again?',
                choices=['y', 'n']
            )
            if redraw == 'y':
                self.draw_card(hand)
                self.show_hand('Your', hand)
            else:
                break

    def play_round(self) -> tuple[list[cards.Card], list[cards.Card]]:
        """play one round of blackjack and return player and bot hands"""
        player_hand, bot_hand = [], []
        self.draw_card(player_hand, 2)
        self.draw_card(bot_hand, 2)
        text.display_line(f"Bot 1st card: {bot_hand[0].as_string()}")
        text.linebreak()
        # Player turn
        self.show_hand('Your', player_hand)
        self.player_turn(player_hand)
        text.linebreak()        
        # Bot turn
        self.bot_turn(bot_hand)
        self.show_hand('Bot', bot_hand)
        return player_hand, bot_hand

    def check_outcome(self,
                      player_hand: list[cards.Card],
                      bot_hand: list[cards.Card]) -> str:
        """Check the outcome of the game and return result string"""
        player_total = self.calculate_hand_value(player_hand)
        bot_total = self.calculate_hand_value(bot_hand)
        if player_total > 21 and bot_total > 21:
            self.points += 100
            return "Both bust! You win 100 points"
        elif bot_total > 21:
            self.points += 100
            return "Bot busts! You win 100 points"
        elif player_total > 21:
            self.points -= 20
            return "You bust! You lose 20 points."
        elif player_total == bot_total:
            self.points -= 20
            return "Tie! You lose 20 points!"
        elif player_total > bot_total:
            self.points += 100
            return "You win 100 points!"
        else:
            self.points -= 20
            return "You lose 20 points!"
    
    def play(self, score: int = 0) -> int:
        """Plays blackjack 3 rounds"""
        for i in range(3):
            text.linebreak()
            text.display_span(f'Round {i+1}! ')
            prompt_continue()
            player_hand, bot_hand = self.play_round()
            result = self.check_outcome(player_hand, bot_hand)
            text.display_line(result)
            text.linebreak()
        return self.points

class Baccarat(Room):
    """Room with Baccarat.
    Implements the Baccarat Game"""
    name = "baccarat"

    VALUES = { # Card values for this game.
        1: 1, 
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
    def _init_(self):
        super().__init__()

    def check_outcome(self,
                      player_hand: list[cards.Card],
                      banker_hand: list[cards.Card]) -> str:
        """Check the outcome of the game and return outcome string"""
        player_value = self.calculate_value_of_hand(player_hand)
        banker_value = self.calculate_value_of_hand(banker_hand)
        if player_value > banker_value:
            return "Player"
        elif player_value < banker_value:
            return "Banker"
        else:
            return "Tie"

    def draw_card(self, hand: list[cards.Card], num: int = 1) -> cards.Card:
        """Draw a card from the deck and add to hand.
        
        Returns the last card drawn.
        """
        # Not simulating a deck; just generating
        for _ in range(num):
            card = cards.create_random_card()
            hand.append(card)
        return hand[-1]

    def handle_bet(self, bet: str, outcome: str) -> int:
        """Handles the bet and returns points gained/lost"""
        if bet == outcome:
            self.display_win()
            if outcome == "Tie":
                return 150  # Tie pays more
            else:
                return 100
        else:
            self.display_loss()
            return -100

    def play(self, score: int = 0) -> int:
        """Baccarat game - rules:
        There will be 2 hands dealt out called Player and Banker.
        The person betting can choose whether to bet on Player, Banker, Tie.
        Each hand will have a value calculated from the 2 cards. The winning hand
        will be the hand in which its value is closest to nine. The other result is a Tie.
        Hence, the player is essentially betting on the outcome of the comparison between both hands. 
        Another rule is natural 8 and 9s. If either or both hands have natural 8s or 9s, 
        the comparison will be made there. If there are no natural 8s or 9s, a third card will be drawn.
        The comparison will be made then and the game loops.
        """
        points = 0
        rounds = 1
    
        while rounds <= 3:
            text.display_line(f"Current Points: {points}")
            text.display_line(f"Current Round: {rounds}")
            bet = prompt_choice(
                "What would you like to wager on?",
                choices=["Player", "Banker", "Tie"]
            )
            player_hand = cards.create_random_hand(2)
            banker_hand = cards.create_random_hand(2)
            text.display_line("Player's hand and value")
            self.display_hand(player_hand)
            text.display_line("Banker's hand and value")
            self.display_hand(banker_hand)

            # early win condition check
            player_value = self.calculate_value_of_hand(player_hand)
            banker_value = self.calculate_value_of_hand(banker_hand)
            if banker_value >= 8 or player_value >= 8:
                outcome = self.check_outcome(player_hand, banker_hand)
                points += self.handle_bet(bet, outcome)
            else:
                # slows the game down to show that game has not ended
                text.display_line("No natural 8s or 9s!")
                text.wait_visible(seconds=2.5, interval=0.5)
                # draw 3rd card
                self.draw_card(player_hand)
                self.draw_card(banker_hand)
                self.display_hand(player_hand)
                self.display_hand(banker_hand)

                outcome = self.check_outcome(player_hand, banker_hand)
                points += self.handle_bet(bet, outcome)
            rounds += 1        
        return points

    def calculate_value_of_hand(self, hand: list[cards.Card]) -> int:
        """calculates the values of the player's or dealer's hand
        based on baccarat values
        """
        total_value = 0
        for card in hand:
            total_value += self.VALUES[card.value]
        total_value = total_value % 10
        return total_value

    def display_loss(self) -> None:
        """Displays a message when the better loses
        """
        text.display_line("You lost!")

    def display_win(self) -> None:
        """Displays a message when the better wins
        """
        text.display_line("You won!")

    def display_hand(self, hand: list[cards.Card]) -> None:
        """displays both the Player's and Banker's Hand,
        hand1 and value1 are the Player's hands and hand's value respectively,
        hand2 and value2 are the Banker's hands and hand's value respectively.
        """
        for card in hand:
            text.display_line(card.as_string())
        text.display_line(str(self.calculate_value_of_hand(hand)))


class Poker(Room):
    """
    Room 3 - poker (for kids)
    the player and dealer both receives three cards each
    then their hands are compared to find the winning hand

    high card - worst outcome, but the highest value card wins, 
    occurs when all cards have different values (1,2,3)
    the winning hand has the higher value card (A -> K -> Q -> ... -> 2)

    pair - when 2 cards have the same number value (like two 7's)

    three of a kind - when all 3 cards have the same number value (like three 5's)

    winning hand: three of a kind -> pair -> high card
    """
    name = "poker"
    VALUES = {
        1: 14,   # Ace counts as highest
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8,
        9: 9,
        10: 10,
        11: 11,  # Jack
        12: 12,  # Queen
        13: 13,  # King
    }

    def __init__(self):
        super().__init__()  # initialize points, player_score, bot_score
        self.deck = cards.create_deck()

    def _count_hand(self, hand: list[cards.Card]) -> dict[int, int]:
        """Counts occurrences of each card value in hand"""
        counts = {}
        for card in hand:
            counts[card.value] = counts.get(card.value, 0) + 1
        return counts

    def _deal_cards(self, num=3) -> list[cards.Card]:
        """deals num cards to player and dealer"""
        # Sort hand by card value descending
        hand = sorted(
            [self.deck.pop() for _ in range(num)],
            key=lambda c: c.value,
            reverse=True
        )
        return hand

    def _evaluate_hand(self, hand: list[cards.Card]) -> tuple[int, str, list[int]]:
        """Calculates the value for poker hands using the simplified rules.
        
        Returns a tuple of (score, description, ranks) where:
        - score: int, the score value of the hand (higher is better)
        - description: str, a textual description of the hand
        - ranks: list[int], a list of card ranks used for tie-breaking
        """
        _counts = self._count_hand(hand)
        # Sort counts by poker value descending
        sorted_counts = {
            card_value: _counts[card_value]
            for card_value in sorted(
                _counts,
                key=lambda c_value: self.VALUES[c_value],
                reverse=True
            )
        }

        for card_value, card_count in sorted_counts.items():
            # Three of a kind case
            if card_count == 3:
                return (
                    35,
                    f"Three of a kind ({cards.NAMES[card_value]})",
                    [self.VALUES[card_value]]
                )
            # Pair case
            elif card_count == 2:
                pair_counts = {
                    card_value: count
                    for card_value, count in sorted_counts.items()
                    if count == 2
                }
                largest_pair_value = list(pair_counts.keys())[0]
                return (
                    25,
                    f"Pair of {cards.NAMES[largest_pair_value]}s",
                    [
                        self.VALUES[card_value]
                        for card_value in sorted_counts.keys()
                    ]
                )

        # High card case
        largest_single_value = list(sorted_counts.keys())[0]
        return (
            15,
            f"High card {cards.NAMES[largest_single_value]}",
            list(sorted_counts.keys())
        )

    def _reset_deck(self) -> None:
        """Resets and shuffles the deck"""
        self.deck = cards.create_deck()
        random.shuffle(self.deck)

    def display_hand(self, hand: list[cards.Card]) -> None:
        """Displays the player's hand"""
        text.display_line(" ".join([c.as_string() for c in hand]))

    def take_turn(self, owner: str, hand: list[cards.Card]) -> tuple[int, str, list[int]]:
        """Handles a turn for either the player or the bot"""
        if owner == "Bot":
            text.display_span("Bot's hand: ")
            self.display_hand(hand)
        else:
            text.display_span("Your hand: ")
            self.display_hand(hand)
        return self._evaluate_hand(hand)

    def check_outcome(self,
                      player_score: int,
                      bot_score: int,
                      player_ranks: list[int],
                      bot_ranks: list[int]) -> int:
        """Check the outcome of the game and display result.
        
        Return the net points gained by the player.
        """
        if player_score > bot_score:
            text.display_line(f"You win this round! (+{player_score})")
        elif bot_score > player_score:
            text.display_line(f"Bot wins this round! (+{bot_score} to bot)")
        else:
            # tie-breaker by ranks
            if player_ranks > bot_ranks:  # Python compares lists lexicographically
                text.display_line(
                    f"You win this round on high card! (+{player_score})"
                )
            elif bot_ranks > player_ranks:
                text.display_line(
                    f"Bot wins this round on high card! (+{bot_score} to bot)"
                )
            else:
                text.display_line(
                    f"This round is a tie! (+{player_score} each)"
                )
        return player_score - bot_score

    def play(self, score: int = 0) -> int:
        """Plays one round of poker. Updates player_score and bot_score.
        Returns net points gained by the player (player_score - bot_score)."""
        self._reset_deck()
        text.linebreak()
        text.display_line("--- Poker Round ---")
        bot_hand = self._deal_cards(3)
        bot_score, bot_desc, bot_ranks = self.take_turn("Bot", bot_hand)
        prompt_continue("Press enter to draw...")
        player_hand = self._deal_cards(3)
        player_score, player_desc, player_ranks = self.take_turn("You", player_hand)

        net_gain = self.check_outcome(
            player_score, bot_score, player_ranks, bot_ranks
        )
        self.points += net_gain
        text.display_line(f"Net points this round: {net_gain}")
        return net_gain


class Roulette(Room):
    """Room with Russian Roulette.
    Implements the Russian Roulette Game"""
    name = "russian_roulette"

    def __init__(self):
        super().__init__()

    def die(self) -> None:
        """The player dies."""
        text.display_span(text.warn("Pew."))
        for delay in text.exponential_increase(25, increase=0.1):
            text.display_span(
                random.choice(
                    [text.warn(","), text.warn("."), "\n", " ", " "]
                )
            )
            text.pause(delay)

    def live(self) -> None:
        """The player lives."""
        text.display_line("Pew.")
        text.pause_medium()
        text.display_line("You... Live.")

    def play(self, score: int = 0) -> int:
        """Call this function to play this room. Takes the current score, and returns 0 as its the last room."""
        chambers, max_rotations = self.shop(score)

        text.display_line("Type your last words...")
        text.display_span("> ")
        text.pause_extra_long()
        text.erase_line()
        text.display_line("Ha. Fate waits for nobody.")

        # Discard extra input and sleep 2.5 seconds.
        text.conceal()
        text.pause_long()
        text.unconceal()

        text.display_line(f"The gun cocks. It has {chambers} chambers.")
        text.display_line(f"It could turn {max_rotations} times.")
        text.pause_long()

        text.linebreak()
        text.pause_medium()
        text.display_line("Ready?")
        text.pause_long()
        text.display_line("Not like I care.")
        text.linebreak()
        text.pause_short()

        rotations = random.randint(max_rotations // 3, max_rotations)
        bullet_fired = self.animate_roulette(rotations, chambers)

        if bullet_fired:
            self.die()
        else:
            self.live()
        return 0

    def shop(self, score: int) -> tuple[int, int]:
        """The shop to buy powerups for russian roulette.

        Returns a tuple of (chambers, max_rotations).
        """
        class RouletteShop:
            """Handles the shop logic for the roulette game."""
        
            def __init__(self, score: int):
                self.score = score
                self.chambers = 6
                self.max_rotations = 30
                self.chamber_cost = 10
                self.rotation_cost = 30
        
            def display_options(self) -> None:
                """Displays the shop options."""
                text.display_line("Welcome to the shop. you can buy these: ")
                text.display_line(f"1) ${self.chamber_cost}: Increase number of chambers from {self.chambers} -> {self.chambers+1}.")
                text.display_line(f"2) ${self.rotation_cost}: Decrease max number of rotations from {self.max_rotations} -> {self.max_rotations-1}")
                text.display_line(f"3) $0: Decrease number of chambers from {self.chambers} -> {self.chambers-1}")
                text.display_line(f"Your balance is: ${self.score}")
        
            def buy_chamber(self, n: Literal[1] | Literal[-1]) -> None:
                """Attempts to buy n chambers.
                
                Validate whether player has enough score to buy first.
                """
                if n == -1:  # Decrease chambers
                    text.display_line("You got: one less chamber...???")
                    if self.chambers <= 3:
                        text.display_line("Oops, the gun cant get smaller!")
                    else:
                        self.chambers -= 1
                elif n == 1:  # Increase chambers
                    text.display_line("You bought: one more chamber!")
                    self.chambers += 1
                    self.score -= self.chamber_cost
                    self.chamber_cost += 3  # Increase cost for next purchase
                else:
                    raise ValueError("n must be 1 or -1")
        
            def buy_rotation(self) -> None:
                """Attempts to buy one less rotation.
                
                Validate whether player has enough score to buy first.
                """
                text.display_line("You bought: one less rotation!")
                self.max_rotations -= 1
                self.score -= self.rotation_cost
                # Increasing cost for each additional upgrade, cost 900 to completely eliminate risk.
                self.rotation_cost += round(
                    1/(0.005 * (self.max_rotations - 1) + 0.0001) - (1/4) * (self.max_rotations - 1)
                )
            
            def prompt_purchase(self) -> str | None:
                """Prompts the user to make a purchase."""
                if (
                        self.score < self.chamber_cost
                        and self.score < self.rotation_cost
                ):
                    text.display_line(
                        "Whoops! You're too poor to buy anything more."
                    )
                    return None
                choice = prompt_choice(
                    "Which do you want to buy (any invalid option to quit)?",
                    choices=["1", "2", "3"],
                    reprompt_on_error=False
                )
                return choice
        
            def visit(self) -> None:
                """Visits the shop and allows the player to buy powerups."""
                while True:
                    self.display_options()
                    choice = self.prompt_purchase()
                    if choice is None:
                        break
                    elif choice == "1":
                        self.buy_chamber(1)
                    elif choice == "2":
                        self.buy_rotation()
                    elif choice == "3":
                        self.buy_chamber(-1)
                    else:
                        text.display_line("You exit the shop.")
                        break
        
        shop = RouletteShop(score)
        shop.visit()
        return shop.chambers, shop.max_rotations

    def format_barrel(self, barrel: list[str]) -> str:
        """Formats the barrel for display"""
        return " ".join([f"[{char}]" for char in barrel])

    def animate_roulette(self, rotations: int, chambers: int) -> bool:
        """An animated russian roulette.

        Returns True if the bullet is fired.
        """
        def rotate(barrel: list[str]) -> None:
            """Rotate the barrel by one position"""
            barrel.append(barrel.pop(0))

        # Create barrel
        barrel = ['.'] * chambers
        barrel[random.randint(0, chambers - 1)] = "0"

        text.display_line(" V")
        text.display_span(self.format_barrel(barrel))
        for delay in text.exponential_increase(rotations):
            rotate(barrel)
            text.erase_line()
            text.display_span(self.format_barrel(barrel))
            text.pause(delay)
        text.linebreak()
        return barrel[0] == "0"

# --- Example run ---
if __name__ == "__main__":
    room = Roulette()
    room.play(160)

# #testing
# baccarat = Baccarat()
# baccarat.play()
