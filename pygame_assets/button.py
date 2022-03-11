import pygame


class Button:

    def __init__(self, text, font, width, height, pos, func):
        self._pressed = False

        self._font = font
        self._rect = pygame.Rect(pos, (width, height))
        self._color = '#475f77'

        self._text_surf = self._font.render(text, True, '#FFFFFF')
        self._text_rect = self._text_surf.get_rect(center=self._rect.center)

        self._func = func

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self._rect, border_radius=12)
        screen.blit(self._text_surf, self._text_rect)
        pygame.display.update()
        return self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self._rect.collidepoint(mouse_pos):
            self._color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self._pressed = True
            else:
                if self._pressed:
                    self._func()
                    self._pressed = False
        else:
            self._color = '#475f77'

