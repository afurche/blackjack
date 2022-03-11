
class Player:

    def __init__(self):
        with open('save.txt', 'r') as save:
            self._player_chips = int(save.readline())

    @property
    def player_chips(self):
        return self._player_chips

    @player_chips.setter
    def player_chips(self, player_chips):
        self._player_chips = player_chips

    def update_save(self):
        with open('save.txt', 'w') as save:
            save.truncate()
            save.write(str(self._player_chips))


