import abc
import random
from typing import List
from Deck import Card
from Deck import Deck
from settings import MESSAGES

class AbstractPlayer(abc.ABC):
    def __init__(self) -> None:
        self.cards: List[Card] = []
        self.bet: int = 0
        self.full_points: int = 0
        self.money: int = 100

    def change_points(self) -> None:
        self.full_points = sum([card.points for card in self.cards])

    def take_card(self, card: Card) -> None:
        self.cards.append(card)
        self.change_points()

    @abc.abstractmethod
    def change_bet(self, max_bet: int, min_bet: int) -> None:
        pass

    @abc.abstractmethod
    def ask_card(self) -> bool:
        pass

    def print_cards(self) -> None:
        for card in self.cards:
            print(card)
        print('Full points: ', self.full_points)

class Player(AbstractPlayer):

    def change_bet(self, max_bet: int, min_bet: int) -> None:
        while True:
            value = int(input('Make your bet: '))
            if min_bet < value < max_bet:
                self.bet = value
                self.money -= self.bet
                break
        print(f'Your bet is: {self.bet}')

    def ask_card(self) -> bool:
        choice = input(MESSAGES.get('ask_card'))
        return choice == 'y'

class Bot(AbstractPlayer):
    def __init__(self) -> None:
        super().__init__()
        self.max_points: int = random.randint(17, 20)

    def change_bet(self, max_bet: int, min_bet: int) -> None:
        self.bet = random.randint(min_bet, max_bet)
        self.money -= self.bet
        print(self, 'give: ', self.bet)

    def ask_card(self) -> bool:
        return self.full_points < self.max_points

class Dealer(AbstractPlayer):
    max_points: int = 17

    def change_bet(self, max_bet: int, min_bet: int) -> None:
        raise Exception('This type is dealer and he has no bets')

    def ask_card(self) -> bool:
        return self.full_points < self.max_points