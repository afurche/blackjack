from card import Card
from numpy.random import shuffle


class Deck:
    suits = ['Club', 'Diamond', 'Heart', 'Spade']
    ranks = [str(i + 1) for i in range(2, 10)] + ['J', 'Q', 'K', 'A']

    def __init__(self):
        self._cards = []
        for suit in self.suits:
            for ranks in self.ranks:
                self._cards.append(Card(suit, ranks))

    def shuffle(self):
        shuffle(self._cards)

    def hit(self):
        return self._cards.pop()
