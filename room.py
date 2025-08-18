import time
import cards

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

class Blackjack(Room):
    """Room with blackjack.
    Implements the blackjack game"""
    VALUES = { # Card values for this game.
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
        
    
    def show(self) -> None:
        """Display room info and rules"""
        print("Blackjack room (placeholder)")

    def draw_card(self) -> cards.Card:
        """Randomly generates the values
        and the suit symbol of a card 
        for the class Card 
        """
        # Not simulating a deck; just generating
        # random cards
        return cards.generate_card()

    def hand_value(self):
        """Calculate value of cards"""
        sum()

    def play(self):
        """TODO: docstring"""
        while self.player_score < 3:
            player_hand = [self.draw_card(), self.draw_card()]
            bot_hand = [self.draw_card(), self.draw_card()]

class Baccarat(Room):
    """Room with Baccarat.
    Implements the Baccarat Game"""
    def __init__(self):
        super().__init__()
        self.VALUES = { # Card values for this game.
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
    
    def show(self) -> None:
        """Display room info."""
        print("Baccarat room (placeholder)")

    def play(self):
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
        points = 100
        rounds = 1
    
        while not game_over and rounds < 4:
            #base case
            if points < 0:
                game_over = True
                break
            
            #displays current points and round
            print(f"Current Points: {points}\n Current Round: {rounds}")
                
            #checks for validity
            bet = prompt("What would you like to wager on? (Player, Banker, Tie - caps sensitive)")
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
                player_value = True
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
                time.sleep(5)

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
                    player_value = True
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
    """Room with Poker.
    Implements the Poker Game"""
    def __init__(self):
        super().__init__()

    def show(self) -> None:
        """Display room info."""
        print("Poker room (placeholder)")

    def play(self):
        pass


#testing
baccarat = Baccarat()
baccarat.play()