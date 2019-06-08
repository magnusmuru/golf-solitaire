"""Golf solitaire."""
from itertools import zip_longest
from textwrap import dedent
from cards import Deck


class Solitaire:
    """
    Solitaire class representing a game of Golf Solitaire.

    This game has 7 columns and 5 cards in each column,
    but the methods should work with other valid values as well.
    """

    columns = 7
    cards_in_column = 5

    def __init__(self):
        """
        Constructor, do the setup here.

        After setup with Solitaire.columns = 7, Solitaire.cards_in_column = 5
        You should have:
        self.tableau -> 7 columns of cards with 5 cards in each column
        self.stock -> 16 cards
        self.waste -> 1 card
        """
        # your code, replace with proper setup
        new_deck = Deck()
        new_deck.shuffle_deck()
        self.deck = new_deck
        column = []
        columns = []
        for i in range(self.columns * self.cards_in_column + 1):
            if i % self.cards_in_column == 0 and i != 0:
                columns.append(column)
                column = []
            if i != self.columns * self.cards_in_column:
                column.append(self.deck.cards.pop(-1))

        self.tableau = columns
        # -> list of (columns[lists] (where each list -> cards_in_column * Card instances))
        self.waste = [self.deck.cards.pop(-1)]  # -> list of Card instances
        self.stock = self.deck.cards

    def can_move(self, card) -> bool:
        """
        Validate if a card from the tableau can be moved to the waste pile.

        The card must be last in the column list and adjacent by rank
        to the topmost card of the waste pile (last in waste list).
        Example: 8 is adjacent to 7 and 9. Ace is only adjacent to 2.
        King is only adjacent to Queen.
        """
        last_cards = []
        for i in self.tableau:
            if len(i) > 0:
                last_cards.append(i[-1])
        if card in last_cards:
            if self.waste[-1].rank == card.rank + 1 or self.waste[-1].rank == card.rank - 1:
                return True
        return False

    def move_card(self, col: int):
        """
        Move a card from the tableau to the waste pile.

        Does not validate the move.
        :param col: index of column
        """
        self.waste.append(self.tableau[col].pop(-1))

    def deal_from_stock(self):
        """
        Deal last card from stock pile to the waste pile.

        If the stock is empty, do nothing.
        """
        if len(self.stock) > 0:
            self.waste.append(self.stock.pop(-1))

    def card_count(self) -> int:
        """"Count remaining cards in play."""
        counted_cards = 0
        for i in self.tableau:
            counted_cards += len(i)
        return counted_cards

    def has_won(self) -> bool:
        """Check for the winning position - no cards left in tableau."""
        if self.card_count() == 0:
            return True
        return False

    def has_lost(self) -> bool:
        """
        Check for the losing position.

        Losing position: no cards left in stock and no possible moves.
        """
        if self.card_count() > 0 and len(self.stock) == 0:
            for i in self.tableau:
                if len(i) > 0:
                    if self.can_move(i[-1]):
                        return False
            return True

    def print_game(self):
        """
        Print the game.

        Assumes:
        Card(decorated=True) by default it is already set to True
        self.tableau -> a list of lists (each list represents a column of cards)
        self.stock -> a list of Card objects that are in the stock
        self.waste_pile -> a list of Card objects that are in the waste pile

        You may modify/write your own print_game.
        """
        print(f" {'    '.join(list('0123456'))}")
        print('-' * 34)
        print("\n".join([(" ".join((map(str, x)))) for x in (zip_longest(*self.tableau, fillvalue="    "))]))
        print()
        print(f"Stock pile: {len(self.stock)} card{'s' if len(self.stock) != 1 else ''}")
        print(f"Waste pile: {self.waste[-1] if self.waste else 'Empty'}")

    @staticmethod
    def rules():
        """Print the rules of the game."""
        print("Rules".center(40, "-"))
        print(dedent("""
                Objective: Move all the cards from each column to the waste pile.

                A card can be moved from a column to the waste pile if the
                rank of that card is one higher or lower than the topmost card
                of the waste pile. Only the first card of each column can be moved.

                You can deal cards from the stock to the waste pile.
                The game is over if the stock is finished and
                there are no more moves left.

                The game is won once the tableau is empty.

                Commands:
                  (0-6) - integer of the column, where the topmost card will be moved
                  (d) - deal a card from the stock
                  (r) - show rules
                  (q) - quit
                  """))

    def play(self):
        """
        Play a game of Golf Solitaire.

        Create the game loop here.
        Use input() for player input.
        Available commands are described in rules().
        """
        print("Lets play Golf Solitaire! r - rules, d - deal, q - quit")
        print("Enter the column number.\n")
        while True:
            self.print_game()
            player_input = input("Command:")
            if player_input == 'r':
                self.rules()
            if player_input == 'q':
                print("Thank you for playing!")
                break
            if player_input == 'd':
                self.deal_from_stock()
            if player_input in list(map(str, list(range(len(self.tableau))))):
                col_num = int(player_input)
                if len(self.tableau[col_num]) > 0:
                    if self.can_move(self.tableau[col_num][-1]):
                        self.move_card(col_num)
            if self.has_won():
                print("You win!")
                break
            if self.has_lost():
                print(f"You lose with {self.card_count()} cards left!")
                break


if __name__ == '__main__':
    s = Solitaire()
    s.play()
