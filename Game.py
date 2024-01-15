from typing import List
import Player
from settings import MESSAGES, SUITS, RANKS
from Deck import Deck
import random
from Player import Card
import time

class Game:
    max_pl_count = 4

    def __init__(self):
        self.players = []
        self.player = None
        self.dealer = Player.Dealer()
        self.player_pos = None
        self.all_players_count = 1
        self.deck = Deck()
        self.max_bet = 20
        self.min_bet = 0
    def reset_for_new_round(self) -> None:
        """
        Reset parameters for a new game round.
        """
        self.players = []
        self.player = None
        self.dealer = Player.Dealer()
        self.player_pos = None
        self.all_players_count = 1
        self.deck = Deck()
        self.max_bet = 20
        self.min_bet = 0
        self._launching()  # Вибрати нового гравця для нового раунду
    @staticmethod
    def _ask_starting(message: str) -> bool:
        while True:
            choice = input(message)
            if choice == 'n':
                return False
            elif choice == 'y':
                return True

    def _launching(self) -> None:
        while True:
            bots_count = int(input(MESSAGES.get('bots_count')))
            if bots_count <= self.max_pl_count - 1:
                break
        self.all_players_count = bots_count + 1

        for _ in range(bots_count):
            b = Player.Bot()
            self.players.append(b)
            print(b, ' is created')

        self.player = Player.Player()
        self.player_pos = random.randint(0, self.all_players_count)
        print("Your position is:", self.player_pos)
        self.players.insert(self.player_pos, self.player)

    def ask_bet(self) -> None:
        for player in self.players:
            player.change_bet(self.max_bet, self.min_bet)

    def first_descr(self) -> None:
        for player in self.players:
            for _ in range(2):
                card = self.deck.get_card()
                player.take_card(card)

        card = self.deck.get_card()
        self.dealer.take_card(card)
        self.dealer.print_cards()

    def check_stop(self, player: Player.AbstractPlayer) -> bool:
        if player.full_points >= 21:
            return True
        else:
            return False

    def remove_player(self, player: Player.AbstractPlayer) -> None:
        player.print_cards()
        if isinstance(player, Player.Player):
            print('You fell')
        elif isinstance(player, Player.Bot):
            print(player, 'fell!')
        self.players.remove(player)

    def ask_cards(self) -> None:
        for player in self.players:
            while player.ask_card():
                card = self.deck.get_card()
                player.take_card(card)

                is_stop = self.check_stop(player)
                if is_stop:
                    if player.full_points > 21 or isinstance(player, Player.Player):
                        self.remove_player(player)
                    break

                if isinstance(player, Player.Player):
                    player.print_cards()

    def check_winner(self) -> None:
        if self.dealer.full_points > 21:
            print('Dealer is fell! All players won!')
            for winner in self.players:
                winner.money += winner.bet * 2
            # all win
        else:
            for player in self.players:
                if player.full_points == self.dealer.full_points:
                    player.money += player.bet
                    print(MESSAGES.get('eq').format(player, player.full_points))
                elif player.full_points > self.dealer.full_points:
                    player.money += player.bet * 2
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('win').format(player))
                    elif isinstance(player, Player.Player):
                        print('You won!')
                elif player.full_points < self.dealer.full_points:
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('lose').format(player))
                    elif isinstance(player, Player.Player):
                        print('You lost!')

    def play_with_dealer(self) -> None:
        while self.dealer.ask_card():
            card = self.deck.get_card()
            self.dealer.take_card(card)
        self.dealer.print_cards()

    def start_game(self) -> None:
        message = MESSAGES.get('ask_start')
        # todo: max player count?
        if not self._ask_starting(message=message):
            exit(0)
        # generating data for starting
        self._launching()

        while True:
            self.ask_bet()

            # give first cards to players
            self.first_descr()

            # print player cards after first deal
            self.player.print_cards()

            # ask players about cards
            self.ask_cards()

            self.play_with_dealer()

            self.check_winner()

            print(f'Your money: {self.player.money}')

            if not self._ask_starting(MESSAGES.get('rerun')):
                break
            else:
                time.sleep(2)
                # Reset game parameters for a new round
                self.reset_for_new_round()