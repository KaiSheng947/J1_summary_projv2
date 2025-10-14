from typing import Callable

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

    def draw_card(self) -> cards.Card:
        """Randomly generates cards for player and bot"""
        # Not simulating a deck; just generating
        return cards.create_random_card()

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

    def play_round(self) -> str:
        """play one round of blackjack and return game outcome"""
        player_hand = [self.draw_card(), self.draw_card()]
        bot_hand = [self.draw_card(), self.draw_card()]
        text.display_line(f"Bot 1st card: {bot_hand[0].as_string()}")
        text.linebreak()

        #Calculating Player Result
        self.show_hand('Your', player_hand)
        while (
                len(player_hand) < 5
                and self.calculate_hand_value(player_hand) <= 21
        ):
            redraw = prompt_choice(
                'Do you want to draw again?',
                choices=['y', 'n']
            )
            if redraw == 'y':
                player_hand.append(self.draw_card())
                total = self.calculate_hand_value(player_hand)
                self.show_hand('Your', player_hand)
            else:
                break
        
        #Calculating Bot Result
        text.linebreak()
        while self.calculate_hand_value(bot_hand) < 17:
            bot_hand.append(self.draw_card())
            bot_total = self.calculate_hand_value(bot_hand)
            
        if self.calculate_hand_value(bot_hand) > 21:
            self.show_hand('Bot', bot_hand)
        else:
            self.show_hand('Bot', bot_hand)

        #Determine winner
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
            text.display_line(self.play_round())
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

        #endings
        game_over = False
        points = 0
        rounds = 1
    
        while rounds <= 3:
            
            #displays current points and round
            text.display_line(f"Current Points: {points}")
            text.display_line(f"Current Round: {rounds}")

            bet = prompt_choice(
                "What would you like to wager on?",
                choices=["Player", "Banker", "Tie"]
            )

            #resets the winner to False
            player_win = False
            banker_win = False
            tie = False
            
            #displays starting hand
            player_hand = cards.create_random_hand(2)
            banker_hand = cards.create_random_hand(2)
            text.display_line("Player's hand and value")
            self.display_hand(player_hand)
            text.display_line("Banker's hand and value")
            self.display_hand(banker_hand)

            player_value = self.calculate_value_of_hand(player_hand)
            banker_value = self.calculate_value_of_hand(banker_hand)
            if banker_value > player_value:
                banker_win = True
            elif banker_value < player_value:
                player_win = True
            else:
                tie = True

            #condition for game to end early
            if banker_value >= 8 or player_value >= 8:
                if bet == "Player":
                    if player_win == True:
                        points += 100
                        self.display_win()
                    else:
                        points -= 100
                        self.display_loss()
                elif bet == "Banker":
                    if banker_win == True:
                        points += 100
                        self.display_win()
                    else:
                        points -= 100
                        self.display_loss()
                else:
                    #more points are rewarded for winning with a tie
                    if tie == True:
                        points += 150
                        self.display_win()
                    else:
                        points -= 100
                        self.display_loss()

            else:
                #slows the game down to show that game has not ended
                text.display_line("No natural 8s or 9s!")
                text.wait_visible(2.5, interval=0.5)

                #adds and displays the 3rd card
                player_hand.append(cards.create_random_card())
                banker_hand.append(cards.create_random_card())

                #displays the value
                self.display_hand(player_hand)
                self.display_hand(banker_hand)

                #calculating winner
                player_value = self.calculate_value_of_hand(player_hand)
                banker_value = self.calculate_value_of_hand(banker_hand)
                if banker_value > player_value:
                    banker_win = True
                elif banker_value < player_value:
                    player_win = True
                else:
                    tie = True

                if bet == "Player":
                    if player_win == True:
                        points += 100
                        self.display_win()
                    else:
                        points -= 100
                        self.display_loss()
                elif bet == "Banker":
                    if banker_win == True:
                        points += 100
                        self.display_win()
                    else:
                        points -= 100
                        self.display_loss()
                else:
                    #more points are rewarded for winning with a tie
                    if tie == True:
                        points += 150
                        self.display_win()
                    else:
                        points -= 100
                        self.display_loss()
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

    def _deal_cards(self, deck: list[cards.Card], num=3) -> list[cards.Card]:
        """deals num cards to player and dealer"""
        return [deck.pop() for _ in range(num)]

    def _evaluate_hand(self, hand: list[cards.Card]) -> tuple[int, str, list[int]]:
        """Calculates the value for poker hands using the simplified rules.
        
        Returns a tuple of (score, description, ranks) where:
        - score: int, the score value of the hand (higher is better)
        - description: str, a textual description of the hand
        - ranks: list[int], a list of card ranks used for tie-breaking
        """
        values = [card.value for card in hand]
        counts = {v: values.count(v) for v in set(values)}

        if 3 in counts.values():
            v = [k for k, c in counts.items() if c == 3][0]
            return (35, f"Three of a kind ({cards.NAMES[v]})", [self.VALUES[v]])

        if 2 in counts.values():
            v = [k for k, c in counts.items() if c == 2][0]
            kickers = sorted(
                [self.VALUES[val] for val in values if val != v],
                reverse=True
            )
            return (25, f"Pair of {cards.NAMES[v]}s", [self.VALUES[v]] + kickers)

        # High card case
        sorted_vals = sorted([self.VALUES[v] for v in values], reverse=True)
        high = sorted_vals[0]
        return (15, f"High card {cards.NAMES[high] if high!=14 else "Ace"}", sorted_vals)

    def display_hand(self, hand: list[cards.Card]) -> None:
        """Displays the player's hand"""
        text.display_line(" ".join([c.as_string() for c in hand]))

    def play(self, score: int = 0) -> int:
        """Plays one round of poker. Updates player_score and bot_score.
        Returns net points gained by the player (player_score - bot_score)."""
        deck = cards.create_deck()
        random.shuffle(deck)

        player_hand = self._deal_cards(deck, 3)
        bot_hand = self._deal_cards(deck, 3)

        # Update scores
        player_score, player_desc, player_ranks = self._evaluate_hand(player_hand)
        bot_score, bot_desc, bot_ranks = self._evaluate_hand(bot_hand)

        text.linebreak()
        text.display_line("--- Poker Round ---")
        text.display_span("Bot's hand: ")
        self.display_hand(bot_hand)
        
        prompt_continue("Press enter to draw...") # Little do they know its already drawn lol
        text.display_span("Your hand: ")
        self.display_hand(player_hand)

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


        # Points gained for this round
        net_gain = player_score - bot_score
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
        shot = self.animate_roulette(rotations, chambers)

        if shot == '0':
            self.die()
        else:
            self.live()
        return 0

    def shop(self, current_score: int) -> tuple[int, int]:
        """The shop to buy powerups for russian roulette.

        Returns a tuple of (chambers, max_rotations).
        """
        chambers = 6
        max_rotations = 30

        # Powerups: 
        # 1. Buy more chambers
        # 2. Buy less rotations

        # See graphs here: https://www.desmos.com/calculator/ouyracensx
        # Each cost increases
        next_chamber_cost = lambda: 10 + 3 * (chambers - 6) # First buy is 10pts, incereases by 3 per buy.
        # Increasing cost for each additional upgrade, cost 900 to completely eliminate risk.
        next_rotation_cost = lambda: round(30 + 1/(0.005 * (max_rotations - 1) + 0.0001) - (1/4) * (max_rotations - 1))

        while True:
            text.display_line("Welcome to the shop. you can buy these: ")
            chamber_cost = next_chamber_cost()
            text.display_line(f"1) ${chamber_cost}: Increase number of chambers from {chambers} -> {chambers+1}.")

            rotation_cost = next_rotation_cost()
            text.display_line(f"2) ${rotation_cost}: Decrease max number of rotations from {max_rotations} -> {max_rotations-1}")

            text.display_line(f"3) $0: Decrease number of chambers from {chambers} -> {chambers-1}")

            text.display_line(f"Your balance is: ${current_score}")
            if current_score < chamber_cost and current_score < rotation_cost:
                text.display_line(f"Whoops! You're too poor to buy anything more.")
                break
            choice = prompt_choice(
                "Which do you want to buy?",
                choices=["1", "2", "3"],
                reprompt_on_error=False
            )

            if choice == "1":
                text.display_line("You bought: one more chamber!")
                chambers += 1
                current_score -= chamber_cost
            elif choice == "2":
                text.display_line("You bought: one less rotation!")
                max_rotations -= 1
                current_score -= rotation_cost
            elif choice == "3":
                text.display_line("You got: one less chamber...???")
                if chambers <= 3:
                    text.display_line("Oops, the gun cant get smaller!")
                else:
                    chambers -= 1
            else:
                text.display_line("You exit the shop.")
                break
        return chambers, max_rotations

    def format_barrel(self, barrel: list[str]) -> str:
        """Formats the barrel for display"""
        return " ".join([f"[{char}]" for char in barrel])

    def animate_roulette(self, iter_num: int, chambers: int) -> str:
        """An animated russian roulette.

        Returns the chamber that is fired (0 is the bullet).
        """
        def rotate(barrel: list[str]) -> None:
            """Spins the barrel by one position"""
            barrel.append(barrel.pop(0))

        # Create barrel
        barrel = ['.'] * chambers
        barrel[random.randint(0, chambers - 1)] = "0"

        text.display_line(" V")

        text.display_span(self.format_barrel(barrel))
        for delay in text.exponential_increase(iter_num):
            rotate(barrel)
            text.erase_line()
            text.display_span(self.format_barrel(barrel))
            text.pause(delay) # Delay
        text.linebreak()
        return barrel[0] 

# --- Example run ---
if __name__ == "__main__":
    room = Roulette()
    room.play(160)

# #testing
# baccarat = Baccarat()
# baccarat.play()
