import cards

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
   
    def __init__(self):
        super().__init__()
        
    def show(self) -> None:
        """Display room info and rules"""
        print("Blackjack room (placeholder)")

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
        print(f"{owner} hand: {', '.join(hand)} \n{owner} Total: {total}")

    def play(self):
        """implements the blackjack game"""
        player_hand = [self.draw_card(), self.draw_card()]
        total = self.calculate_card(player_hand)
        bot_hand = [self.draw_card(), self.draw_card()]
        bot_total = self.calculate_card(bot_hand)
        print(f"Bot 1st card: {bot_hand[0]}")
        print('')

        #Calculating Player Result
        self.show_hand('Your', player_hand, total)
        while total < 16:
            player_hand.append(self.draw_card())
            total = self.calculate_card(player_hand)
            self.show_hand('Your', player_hand, total)
            if total > 21:
                print("Bust!")
        
        redraw = input('Do you want to draw again? y/n ')
        if redraw == 'y':
            player_hand.append(self.draw_card())
            total = self.calculate_card(player_hand)
            self.show_hand('Your', player_hand, total)
            if total > 21:
                print("Bust!")
        print('')
        
        #Calculating Bot Result
        while bot_total < 19:
            bot_hand.append(self.draw_card())
            bot_total = self.calculate_card(bot_hand)
            
        if bot_total > 21:
            self.show_hand('Bot', bot_hand, bot_total)
        else:
            self.show_hand('Bot', bot_hand, bot_total)

        #Determine winner
        print('')
        if total > 21 and bot_total > 21:
            return "Both bust! You lose!"
        elif total > 21:
            return "Bust! You lose."
        elif bot_total > 21:
            return "Bot busts! You win."
        elif total == bot_total:
            return "Tie! You lose!"
        elif total > bot_total:
            return "You win!"
        else:
            return "You lose!"

class Baccarat(Room):
    """Room with Baccarat.
    Implements the Baccarat Game"""
    def __init__(self):
        super().__init__()
        # self.VALUES = 
    
    def show(self) -> None:
        """Display room info."""
        print("Baccarat room (placeholder)")

    def play(self):
        pass

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

