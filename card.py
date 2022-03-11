
class Card:

    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank
        try:
            self._rank_val = int(rank)
        except ValueError:
            if rank in {'J', 'Q', 'K'}:
                self._rank_val = 10
            elif rank == 'A':
                self._rank_val = 11

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def rank_val(self):
        return self._rank_val

    def __str__(self):
        return f'{self._suit} {self._rank}'




