from itertools import product
from typing import List
from random import shuffle
from settings import MESSAGES, SUITS, RANKS

class Card:
    def __init__(self, suit: str, rank: str, points: int) -> None:
        self.suit: str = suit
        self.rank: str = rank
        self.points: int = points

    def __str__(self) -> str:
        return f'{self.rank}{self.suit} {self.points} points'

class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = self._create_deck()
        shuffle(self.cards)

    def _create_deck(self) -> List[Card]:
        cards: List[Card] = []
        for suit, rank in product(SUITS, RANKS):
            if rank == 'A':
                points = 11
            elif rank.isdigit():
                points = int(rank)
            else:
                points = 10
            c = Card(suit=suit, rank=rank, points=points)
            cards.append(c)
        return cards

    def get_card(self) -> Card:
        return self.cards.pop()

    def __len__(self) -> int:
        return len(self.cards)