from deck import Deck
from player import Player
from pygame_assets.button import Button
import pygame as pygame
import os as os


class Table:
    """
    Table is representing a casino table where games are happening,
    also is responsible for handling pygame logic
    """
    SCREEN_HEIGHT, SCREEN_WIDTH = 800, 1000
    PLAYER_STAND_EVENT = 0
    PLAYER_HIT_EVENT = 1
    START_SCREEN_ON_EVENT = 2
    BLACKJACK_EVENT = 3
    WIN_EVENT = 4
    DRAW_EVENT = 5
    BET = 100
    BLACKJACK = 1.5
    WIN = 1.2

    def __init__(self):

        self._deck = Deck()
        self._player = Player()

        self._player_score = 0
        self._dealer_score = 0
        self._score_cap = 21
        self._session = True

        # following variables represent initial positions for placing cards for player and dealer
        self._player_x = 400
        self._player_y = 350
        self._dealer_x = 400
        self._dealer_y = 150

        # variables describing logical state of the game
        self._player_stands = False
        self._dealer_2_card_revealed = False
        self._game_run = False  # game starts after player bets
        self._game_over = False
        self._score_was_blit = False
        self._chips_were_blit = False
        self._player_hit = False
        self._player_turn_end = False
        self._player_bet = False
        self._chips_balanced = False
        self._quit_on_start_screen = False

        # pygame assets initialization
        pygame.init()
        self._screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Blackjack')
        self._bg = pygame.image.load(os.path.join('img', 'bg_table.jpg'))
        self._screen.blit(self._bg, self._bg.get_rect())
        self._hit_button = Button('Hit', pygame.font.Font(None, 30), 200, 40, (75, 200), self.hit)
        self._stand_button = Button('Stand', pygame.font.Font(None, 30), 200, 40, (75, 250), self.stand)
        self._play_again_button = Button('Play again', pygame.font.Font(None, 30), 200, 40, (75, 200), self.restart_game)
        self._end_game_button = Button('End game', pygame.font.Font(None, 30), 200, 40, (75, 250), self.end_game)
        self._bet_button = Button('Bet', pygame.font.Font(None, 30), 200, 40, (380, 350), self.player_bet)
        self._title = pygame.font.Font(os.path.join('fonts', 'PlayfairDisplay-Regular.ttf'), 80).render('Blackjack', False, '#FFFFFF')
        self._title_start_screen = pygame.font.Font(os.path.join('fonts', 'PlayfairDisplay-Regular.ttf'), 120).render('Blackjack', False, '#FFFFFF')
        self._dealer_hand_title = pygame.font.Font(os.path.join('fonts', 'PlayfairDisplay-Regular.ttf'), 35).render("Dealer hand", False, '#FFFFFF')
        self._player_hand_title = pygame.font.Font(os.path.join('fonts', 'PlayfairDisplay-Regular.ttf'), 35).render("Player hand", False, '#FFFFFF')
        self._player_score_title = pygame.font.Font(None, 45).render("Player score: ", False, '#FFFFFF')
        self._player_chips_title = pygame.font.Font(None, 45).render("Player chips: ", False, '#FFFFFF')
        self._card_placement_sound = pygame.mixer.Sound(os.path.join('music', 'card_placement.mp3'))
        self._clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join('music', 'bg_music.mp3'))
        pygame.mixer.music.set_volume(50)
        pygame.mixer.music.play(-1)
        pygame.display.update()

    def blit_start_screen(self):
        self._screen.blit(self._bg, self._bg.get_rect())
        self._screen.blit(self._title_start_screen, (240, 60))
        self._screen.blit(self._player_chips_title, (340, 300))
        menu_photo = pygame.image.load(os.path.join('img', 'start_screen.png'))
        self._screen.blit(menu_photo, (100, 300))

    def blit_basic_screen(self):
        self._screen.blit(self._bg, self._bg.get_rect())
        self._screen.blit(self._title, (30, 50))
        self._screen.blit(self._dealer_hand_title, (400, 100))
        self._screen.blit(self._player_hand_title, (400, 300))
        self._screen.blit(self._player_score_title, (75, 420))
        self._screen.blit(self._player_chips_title, (75, 460))

    def table_reset(self):
        self._deck = Deck()
        self._player_stands = False
        self._dealer_2_card_revealed = False
        self._game_over = False
        self._score_was_blit = False
        self._player_hit = False
        self._player_turn_end = False
        self._player_x = 400
        self._dealer_x = 400
        self._player_score = 0
        self._dealer_score = 0
        self._score_cap = 21
        self._chips_balanced = False

    def blackjack_init(self):
        pygame.init()
        self._player_stands = False
        self._deck.shuffle()
        dealer_init_cards = [self._deck.hit() for _ in range(2)]
        player_init_cards = [self._deck.hit() for _ in range(2)]
        self._dealer_score = dealer_init_cards[0].rank_val + dealer_init_cards[1].rank_val
        self._player_score = player_init_cards[0].rank_val + player_init_cards[1].rank_val
        return dealer_init_cards, player_init_cards

    def init_cards_draw(self, dealer_card1, player_cards):
        dealer_card_1_img = self.get_card_img(dealer_card1)
        self.draw_card(dealer_card_1_img, (self._dealer_x, self._dealer_y))
        self._dealer_x += 100
        card_back = pygame.image.load(os.path.join('img', 'card_sprites', 'card_back.png'))
        self.draw_card(card_back, (self._dealer_x, self._dealer_y))
        for card_img in self.get_multiple_card_img(player_cards):
            self.draw_card(card_img, (self._player_x, self._player_y))
            self._player_x += 100

    def show_player_score(self):
        if not self._score_was_blit:
            self._screen.blit(pygame.font.Font(None, 45).render(str(self._player_score), False, '#FFFFFF'), (270, 420))
            pygame.display.update()
            self._score_was_blit = True
        elif self._player_hit:
            dirty_blit_img = pygame.image.load(os.path.join('img', 'dirty_blit.png'))
            self._screen.blit(dirty_blit_img, (270, 400))
            pygame.display.update()
            self._screen.blit(pygame.font.Font(None, 45).render(str(self._player_score), False, '#FFFFFF'), (270, 420))
            pygame.display.update()
            self._player_hit = False

    def show_player_chips(self, coord):  # (270, 460) for game (270, 300) for start screen
        if not self._chips_were_blit:
            self._screen.blit(pygame.font.Font(None, 45).render(str(self._player.player_chips), False, '#FFFFFF'), coord)
            pygame.display.update()
            self._chips_were_blit = True
        else:
            dirty_blit_img = pygame.image.load(os.path.join('img', 'dirty_blit.png'))
            self._screen.blit(dirty_blit_img, (270, 450))
            pygame.display.update()
            self._screen.blit(pygame.font.Font(None, 45).render(str(self._player.player_chips), False, '#FFFFFF'), coord)
            pygame.display.update()
            self._player_bet = False

    def player_bet(self):
        self._player.player_chips -= 100
        player_bet_event = pygame.event.Event(pygame.USEREVENT, EventType=self.START_SCREEN_ON_EVENT)
        pygame.event.post(player_bet_event)

    @staticmethod
    def get_card_img(card):
        return pygame.image.load(os.path.join('img', 'card_sprites', card.suit, f'{card.rank}.png'))

    def draw_card(self, card_img, coord):
        pygame.time.wait(500)
        self._card_placement_sound.play()
        self._screen.blit(card_img, coord)
        pygame.display.update()

    def hit(self):
        if not self._game_over:
            card = self._deck.hit()
            card_img = self.get_card_img(card)
            self.draw_card(card_img, (self._player_x, self._player_y))
            self._player_x += 100
            self._player_score += card.rank_val
            hit_event = pygame.event.Event(pygame.USEREVENT, EventType=self.PLAYER_HIT_EVENT)
            pygame.event.post(hit_event)

    def stand(self):
        if not self._game_over:
            self._player_stands = True

    def get_multiple_card_img(self, cards):
        card_imgs = []
        for card in cards:
            card_imgs.append(self.get_card_img(card))
        return card_imgs

    def player_turn_end_post_event(self):
        if (self._player_score >= self._score_cap or self._player_stands) and not self._player_turn_end:
            player_stand_event = pygame.event.Event(pygame.USEREVENT, EventType=self.PLAYER_STAND_EVENT)
            pygame.event.post(player_stand_event)
            self._score_cap = 99

    def after_player_turn(self, dealer_card_2):
        if self._player_turn_end:
            self.dealer_turn(dealer_card_2)
            self.declare_winner()

    def dealer_turn(self, dealer_card_2):
        dealer_card_2_img = self.get_card_img(dealer_card_2)
        if not self._dealer_2_card_revealed:
            self.draw_card(dealer_card_2_img, (self._dealer_x, self._dealer_y))
            self._dealer_2_card_revealed = True
        self._dealer_x += 100
        while self._dealer_score < 17:
            card = self._deck.hit()
            card_img = self.get_card_img(card)
            self.draw_card(card_img, (self._dealer_x, self._dealer_y))
            self._dealer_x += 100
            self._dealer_score += card.rank_val

    def declare_winner(self):
        self._score_cap = 21  # score_cap was changed to 99 in self.player_end_turn_post_event() to avoid infinite loop of it, here it is corrected
        if self._score_cap == self._player_score and self._player_score > self._dealer_score:
            self._screen.blit(pygame.font.Font(None, 45).render("BLACKJACK !!!", False, '#FFFFFF'), (200, 600))
            if not self._chips_balanced:
                blackjack_event = pygame.event.Event(pygame.USEREVENT, EventType=self.BLACKJACK_EVENT)
                pygame.event.post(blackjack_event)
        elif self._score_cap >= self._player_score > self._dealer_score or (self._dealer_score > self._score_cap >= self._player_score):
            self._screen.blit(pygame.font.Font(None, 45).render("You won !!!", False, '#FFFFFF'), (200, 600))
            if not self._chips_balanced:
                win_event = pygame.event.Event(pygame.USEREVENT, EventType=self.WIN_EVENT)
                pygame.event.post(win_event)
        elif self._score_cap >= self._dealer_score > self._player_score or (self._player_score > self._score_cap >= self._dealer_score):
            self._screen.blit(pygame.font.Font(None, 45).render("You lost :(", False, '#FFFFFF'), (200, 600))
        elif self._player_score == self._dealer_score or (self._player_score > self._score_cap and self._dealer_score > self._score_cap):
            self._screen.blit(pygame.font.Font(None, 45).render("It's a draw", False, '#FFFFFF'), (200, 600))
            if not self._chips_balanced:
                draw_event = pygame.event.Event(pygame.USEREVENT, EventType=self.DRAW_EVENT)
                pygame.event.post(draw_event)
        self._game_over = True

    def start_screen_event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._player_bet = True
                self._game_run = False
                self._session = False
                self._quit_on_start_screen = True
            elif event.type == pygame.USEREVENT:
                if event.EventType == self.START_SCREEN_ON_EVENT:
                    self._game_run = True
                    self._player_bet = True

    def game_event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_run = False
                self._session = False
            elif event.type == pygame.USEREVENT:
                if event.EventType == self.PLAYER_STAND_EVENT:
                    self._player_turn_end = True
                elif event.EventType == self.PLAYER_HIT_EVENT:
                    if not self._game_over:
                        self._player_hit = True
                elif event.EventType == self.BLACKJACK_EVENT:
                    self._player.player_chips += int(self.BET * self.BLACKJACK)
                    self._chips_balanced = True
                elif event.EventType == self.WIN_EVENT:
                    self._player.player_chips += int(self.BET * self.WIN)
                    self._chips_balanced = True
                elif event.EventType == self.DRAW_EVENT:
                    self._player.player_chips += self.BET
                    self._chips_balanced = True

    def restart_game(self):
        self._game_run = False

    def end_game(self):
        self._game_run = False
        self._session = False

    def play_again(self):
        if self._game_over:
            self._play_again_button.draw(self._screen)
            self._end_game_button.draw(self._screen)
            self.show_player_chips((270, 460))

    def blackjack(self):
        while self._session:
            self.blit_start_screen()
            self.show_player_chips((550, 300))
            while not self._player_bet:
                if self._player.player_chips >= self.BET:
                    self._bet_button.draw(self._screen)
                elif self._player.player_chips < self.BET:
                    self._screen.blit(pygame.font.Font(None, 45).render("Oh no, you're out of chips :( :( :(", False, '#FFFFFF'), (100, 450))
                    pygame.display.update()
                self.start_screen_event_catcher()
            if not self._quit_on_start_screen:
                self.blit_basic_screen()
                self.show_player_chips((270, 460))
                dealer_init_cards, player_init_cards = self.blackjack_init()
                self.init_cards_draw(dealer_init_cards[0], player_init_cards)
                while self._game_run:
                    self._clock.tick(60)
                    self.show_player_score()
                    self.game_event_catcher()
                    if not self._game_over:
                        self._hit_button.draw(self._screen)
                        self._stand_button.draw(self._screen)
                    self.after_player_turn(dealer_init_cards[1])
                    self.player_turn_end_post_event()
                    self.play_again()
                    pygame.display.update()
            self.table_reset()
        self._player.update_save()
