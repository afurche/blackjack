from deck import Deck
from random import random


class Game:
    score_cap = 21
    hit_bet = 50

    def __init__(self):
        self._deck = Deck()

    def hit(self):
        card = self._deck.hit()
        print(f'Added to table {str(card)}')
        return card.rank_val

    def move(self):
        pass

    def game(self, player_chips, func, screen):
        player_score, dealer_score, player_bets = 0, 0, 0
        outcome = ''  # possible outcome : 'win'/'draw'/'loss'
        self._deck.shuffle()
        dealer_card_1, dealer_card_2 = self._deck.hit(), self._deck.hit()
        dealer_score = dealer_card_1.rank_val + dealer_card_2.rank_val
        print(f'Player chips: {player_chips}')
        print(f"Dealer's first card: {str(dealer_card_1)}")
        while True:
            action = input('Select action: ')
            if action == 'hit':
                if player_bets < player_chips - 50:
                    player_score += self.hit()
                    player_bets += self.hit_bet
                    func(screen)
                    print(f'Player score: {player_score}')
                    if player_score > self.score_cap:
                        print("Oh no, You've busted :(\nDealer's turn")
                        print(f"Dealer's turn\nDealer's second card: {str(dealer_card_2)}")
                        while dealer_score < 17:
                            dealer_score += self.hit()
                        if dealer_score > self.score_cap:
                            print("It's a draw ! Dealer has also busted !!")
                            outcome = 'draw'
                            break
                        else:
                            print('Dealer has won :(')
                            outcome = 'loss'
                            break
                    elif player_score == self.score_cap:
                        print('BLACKJACK!!!\nCongratulations!!!!')
                        outcome = 'win'
                        break
                    else:
                        continue
                else:
                    print("You don't have enough chips !! You have to 'stand'")
                    continue
            elif action == 'stand':
                print(f"Dealer's turn\nDealer's second card {str(dealer_card_2)}")
                print(f"Dealer score: {dealer_score}")
                while dealer_score < 17:
                    dealer_score += self.hit()
                    print(f"Dealer score: {dealer_score}")
                if dealer_score > self.score_cap or player_score > dealer_score:
                    print("Congratulations You've won :)")
                    outcome = 'win'
                elif player_score == dealer_score:
                    print("It's a draw")
                    outcome = 'draw'
                elif player_score < dealer_score:
                    print("Oh no You've lost :(")
                    outcome = 'loss'
                break
        return outcome, player_bets

