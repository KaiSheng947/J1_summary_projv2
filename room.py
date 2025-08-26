import time
import cards
import yaml
import random

with open("text.yaml", "r") as file:
    config = yaml.safe_load(file)

INPUT_FUNCTION = input
def prompt(question: str) -> str:
    """This function behaves the same as input().
    The pattern is to allow for automated testing."""
    return INPUT_FUNCTION(question)

class Room:
    """Parent class of all rooms. 
    Each room has a specific game."""
    def __init__(self):
        self.points = 0
        self.player_score = 0
        self.bot_score = 0
    
    def play(score: int) -> int:
        """Plays the room. Returns the score gain/loss due to the game.
        Eg. if you gained 20, return 20. If you lost 20, return -20."""
        raise NotImplementedError

class Blackjack(Room):
    """Room with blackjack.
    Implements the blackjack game"""
    def __init__(self):
        super().__init__()
        
    def show(self) -> None:
        """Display room info."""
        print(config["rooms"]["blackjack"]["description"])
        for i in range(5):
                    print(".", end = "", flush = True)
                    time.sleep(1)
                    print("")
        print(config["rooms"]["blackjack"]["rules"])


    def draw_card(self) -> str:
        """Randomly generates cards for player and bot"""
        # Not simulating a deck; just generating
        return cards.generate_card().as_string()
    
    def calculate_card(self, hand):
        """Calculates card value in hand"""
        # Card values for this game.
        VALUES = {
        'A': 11, # Ace starts at 11 for blackjack
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '1': 10,
        'J': 10, # Jack
        'Q': 10, # Queen
        'K': 10  # King
    }
        total = 0
        aces = 0
        for cards in hand:
            total += VALUES[cards[5]]
            # Account for aces as it can be 11 or 1
            if cards[5] == 'A':
                aces += 1
                while total > 21 and aces:
                    total -= 10
                    aces -= 1
        return total

    def show_hand(self, owner: str, hand: list[str], total: int):
        """displays the hand bot and player have"""
        print(f"{owner} hand: {', '.join(hand)} \n{owner} Total: {total}")

    def play_round(self) -> str:
        """play one round of blackjack and return game outcome"""
        player_hand = [self.draw_card(), self.draw_card()]
        total = self.calculate_card(player_hand)
        bot_hand = [self.draw_card(), self.draw_card()]
        bot_total = self.calculate_card(bot_hand)
        print(f"Bot 1st card: {bot_hand[0]}")
        print('')

        #Calculating Player Result
        self.show_hand('Your', player_hand, total)
        while len(player_hand) < 5 and total <= 21:
            redraw = prompt('Do you want to draw again? y/n ')
            if redraw == 'y':
                player_hand.append(self.draw_card())
                total = self.calculate_card(player_hand)
                self.show_hand('Your', player_hand, total)
            else:
                break
        
        #Calculating Bot Result
        print('')
        while bot_total < 17:
            bot_hand.append(self.draw_card())
            bot_total = self.calculate_card(bot_hand)
            
        if bot_total > 21:
            self.show_hand('Bot', bot_hand, bot_total)
        else:
            self.show_hand('Bot', bot_hand, bot_total)

        #Determine winner
        if total > 21 and bot_total > 21:
            self.points -= 100
            return "Both bust! You win 100 points"
        elif bot_total > 21:
            self.points += 100
            return "Bot busts! You win 100 points"
        elif total > 21:
            self.points -= 20
            return "You bust! You lose 20 points."
        elif total == bot_total:
            self.points -= 20
            return "Tie! You lose 20 points!"
        elif total > bot_total:
            self.points += 100
            return "You win 100 points!"
        else:
            self.points -= 20
            return "You lose 20 points!"
    
    def play(self, _):
        """Plays blackjack 3 rounds"""
        for i in range(3):
            print('')
            prompt(f'Round {i+1}! [Press enter to continue]')
            print(self.play_round())
            print('')
        return self.points

class Baccarat(Room):
    """Room with Baccarat.
    Implements the Baccarat Game"""
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
        super()._init_()
    
    def show(self) -> None:
        """Display room info."""
        print(config["rooms"]["baccarat"]["description"])
        for i in range(5):
                    print(".", end = "", flush = True)
                    time.sleep(1)
                    print("")
        print(config["rooms"]["baccarat"]["rules"])

    def play(self, _):
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
    
        while not game_over and rounds <= 3:
            #base case
            if points < 0:
                game_over = True
                break
            
            #displays current points and round
            print(f"Current Points: {points}\n Current Round: {rounds}")
                
            #checks for validity

            bet = prompt("What would you like to wager on? (Player, Banker, Tie - caps sensitive): ")

            if bet not in ["Player", "Banker", "Tie"]:
                continue

            #resets the winner to False
            player_win = False
            banker_win = False
            tie = False
        
            
            #displays starting hand
            player_hand = [cards.generate_card(), cards.generate_card()]
            banker_hand = [cards.generate_card(), cards.generate_card()]

            #calculates starting value
            player_value = self.calculate_value(player_hand)
            banker_value = self.calculate_value(banker_hand)
            
            #displays hand
            self.display_hand(player_hand, banker_hand, player_value, banker_value)

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
                        points += 20
                        self.display_win()
                    else:
                        points -= 20
                        self.display_loss()
                elif bet == "Banker":
                    if banker_win == True:
                        points += 20
                        self.display_win()
                    else:
                        points -= 20
                        self.display_loss()
                else:
                    #more points are rewarded for winning with a tie
                    if tie == True:
                        points += 50
                        self.display_win()
                    else:
                        points -= 20
                        self.display_loss()

            else:
                #slows the game down to show that game has not ended
                print("No natural 8s or 9s!")

                for i in range(5):
                    print(".", end = "", flush = True)
                    time.sleep(0.5)
                print("")

                #adds and displays the 3rd card
                player_hand.append(cards.generate_card())
                banker_hand.append(cards.generate_card())

                #calculates new values
                player_value = self.calculate_value(player_hand)
                banker_value = self.calculate_value(banker_hand)

                #displays the value
                self.display_hand(player_hand, banker_hand, player_value, banker_value)

                #calculating winner
                if banker_value > player_value:
                    banker_win = True
                elif banker_value < player_value:
                    player_win = True
                else:
                    tie = True

                if bet == "Player":
                    if player_win == True:
                        points += 20
                        self.display_win()
                    else:
                        points -= 20
                        self.display_loss()
                elif bet == "Banker":
                    if banker_win == True:
                        points += 20
                        self.display_win()
                    else:
                        points -= 20
                        self.display_loss()
                else:
                    #more points are rewarded for winning with a tie
                    if tie == True:
                        points += 50
                        self.display_win()
                    else:
                        points -= 20
                        self.display_loss()

            #closer to base case
            rounds += 1
        
        return points
        

    def calculate_value(self, hand: list) -> int:
        """calculates the values of the player's or dealer's hand
        based on baccarat values
        """
        total_values = 0
        for card in hand:
            total_values += self.VALUES.get(card.value)
        total_values = total_values % 10
        return total_values

    def display_loss(self) -> None:
        """Displays a message when the better loses
        """
        print("You lost!")

    def display_win(self) -> None:
        """Displays a message when the better wins
        """
        print("You won!")
    
    def display_hand(self, hand1, hand2, value1, value2) -> str:
        """displays both the Player's and Banker's Hand,
        hand1 and value1 are the Player's hands and hand's value respectively,
        hand2 and value2 are the Banker's hands and hand's value respectively.
        """
        print("Player's hand and value")
        for card in hand1:
            print(card.as_string())
        print(value1)
        print("Banker's hand and value")
        for card in hand2:
            print(card.as_string())
        print(value2)

class Poker(Room):
    # Poker values dictionary inside the class
    POKER_VALUES = {
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

    def show(self) -> None:
        """Display room info."""
        print(config["rooms"]["poker"]["description"])
        for i in range(5):
                    print(".", end = "", flush = True)
                    time.sleep(1)
                    print("")
        print(config["rooms"]["poker"]["rules"])

    def _create_deck(self):
        return [Card(suit, value) for suit in SUIT_SYMBOL for value in NAMES]

    def _deal_cards(self, deck, num=3):
        return [deck.pop() for _ in range(num)]

    def _evaluate_hand(self, hand):
        values = [card.value for card in hand]
        counts = {v: values.count(v) for v in set(values)}

        if 3 in counts.values():
            v = [k for k, c in counts.items() if c == 3][0]
            return (3, f"Three of a kind ({NAMES[v]})")

        if 2 in counts.values():
            v = [k for k, c in counts.items() if c == 2][0]
            return (2, f"Pair of {NAMES[v]}s")

        high = max(values, key=lambda v: self.POKER_VALUES[v])
        return (1, f"High card {NAMES[high]}")

    def play(self, score=0) -> int:
        """Plays one round of poker. Updates player_score and bot_score.
        Returns net points gained by the player (player_score - bot_score)."""
        deck = self._create_deck()
        random.shuffle(deck)

        player_hand = self._deal_cards(deck, 3)
        bot_hand = self._deal_cards(deck, 3)

        player_score, player_desc = self._evaluate_hand(player_hand)
        bot_score, bot_desc = self._evaluate_hand(bot_hand)

        print("\n--- Poker Round ---")
        print("Your hand: " + " ".join([c.as_string() for c in player_hand]) + f" → {player_desc}")
        print("Bot hand: " + " ".join([c.as_string() for c in bot_hand]) + f" → {bot_desc}")

        # Update scores
        self.player_score += player_score
        self.bot_score += bot_score

        if player_score > bot_score:
            print(f"You win this round! (+{player_score})")
        elif bot_score > player_score:
            print(f"Bot wins this round! (+{bot_score} to bot)")
        else:
            print(f"This round is a tie! (+{player_score} each)")

        # Points gained for this round
        net_gain = player_score - bot_score
        self.points += net_gain
        print(f"Net points this round: {net_gain}")
        print(f"Total player score: {self.player_score}, Bot score: {self.bot_score}\n")

        return net_gain


# --- Example run ---
# if __name__ == "__main__":
#     room = PokerRoom()
#     for _ in range(3):
#         room.play()



# #testing
# baccarat = Baccarat()
# baccarat.play()
